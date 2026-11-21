#!/usr/bin/env python3
"""Date-windowed sweep for work that appeared since the last check of a topic.

Reads a watch profile (topic_watch.json), asks OpenAlex and arXiv for
  - papers matching each saved query,
  - papers citing each seed paper,
  - new papers by the first and last authors of the seeds marked "closest",
published on or after the window start, removes what the project already
holds, and writes sweep.json and sweep.md into the run folder.

Standard library only. Queries are keywords from the profile; nothing else
from the project is sent. No contact address is sent to either service.

Known ceilings (ponytail):
  - The window uses publication dates, so a paper indexed late is caught only
    by the overlap (default 30 days before the last check). Raise --overlap-days
    after a long gap.
  - "Known" papers are recognised by DOI or arXiv id found in the --known
    files. A known paper listed without an identifier comes back as new.
  - Inside one sweep, two records with the same title of four or more words
    are taken as one paper (preprint and published version). Two different
    papers with an identical long title would be merged; shorter and non-Latin
    titles are never merged by title.
  - One query returns at most --pages x 50 records; a truncated query is
    flagged so the caller narrows it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

OPENALEX = "https://api.openalex.org"
ARXIV = "https://export.arxiv.org/api/query"
USER_AGENT = "topic-update-sweep/1.0"
PER_PAGE = 50
TIMEOUT_S = 30
PAUSE_S = 0.3
ATOM = "{http://www.w3.org/2005/Atom}"
SELECT = ("id,doi,title,publication_date,type,primary_location,"
          "authorships,abstract_inverted_index")

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>)\]}|,;]+", re.I)
ARXIV_RE = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])")
ARXIV_DOI_RE = re.compile(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", re.I)
MIN_TITLE_WORDS = 4
# Everything a request or a malformed answer can raise: URLError, HTTPError and
# TimeoutError are OSError; JSONDecodeError and UnicodeDecodeError are ValueError.
REQUEST_ERRORS = (OSError, http.client.HTTPException, ValueError, ET.ParseError)


class ProfileError(ValueError):
    """The watch profile is missing a field or holds a wrong value."""


# ---------- pure helpers -------------------------------------------------

def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def clean_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    match = DOI_RE.search(doi)
    return match.group(0).rstrip(".").lower() if match else None


def arxiv_id_of(text: str | None) -> str | None:
    if not text:
        return None
    from_doi = ARXIV_DOI_RE.search(text)
    if from_doi:
        return from_doi.group(1)
    match = ARXIV_RE.search(text)
    return match.group(1) if match else None


def extract_known_ids(text: str) -> set[str]:
    """DOIs and arXiv ids found anywhere in a project file."""
    dois = {clean_doi(m) for m in DOI_RE.findall(text)}
    arxiv = {f"arxiv:{m}" for m in ARXIV_RE.findall(text)}
    arxiv |= {f"arxiv:{m}" for m in ARXIV_DOI_RE.findall(text)}
    return {d for d in dois if d} | arxiv


def record_keys(record: dict[str, Any]) -> set[str]:
    keys = set(record.get("other_ids") or [])
    if record.get("doi"):
        keys.add(record["doi"])
    if record.get("arxiv_id"):
        keys.add(f"arxiv:{record['arxiv_id']}")
    return keys


def title_key(title: str) -> set[str]:
    """A key for merging by title, only for titles long enough to identify a paper."""
    normalized = normalize_title(title)
    return {f"title:{normalized}"} if len(normalized.split()) >= MIN_TITLE_WORDS else set()


def rebuild_abstract(inverted: dict[str, list[int]] | None) -> str:
    if not inverted:
        return ""
    words = sorted((pos, word) for word, places in inverted.items() for pos in places)
    return " ".join(word for _, word in words)


def window_start(profile: dict[str, Any], since: str | None, overlap_days: int) -> dt.date:
    if since:
        return parse_date(since, "--since")
    last = parse_date(profile["last_check"], "last_check")
    return last - dt.timedelta(days=overlap_days)


def parse_date(value: str, name: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ProfileError(f"{name} must be a date YYYY-MM-DD, got {value!r}") from exc


def validate_profile(profile: Any) -> dict[str, Any]:
    if not isinstance(profile, dict):
        raise ProfileError("the profile must be a JSON object")
    queries = profile.get("queries")
    if not isinstance(queries, list) or not queries:
        raise ProfileError("queries: at least one {id, text} entry is required")
    for query in queries:
        if not isinstance(query, dict) or not all(
                isinstance(query.get(k), str) and query[k].strip() for k in ("id", "text")):
            raise ProfileError(f"queries: each entry needs a text id and text, got {query!r}")
        if not re.findall(r"[\w-]+", query["text"]):
            raise ProfileError(f"queries: text holds no search word, got {query['text']!r}")
    seeds = profile.get("seeds", [])
    if not isinstance(seeds, list):
        raise ProfileError("seeds must be a list of {id, role} entries")
    for seed in seeds:
        seed_id = seed.get("id") if isinstance(seed, dict) else None
        if not isinstance(seed_id, str) or not (clean_doi(seed_id) or arxiv_id_of(seed_id)):
            raise ProfileError(f"seeds: id must be a DOI or an arXiv id, got {seed!r}")
    categories = profile.get("arxiv_categories", [])
    if not isinstance(categories, list) or not all(isinstance(c, str) for c in categories):
        raise ProfileError("arxiv_categories must be a list of names such as [\"cs.CR\"]")
    parse_date(profile.get("last_check"), "last_check")
    return profile


def merge_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One entry per paper: same DOI, same arXiv id or same normalised title."""
    merged: list[dict[str, Any]] = []
    index: dict[str, int] = {}
    for record in records:
        keys = record_keys(record) | title_key(record["title"])
        hit = next((index[k] for k in sorted(keys) if k in index), None)
        if hit is None:
            merged.append({**record, "found_by": list(record["found_by"])})
            hit = len(merged) - 1
        else:
            old = merged[hit]
            merged[hit] = {
                **old,
                "doi": old.get("doi") or record.get("doi"),
                "arxiv_id": old.get("arxiv_id") or record.get("arxiv_id"),
                "abstract": old.get("abstract") or record.get("abstract"),
                "other_ids": sorted(record_keys(old) | record_keys(record)),
                "found_by": sorted(set(old["found_by"]) | set(record["found_by"])),
            }
        for key in keys | record_keys(merged[hit]):
            index[key] = hit
    return merged


def drop_known(records: list[dict[str, Any]], known: set[str]) -> list[dict[str, Any]]:
    return [r for r in records if not (record_keys(r) & known)]


# ---------- parsing service answers --------------------------------------

def openalex_record(work: dict[str, Any], found_by: str) -> dict[str, Any]:
    doi = clean_doi(work.get("doi"))
    source = ((work.get("primary_location") or {}).get("source") or {})
    authors = [(a.get("author") or {}).get("display_name") for a in work.get("authorships") or []]
    return {
        "title": work.get("title") or "",
        "date": work.get("publication_date"),
        "doi": doi,
        "arxiv_id": (ARXIV_DOI_RE.search(doi or "") or [None, None])[1],
        "venue": source.get("display_name"),
        "type": work.get("type"),
        "authors": [a for a in authors if a],
        "abstract": rebuild_abstract(work.get("abstract_inverted_index")),
        "openalex_id": work.get("id"),
        "found_by": [found_by],
    }


def arxiv_records(xml_text: str, found_by: str, start: dt.date) -> list[dict[str, Any]]:
    records = []
    for entry in ET.fromstring(xml_text).iter(f"{ATOM}entry"):
        if "/api/errors" in (entry.findtext(f"{ATOM}id") or ""):
            raise ValueError(f"arXiv refused the query: {entry.findtext(f'{ATOM}summary')}")
        published = (entry.findtext(f"{ATOM}published") or "")[:10]
        if not published or dt.date.fromisoformat(published) < start:
            continue
        records.append({
            "title": " ".join((entry.findtext(f"{ATOM}title") or "").split()),
            "date": published,
            "doi": None,
            "arxiv_id": arxiv_id_of(entry.findtext(f"{ATOM}id")),
            "venue": "arXiv",
            "type": "preprint",
            "authors": [a.findtext(f"{ATOM}name") for a in entry.iter(f"{ATOM}author")],
            "abstract": " ".join((entry.findtext(f"{ATOM}summary") or "").split()),
            "openalex_id": None,
            "found_by": [found_by],
        })
    return records


# ---------- network ------------------------------------------------------

def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:  # noqa: S310 (fixed https hosts)
        return response.read().decode("utf-8", errors="replace")


def openalex_list(filters: str, label: str, pages: int, log: list, errors: list) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    failed = False
    for page in range(1, pages + 1):
        query = urllib.parse.urlencode({"filter": filters, "per-page": PER_PAGE, "page": page,
                                        "sort": "publication_date:desc", "select": SELECT})
        url = f"{OPENALEX}/works?{query}"
        try:
            results = json.loads(fetch(url)).get("results", [])
        except REQUEST_ERRORS as exc:
            errors.append({"source": "openalex", "query": label, "url": url, "error": repr(exc)})
            failed = True
            break
        records += [openalex_record(work, label) for work in results]
        time.sleep(PAUSE_S)
        if len(results) < PER_PAGE:
            break
    log.append({"source": "openalex", "query": label, "returned": len(records),
                "truncated": len(records) >= pages * PER_PAGE, "failed": failed})
    return records


def resolve_seed(seed_id: str, errors: list) -> dict[str, Any] | None:
    doi = clean_doi(seed_id) or f"10.48550/arxiv.{arxiv_id_of(seed_id)}"
    url = f"{OPENALEX}/works/doi:{urllib.parse.quote(doi, safe='/:.')}?select=id,title,authorships"
    try:
        work = json.loads(fetch(url))
        if not isinstance(work, dict) or not work.get("id"):
            raise ValueError("the answer names no work")
        return work
    except REQUEST_ERRORS as exc:
        errors.append({"source": "openalex", "query": f"seed {seed_id}", "url": url, "error": repr(exc)})
        return None
    finally:
        time.sleep(PAUSE_S)


def arxiv_search(text: str, categories: list[str], label: str, start: dt.date,
                 log: list, errors: list) -> list[dict[str, Any]]:
    terms = " AND ".join(f"all:{t}" for t in re.findall(r"[\w-]+", text))
    if categories:
        terms = f"({terms}) AND (" + " OR ".join(f"cat:{c}" for c in categories) + ")"
    query = urllib.parse.urlencode({"search_query": terms, "sortBy": "submittedDate",
                                    "sortOrder": "descending", "max_results": PER_PAGE})
    url = f"{ARXIV}?{query}"
    try:
        records = arxiv_records(fetch(url), label, start)
    except REQUEST_ERRORS as exc:
        errors.append({"source": "arxiv", "query": label, "url": url, "error": repr(exc)})
        log.append({"source": "arxiv", "query": label, "returned": 0, "truncated": False, "failed": True})
        return []
    finally:
        time.sleep(3)  # arXiv asks for one request every three seconds
    log.append({"source": "arxiv", "query": label, "returned": len(records),
                "truncated": len(records) >= PER_PAGE, "failed": False})
    return records


# ---------- the sweep ----------------------------------------------------

def watched_authors(work: dict[str, Any]) -> list[str]:
    authorships = work.get("authorships") or []
    ends = [authorships[0], authorships[-1]] if authorships else []
    ids = [(a.get("author") or {}).get("id") for a in ends]
    return sorted({i.rsplit("/", 1)[-1] for i in ids if i})


def run_sweep(profile: dict[str, Any], start: dt.date, pages: int) -> dict[str, Any]:
    log: list = []
    errors: list = []
    found: list = []
    since = f"from_publication_date:{start.isoformat()}"
    for query in profile["queries"]:
        label = f"query:{query['id']}"
        search = query["text"].replace(",", " ")
        found += openalex_list(f"title_and_abstract.search:{search},{since}", label, pages, log, errors)
        found += arxiv_search(query["text"], profile.get("arxiv_categories", []), label, start, log, errors)
    for seed in profile.get("seeds", []):
        work = resolve_seed(seed["id"], errors)
        if not work:
            continue
        short_id = work["id"].rsplit("/", 1)[-1]
        found += openalex_list(f"cites:{short_id},{since}", f"cites:{seed['id']}", pages, log, errors)
        if seed.get("role") == "closest" and watched_authors(work):
            authors = "|".join(watched_authors(work))
            found += openalex_list(f"authorships.author.id:{authors},{since}",
                                   f"authors-of:{seed['id']}", pages, log, errors)
    return {"log": log, "errors": errors, "found": found}


def summary_md(result: dict[str, Any]) -> str:
    lines = [f"# Sweep {result['run_date']} (window from {result['window_start']})", "",
             "| Source | Query | Returned | Truncated |", "|---|---|---|---|"]
    lines += [f"| {q['source']} | {q['query']} | {'FAILED' if q['failed'] else q['returned']} | "
              f"{'yes' if q['truncated'] else 'no'} |" for q in result["queries"]]
    lines += ["", f"Errors: {len(result['errors'])} (a failed request is no answer, not zero results)"]
    lines += [f"- {e['source']} {e['query']}: {e['error']}" for e in result["errors"]]
    lines += ["", f"New records after removing known papers: {len(result['records'])}", ""]
    lines += [f"- {r['date']} | {r['title']} | {r['doi'] or r['arxiv_id'] or 'no id'} | "
              f"{', '.join(r['found_by'])}" for r in result["records"]]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="run folder")
    parser.add_argument("--known", nargs="*", default=[], type=Path,
                        help="project files whose DOIs and arXiv ids are already held")
    parser.add_argument("--since", help="window start YYYY-MM-DD (default: last_check minus overlap)")
    parser.add_argument("--overlap-days", type=int, default=30)
    parser.add_argument("--pages", type=int, default=2, choices=range(1, 5))
    args = parser.parse_args(argv)
    try:
        profile = validate_profile(json.loads(args.profile.read_text(encoding="utf-8")))
        start = window_start(profile, args.since, args.overlap_days)
        known = set().union(*(extract_known_ids(p.read_text(encoding="utf-8", errors="replace"))
                              for p in args.known))
    except (OSError, ValueError, OverflowError) as exc:
        print(f"sweep: cannot start: {exc}", file=sys.stderr)
        return 2
    swept = run_sweep(profile, start, args.pages)
    records = drop_known(merge_records(swept["found"]), known)
    result = {"run_date": dt.date.today().isoformat(), "window_start": start.isoformat(),
              "queries": swept["log"], "errors": swept["errors"],
              "records": sorted(records, key=lambda r: r["date"] or "", reverse=True)}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "sweep.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.out / "sweep.md").write_text(summary_md(result), encoding="utf-8")
    print(f"sweep: {len(result['records'])} new records, {len(result['errors'])} failed requests -> {args.out}")
    return 1 if swept["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())

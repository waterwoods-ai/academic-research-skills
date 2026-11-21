#!/usr/bin/env python3
"""Elicit API v2 client for the topic skills (find-, verify- and update-research-topic). Standard library only.

Commands:
  check                          verify ELICIT_API_KEY and print the account's usage
  search QUERY [-n N] [--min-year Y] [--max-year Y] [--since YYYY-MM-DD] [--has-pdf]
               [--include WORD]... [--exclude WORD]... [--keyword-mode] [-o FILE]
                                 paper search: numbered summary to stdout, full JSON to FILE

The key is read from the environment and never printed. QUERY is sent to Elicit: keywords only,
never unpublished claim or draft text. Exit codes: 0 ok, 1 the request failed, 2 it could not start.
Request shapes follow https://docs.elicit.com (GET /usage, POST /search/papers), read 2026-11-21.
"""
from __future__ import annotations

import argparse
import datetime as dt
import http.client
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://elicit.com/api/v2"
USER_AGENT = "topic-skills-elicit/1.0"  # urllib's default user agent is blocked by some CDNs
PLAN_CAP = 300  # results per search on the Pro plan; a higher plan allows more, the API refuses beyond its cap
HINTS = {
    401: "key missing, invalid, revoked or expired",
    402: "plan quota exhausted",
    403: "the API needs an Elicit Pro plan or above",
    409: "usage reporting is not available for this account",
    429: "rate limited: the IP is blocked for 5 minutes, wait before retrying",
}


class ElicitError(Exception):
    """A request that got no usable answer. Never a reason to report zero results."""


def ssl_context() -> ssl.SSLContext:
    try:  # some Python builds ship without a CA bundle; certifi supplies one when installed
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def error_detail(raw: str) -> str:
    """The message of Elicit's error body, which is nested for most codes and flat for 429."""
    try:
        body = json.loads(raw)
    except ValueError:
        return raw[:200]
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or "")
    return str(body.get("message") or error or "") if isinstance(body, dict) else raw[:200]


def api(method: str, path: str, body: dict | None = None) -> dict:
    key = os.environ.get("ELICIT_API_KEY")
    if not key:
        raise ElicitError("ELICIT_API_KEY is not set (create a key at https://elicit.com/settings; Pro plan or above)")
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(BASE_URL + path, method=method, data=data, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, context=ssl_context(), timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = error_detail(e.read().decode("utf-8", errors="replace"))
        hint = f" ({HINTS[e.code]})" if e.code in HINTS else ""
        raise ElicitError(f"Elicit API error {e.code}{hint}: {detail}") from e
    except (OSError, http.client.HTTPException, ValueError) as e:
        raise ElicitError(f"no answer from Elicit: {getattr(e, 'reason', e)}") from e


def epoch_seconds(day: str) -> int:
    return int(dt.datetime.fromisoformat(day).replace(tzinfo=dt.timezone.utc).timestamp())


def search_body(args: argparse.Namespace) -> dict:
    """The POST /search/papers body. Keyword mode and filters cannot be mixed: the API answers 400."""
    filters = {
        "minYear": args.min_year, "maxYear": args.max_year,
        "minEpochS": epoch_seconds(args.since) if args.since else None,
        "hasPdf": True if args.has_pdf else None,
        "includeKeywords": args.include or None, "excludeKeywords": args.exclude or None,
    }
    filters = {name: value for name, value in filters.items() if value is not None}
    if args.keyword_mode and filters:
        raise ValueError("--keyword-mode cannot be combined with filters")
    if not 1 <= args.n <= PLAN_CAP:
        raise ValueError(f"-n must be between 1 and {PLAN_CAP}")
    if not args.query.strip():
        raise ValueError("the query is empty")
    body = {"query": args.query, "maxResults": args.n, "searchMode": "keyword" if args.keyword_mode else "semantic"}
    return {**body, "filters": filters} if filters else body


def summary_line(number: int, paper: dict) -> str:
    authors = paper.get("authors") or []
    who = f"{authors[0]} et al." if len(authors) > 1 else (authors[0] if authors else "?")
    return (f"{number:>3}. {paper.get('title') or '(no title)'} | {who} | {paper.get('year') or '?'} | "
            f"{paper.get('venue') or '-'} | cited {paper.get('citedByCount') or 0} | {paper.get('doi') or 'no DOI'}")


def cmd_check(_: argparse.Namespace) -> int:
    print(json.dumps(api("GET", "/usage"), indent=2))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    body = search_body(args)
    answer = api("POST", "/search/papers", body)
    papers = answer.get("papers")
    if not isinstance(papers, list):
        raise ElicitError("the answer holds no list of papers")
    for warning in answer.get("warnings") or []:
        print(f"warning from Elicit: {warning.get('message')}", file=sys.stderr)
    if args.o:
        saved = {"query": args.query, "filters": body.get("filters", {}), "searched_on": dt.date.today().isoformat(),
                 "papers": papers, "warnings": answer.get("warnings") or []}
        Path(args.o).write_text(json.dumps(saved, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(papers)} papers for: {args.query}")
    for number, paper in enumerate(papers, 1):
        print(summary_line(number, paper))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check").set_defaults(run=cmd_check)
    search = commands.add_parser("search")
    search.add_argument("query")
    search.add_argument("-n", type=int, default=25, help="maximum results (default 25)")
    search.add_argument("--min-year", type=int)
    search.add_argument("--max-year", type=int)
    search.add_argument("--since", help="only papers published on or after YYYY-MM-DD")
    search.add_argument("--has-pdf", action="store_true", help="only papers with an available PDF")
    search.add_argument("--include", action="append", help="keyword that must appear (repeatable)")
    search.add_argument("--exclude", action="append", help="keyword that must not appear (repeatable)")
    search.add_argument("--keyword-mode", action="store_true", help="keyword search instead of semantic; no filters")
    search.add_argument("-o", help="write the full JSON results here")
    search.set_defaults(run=cmd_search)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.run(args)
    except ValueError as e:
        print(f"cannot start: {e}", file=sys.stderr)
        return 2
    except ElicitError as e:
        print(f"FAILED, not zero results: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"cannot write the output: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

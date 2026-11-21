"""Offline checks for sweep.py: no network."""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import sweep  # noqa: E402

ATOM_FEED = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry><id>http://arxiv.org/abs/2611.01234v2</id><published>2026-11-02T10:00:00Z</published>
    <title>A New
      Attack</title><summary>We show.</summary><author><name>A. One</name></author></entry>
  <entry><id>http://arxiv.org/abs/2601.00001v1</id><published>2026-01-05T10:00:00Z</published>
    <title>Old</title><summary>Old.</summary><author><name>B. Two</name></author></entry>
</feed>"""


def rec(title, doi=None, arxiv_id=None, found_by="q"):
    return {"title": title, "doi": doi, "arxiv_id": arxiv_id, "abstract": "", "date": "2026-11-01",
            "found_by": [found_by]}


def test_known_ids_cover_doi_and_arxiv_forms():
    text = "see https://doi.org/10.1145/3576915.3623123, arXiv:2501.01234v3 and 10.48550/arXiv.2402.00001."
    assert sweep.extract_known_ids(text) == {
        "10.1145/3576915.3623123", "arxiv:2501.01234", "10.48550/arxiv.2402.00001", "arxiv:2402.00001"}


def test_preprint_and_published_version_merge_and_known_is_dropped():
    merged = sweep.merge_records([
        rec("Confused Deputies: A Study of Bridges", arxiv_id="2501.01234", found_by="query:core"),
        rec("Confused deputies - a study of bridges", doi="10.1145/1.2", found_by="cites:x"),
        rec("Something Else", doi="10.1/zz"),
    ])
    assert len(merged) == 2
    assert merged[0]["doi"] == "10.1145/1.2" and merged[0]["arxiv_id"] == "2501.01234"
    assert merged[0]["found_by"] == ["cites:x", "query:core"]
    assert [r["title"] for r in sweep.drop_known(merged, {"arxiv:2501.01234"})] == ["Something Else"]


def test_arxiv_feed_keeps_only_the_window():
    records = sweep.arxiv_records(ATOM_FEED, "query:core", dt.date(2026, 10, 1))
    assert [(r["arxiv_id"], r["title"]) for r in records] == [("2611.01234", "A New Attack")]


def test_openalex_record_rebuilds_abstract_and_maps_arxiv_doi():
    work = {"id": "https://openalex.org/W1", "doi": "https://doi.org/10.48550/arXiv.2611.00009",
            "title": "T", "publication_date": "2026-11-03", "type": "preprint",
            "abstract_inverted_index": {"world": [1], "hello": [0]},
            "authorships": [{"author": {"display_name": "A"}}]}
    record = sweep.openalex_record(work, "q")
    assert (record["abstract"], record["arxiv_id"], record["authors"]) == ("hello world", "2611.00009", ["A"])


def test_window_overlaps_the_last_check():
    profile = {"last_check": "2026-10-31"}
    assert sweep.window_start(profile, None, 30) == dt.date(2026, 10, 1)
    assert sweep.window_start(profile, "2026-06-01", 30) == dt.date(2026, 6, 1)


@pytest.mark.parametrize("profile", [
    [], {"queries": [], "last_check": "2026-10-01"},
    {"queries": [{"id": "a", "text": "x"}], "last_check": "last week"},
    {"queries": [{"id": "a", "text": "x"}], "seeds": [{"id": "not an id"}], "last_check": "2026-10-01"},
    {"queries": [{"id": "a", "text": "x"}], "seeds": [{"id": 123}], "last_check": "2026-10-01"},
    {"queries": [{"id": "a", "text": 5}], "last_check": "2026-10-01"},
    {"queries": [{"id": "a", "text": "!!!"}], "last_check": "2026-10-01"},
    {"queries": [{"id": "a", "text": "x"}], "arxiv_categories": "cs.CR", "last_check": "2026-10-01"},
])
def test_bad_profiles_are_refused(profile):
    with pytest.raises(sweep.ProfileError):
        sweep.validate_profile(profile)


def test_watched_authors_are_first_and_last():
    work = {"authorships": [{"author": {"id": "https://openalex.org/A1"}},
                            {"author": {"id": "https://openalex.org/A2"}},
                            {"author": {"id": "https://openalex.org/A3"}}]}
    assert sweep.watched_authors(work) == ["A1", "A3"]


@pytest.mark.parametrize("titles", [("机器学习安全", "对抗样本"), ("Erratum", "Erratum"), ("", "")])
def test_short_or_non_latin_titles_never_merge_so_a_new_paper_survives(titles):
    merged = sweep.merge_records([rec(titles[0], doi="10.1/known"), rec(titles[1], doi="10.1/new")])
    assert [r["doi"] for r in sweep.drop_known(merged, {"10.1/known"})] == ["10.1/new"]


def test_a_doi_with_arxiv_like_digits_gives_no_arxiv_id():
    work = {"doi": "https://doi.org/10.1007/978-3-031-1234.5678", "title": "T"}
    assert sweep.openalex_record(work, "q")["arxiv_id"] is None


def test_arxiv_error_feed_is_an_error_not_zero_results():
    feed = ATOM_FEED.replace("http://arxiv.org/abs/2611.01234v2", "http://arxiv.org/api/errors#bad")
    with pytest.raises(ValueError):
        sweep.arxiv_records(feed, "q", dt.date(2026, 1, 1))


def write_profile(tmp_path):
    profile = tmp_path / "topic_watch.json"
    profile.write_text('{"queries": [{"id": "a", "text": "x y"}], "last_check": "2026-10-01"}')
    return profile


def test_every_request_failing_is_exit_1_and_marked_failed(tmp_path, monkeypatch):
    def down(url):
        raise ConnectionResetError("down")
    monkeypatch.setattr(sweep, "fetch", down)
    monkeypatch.setattr(sweep.time, "sleep", lambda s: None)
    out = tmp_path / "run"
    assert sweep.main(["--profile", str(write_profile(tmp_path)), "--out", str(out)]) == 1
    assert (out / "sweep.md").read_text().count("FAILED") == 2


def test_unreadable_known_file_and_bad_profile_do_not_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(sweep, "fetch", lambda url: '{"results": []}' if "openalex" in url else "<feed/>")
    monkeypatch.setattr(sweep.time, "sleep", lambda s: None)
    known = tmp_path / "refs.bib"
    known.write_bytes("caf\xe9 10.1/abc".encode("latin-1"))
    args = ["--profile", str(write_profile(tmp_path)), "--out", str(tmp_path / "run")]
    assert sweep.main(args + ["--known", str(known)]) == 0
    assert sweep.main(args + ["--overlap-days", "999999999"]) == 2

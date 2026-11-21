"""Offline checks for elicit_api.py: no network, no key."""
from __future__ import annotations

import io
import json
import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import elicit_api  # noqa: E402

PAPER = {"title": "A Study", "authors": ["A. One", "B. Two"], "year": 2026, "venue": "NDSS",
         "citedByCount": 3, "doi": "10.1/x"}


def args(*argv):
    return elicit_api.build_parser().parse_args(["search", *argv])


def test_search_body_carries_only_the_filters_given():
    body = elicit_api.search_body(args("tool poisoning", "-n", "40", "--since", "2026-10-01", "--exclude", "survey"))
    assert body == {"query": "tool poisoning", "maxResults": 40, "searchMode": "semantic",
                    "filters": {"minEpochS": 1790812800, "excludeKeywords": ["survey"]}}
    assert "filters" not in elicit_api.search_body(args("tool poisoning"))


@pytest.mark.parametrize("argv", [("q", "--keyword-mode", "--min-year", "2024"), ("q", "-n", "0"),
                                  ("q", "-n", "301"), ("  ",), ("q", "--since", "last week")])
def test_bad_requests_are_refused_before_any_call(argv, monkeypatch):
    monkeypatch.setattr(elicit_api, "api", lambda *a, **k: pytest.fail("a request was sent"))
    assert elicit_api.main(["search", *argv]) == 2


def test_search_prints_a_summary_and_saves_the_full_answer(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(elicit_api, "api", lambda method, path, body=None: {"papers": [PAPER], "warnings": []})
    out = tmp_path / "q.json"
    assert elicit_api.main(["search", "tool poisoning", "-o", str(out)]) == 0
    assert "  1. A Study | A. One et al. | 2026 | NDSS | cited 3 | 10.1/x" in capsys.readouterr().out
    assert json.loads(out.read_text())["papers"] == [PAPER]


def test_a_failed_request_is_exit_1_and_never_zero_results(monkeypatch, capsys):
    def blocked(request, **kwargs):
        body = io.BytesIO(b'{"error":"Rate limit exceeded","message":"Too many requests."}')
        raise urllib.error.HTTPError(request.full_url, 429, "Too Many Requests", None, body)
    monkeypatch.setenv("ELICIT_API_KEY", "test-value")
    monkeypatch.setattr(elicit_api.urllib.request, "urlopen", blocked)
    assert elicit_api.main(["search", "tool poisoning"]) == 1
    err = capsys.readouterr().err
    assert "429" in err and "not zero results" in err and "test-value" not in err


def test_missing_key_and_malformed_answer_fail(monkeypatch):
    monkeypatch.delenv("ELICIT_API_KEY", raising=False)
    assert elicit_api.main(["check"]) == 1
    monkeypatch.setattr(elicit_api, "api", lambda *a, **k: {"unexpected": True})
    assert elicit_api.main(["search", "q"]) == 1

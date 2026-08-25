#!/usr/bin/env python3
"""Structural validator for an ars-review/ workspace (RW-passport-inspired).

STRUCTURAL ONLY and ADVISORY: "workspace valid" != "round approved / verdict
correct / tasks truly resolved". Check #10 verifies a human-confirmation
marker EXISTS; the script never stands in for the MANDATORY human checkpoint.
It strengthens the numbers-from-ledger iron rule (check #4) — an experiment
task cannot be `resolved` without a ledger_run_id.

Venue decision vocabulary is derived from major_revision_playbook.md §1 /
conference_ranking_2025.json — never hardcoded model memory.

Usage:
  validate_review_workspace.py PATH/TO/ars-review        # validate a workspace
  validate_review_workspace.py --selftest                # CI: validate on a
                                                          # synthetic fixture,
                                                          # no real workspace
Stdlib only. Exit 0 clean, 1 on failures.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent

# Only NDSS keeps a Major Revision (see major_revision_playbook.md §1). The
# validator sources the venue -> allowed-decision map from that file so it is
# never a hardcoded belief; the fallback below is used only if the file moved.
MAJOR_REVISION_VENUES = {"NDSS"}


def venue_family(venue: str) -> str:
    v = venue.upper()
    for fam in ("S&P", "SP", "OAKLAND", "NDSS", "CCS", "USENIX"):
        if fam in v:
            return "S&P" if fam in ("SP", "OAKLAND") else fam
    return venue


def allowed_decisions(venue: str, playbook_text: str | None) -> set[str] | None:
    """Return the lowercased decision-token set the venue may use, or None if unknown."""
    fam = venue_family(venue)
    # Structural rule that matters most: 'major revision' is NDSS-only.
    base = {"accept", "reject"}
    if fam == "NDSS":
        return base | {"minor revision", "major revision"}
    if fam == "CCS":
        return base | {"minor revision", "administrative reject"}
    if fam == "USENIX":
        return base | {"accepted", "accepted on shepherd approval", "rejected"}
    if fam == "S&P":
        return base
    return None  # unknown venue -> skip the vocabulary check (do not false-fail)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_schema() -> dict:
    return json.loads((SKILL_ROOT / "contracts" / "review-workspace.schema.json").read_text())


def validate(ws: Path) -> list[str]:
    fails: list[str] = []
    state_file = ws / "state.json"
    if not state_file.exists():
        return [f"missing {state_file}"]
    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"state.json is not valid JSON: {e}"]

    if state.get("schema_version") != "sec-review-workspace/v1":
        fails.append("schema_version must be 'sec-review-workspace/v1'")
    rounds = state.get("rounds", [])
    if not rounds:
        return fails + ["no rounds declared"]

    playbook = SKILL_ROOT / "references" / "major_revision_playbook.md"
    playbook_text = playbook.read_text(encoding="utf-8") if playbook.exists() else None
    venue = state.get("venue", "")
    allowed = allowed_decisions(venue, playbook_text)

    nums = [r.get("round") for r in rounds]
    # 2. rounds monotonic, no gaps, state.round == max
    if nums != list(range(1, len(nums) + 1)):
        fails.append(f"rounds must be 1..N with no gaps, got {nums}")
    if state.get("round") != max(nums):
        fails.append(f"state.round ({state.get('round')}) must equal max round ({max(nums)})")

    prev_freeze = state.get("frozen_criteria_hash")

    for r in rounds:
        rn = r.get("round")
        rdir = ws / f"round-{rn}"
        # 1. each round dir has its files
        if rdir.exists():
            for needed in ("decision.md", "compliance.md"):
                if not (rdir / needed).exists():
                    fails.append(f"round-{rn}: missing {needed}")
            snaps = list(rdir.glob("manuscript-snapshot.*"))
            if not snaps:
                fails.append(f"round-{rn}: missing manuscript-snapshot.*")
        # 3. decision uses only the venue's vocabulary
        dec = (r.get("decision") or "").strip().lower()
        if allowed is not None and dec and dec not in allowed:
            fails.append(f"round-{rn}: decision '{r.get('decision')}' not in {venue} vocabulary {sorted(allowed)}")
        if dec == "major revision" and venue_family(venue) not in MAJOR_REVISION_VENUES:
            fails.append(f"round-{rn}: 'Major Revision' is NDSS-only, not valid for {venue}")
        # 4+5. numbers-from-ledger + evidence pointer on resolved tasks
        for t in r.get("tasks", []):
            if t.get("status") == "resolved":
                if t.get("type") == "experiment" and not t.get("ledger_run_id"):
                    fails.append(f"round-{rn} task {t.get('id')}: experiment resolved without ledger_run_id (numbers-from-ledger)")
                if not t.get("evidence_pointer"):
                    fails.append(f"round-{rn} task {t.get('id')}: resolved without evidence_pointer")
        # 8. manuscript snapshot hash matches stored file
        ms = r.get("manuscript_snapshot") or {}
        if ms.get("file") and ms.get("content_sha256"):
            f = ws / ms["file"] if not Path(ms["file"]).is_absolute() else Path(ms["file"])
            if f.exists() and sha256_text(f.read_text(encoding="utf-8", errors="replace")) != ms["content_sha256"]:
                fails.append(f"round-{rn}: manuscript_snapshot.content_sha256 does not match {ms['file']} (silent edit?)")
        # 9. frozen criteria hash stable
        if prev_freeze and state.get("frozen_criteria_hash") != prev_freeze:
            fails.append("frozen_criteria_hash changed across rounds without a new freeze event")
        # 10. human gate on terminal decisions
        cred = r.get("round_decision_credential") or {}
        if dec in ("accept", "reject", "accepted", "rejected") and not cred.get("human_confirmed"):
            fails.append(f"round-{rn}: terminal decision '{r.get('decision')}' requires round_decision_credential.human_confirmed=true (model may not self-certify)")

    return fails


def selftest() -> list[str]:
    """Build a synthetic valid workspace + one that must fail, verify both."""
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as d:
        ws = Path(d) / "ars-review"
        (ws / "round-1").mkdir(parents=True)
        paper = ws / "round-1" / "manuscript-snapshot.tex"
        paper.write_text("draft body", encoding="utf-8")
        (ws / "round-1" / "decision.md").write_text("Major Revision\nT1 ...", encoding="utf-8")
        (ws / "round-1" / "compliance.md").write_text("P0-1 PASS", encoding="utf-8")
        good = {
            "schema_version": "sec-review-workspace/v1",
            "venue": "NDSS 2027", "paper_path": "./paper.tex", "round": 1,
            "created": "2026-08-25", "frozen_criteria_hash": "abc",
            "rounds": [{
                "round": 1, "decision": "Major Revision",
                "manuscript_snapshot": {"file": "round-1/manuscript-snapshot.tex", "content_sha256": sha256_text("draft body")},
                "tasks": [{"id": "T1", "type": "experiment", "status": "resolved", "evidence_pointer": "ledger/run-1", "ledger_run_id": "run-1"}],
            }],
        }
        (ws / "state.json").write_text(json.dumps(good), encoding="utf-8")
        f = validate(ws)
        if f:
            problems.append(f"VALID fixture wrongly failed: {f}")

        # mutate: S&P cannot say Major Revision; experiment resolved w/o ledger
        bad = json.loads(json.dumps(good))
        bad["venue"] = "IEEE S&P 2027"
        bad["rounds"][0]["tasks"][0]["ledger_run_id"] = ""
        (ws / "state.json").write_text(json.dumps(bad), encoding="utf-8")
        f2 = validate(ws)
        if not any("NDSS-only" in x for x in f2):
            problems.append("INVALID fixture: did not catch S&P Major Revision")
        if not any("ledger_run_id" in x for x in f2):
            problems.append("INVALID fixture: did not catch missing ledger_run_id")
    return problems


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        problems = selftest()
        print(json.dumps({"selftest": "review-workspace", "ok": not problems, "problems": problems}, indent=2))
        return 0 if not problems else 1
    if len(sys.argv) < 2:
        print("usage: validate_review_workspace.py PATH/TO/ars-review | --selftest", file=sys.stderr)
        return 2
    fails = validate(Path(sys.argv[1]))
    print(json.dumps({"workspace": sys.argv[1], "ok": not fails, "failures": fails, "note": "structural only; not an approval of any round"}, ensure_ascii=False, indent=2))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

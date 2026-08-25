#!/usr/bin/env python3
"""Static linter for the security-track overlay (RW-inspired self_check layer 1+2).

Proves the overlay's routing + behavior scenarios are well-formed and
self-consistent on disk. It CANNOT prove a signal actually fires at runtime —
that stays the manual paste-into-a-fresh-session check in baseline_scenarios.md.

Checks:
 1. every scenario's expected_ref exists under references/
 2. every expected_signal literally appears in its expected_ref file
 3. every reference named in the SKILL.md routing table exists on disk
 4. every references/*.md is named by the routing table OR >=1 scenario (no orphans)
 5. coverage floors: >=7 scenarios, >=1 trap, one scenario per routed protocol file
 6. per-scenario structural well-formedness (required fields, non-empty)
 7. path-hygiene: no personal absolute paths (/Users/, ~/.claude, /home/) in any
    security-track file — both forks sync from upstream and must stay portable

Output contract: prints failures; exit 0 if clean, 1 otherwise.
Stdlib only; run from the security-track dir or pass it as argv[1].
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Personal filesystem paths that must not be hardcoded (fork portability).
# Matched as real path prefixes, NOT as URL path segments (e.g. a CFP link
# "https://host/home/index.html") and NOT inside this linter's own docstring.
# /Users/ and /home/ are always forbidden (a hardcoded machine path is never
# legitimate). ~/.claude and ~/.codex are legitimate in user-facing docs
# (README/HOWTO tell the user to run e.g. `rm -rf ~/.codex/plugins/...`), so
# they are only forbidden outside doc files.
HYGIENE_ABS = re.compile(r"(?<![:\w])(?:/Users/|/home/[a-z])")
HYGIENE_TILDE = re.compile(r"~/\.(?:claude|codex)")
HYGIENE_DOC_FILES = {"README.md", "HOWTO.md"}
HYGIENE_SELF_EXEMPT = "check_behavior_scenarios.py"
# references that are data/generated, not routed protocol prose — exempt from orphan/floor rules
NON_PROTOCOL_REFS = {
    "deadlines_current.md",       # generated calendar
    "conference_ranking_2025.json",
    "knowledge_index.jsonl",      # canonical data store, rendered by knowledge_index.md
}


def load_routing_refs(skill_md: Path) -> set[str]:
    """Reference filenames named anywhere in SKILL.md (routing table + prose)."""
    text = skill_md.read_text(encoding="utf-8")
    return set(re.findall(r"references/([A-Za-z0-9_./-]+\.(?:md|json|jsonl))", text))


def check(root: Path) -> list[str]:
    fails: list[str] = []
    refs_dir = root / "references"
    skill_md = root / "SKILL.md"
    scen_file = root / "tests" / "behavior_scenarios.json"

    for required in (refs_dir, skill_md, scen_file):
        if not required.exists():
            return [f"missing required path: {required.relative_to(root)}"]

    scenarios = json.loads(scen_file.read_text(encoding="utf-8")).get("scenarios", [])
    routed = load_routing_refs(skill_md)

    # 6. per-scenario well-formedness + 1/2 ref+signal
    required_fields = ("id", "prompt", "must_do", "must_not", "expected_ref", "expected_signal")
    scenario_refs: set[str] = set()
    for s in scenarios:
        sid = s.get("id", "<no-id>")
        for f in required_fields:
            if not s.get(f):
                fails.append(f"scenario {sid}: missing/empty field '{f}'")
        ref = s.get("expected_ref", "")
        sig = s.get("expected_signal", "")
        ref_path = root / ref
        if ref and not ref_path.exists():
            fails.append(f"scenario {sid}: expected_ref does not exist: {ref}")
        elif ref and sig and sig not in ref_path.read_text(encoding="utf-8"):
            fails.append(f"scenario {sid}: expected_signal '{sig}' not found in {ref}")
        if ref.startswith("references/"):
            scenario_refs.add(ref.split("/", 1)[1])

    # 3. every routed reference exists on disk
    for r in sorted(routed):
        if not (refs_dir / r).exists():
            fails.append(f"routing table names references/{r} but it is missing on disk")

    # 4. orphan protocol refs (present on disk, named nowhere)
    on_disk = {p.name for p in refs_dir.iterdir() if p.is_file()}
    for r in sorted(on_disk):
        if r in NON_PROTOCOL_REFS:
            continue
        if r not in routed and r not in scenario_refs:
            fails.append(f"orphan reference references/{r}: not in routing table and no scenario covers it")

    # 5. coverage floors
    if len(scenarios) < 7:
        fails.append(f"coverage floor: >=7 scenarios required, found {len(scenarios)}")
    if not any(s.get("trap") for s in scenarios):
        fails.append("coverage floor: >=1 trap/negative scenario required")

    # 7. path hygiene across every security-track file
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix in (".pyc",):
            continue
        if path.name == HYGIENE_SELF_EXEMPT:  # this linter documents the patterns it forbids
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        m = HYGIENE_ABS.search(text)
        if not m and path.name not in HYGIENE_DOC_FILES:
            m = HYGIENE_TILDE.search(text)
        if m:
            fails.append(f"path-hygiene: personal path '{m.group()}' found in {path.relative_to(root)}")

    return fails


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    fails = check(root)
    result = {"skill": "security-track", "ok": not fails, "failures": fails}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

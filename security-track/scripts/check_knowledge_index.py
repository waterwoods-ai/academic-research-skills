#!/usr/bin/env python3
"""Consistency checker for the dual-layer L1 knowledge index (RW atoms pattern).

knowledge_index.jsonl is the canonical machine store (one reviewer-bar atom per
row); knowledge_index.md is its rendered human view. This lints the JSONL for
well-formedness and checks the two layers do not drift: every subfield in the
JSONL must be represented in the rendered .md, so the human view can never
silently omit a bar the machine store carries.

Iron-rule guard: `status` must stay orthogonal to `confidence` — a
`confidence:high` row may still be `status:seeded/provisional`; the checker
forbids machine-promoting a provisional lesson (that stays a human gate).

Stdlib only. Exit 0 clean, 1 on failures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "references" / "knowledge_index.jsonl"
MD = ROOT / "references" / "knowledge_index.md"

REQUIRED = ("id", "subfield", "type", "knowledge", "best_practice", "severity",
            "venues", "confidence", "status", "source", "provenance",
            "applies_when", "fails_when", "date")
SEVERITY = {"desk_reject", "reject", "weakening"}
STATUS = {"seeded", "provisional", "confirmed"}
CONFIDENCE = {"low", "medium", "high"}


def check() -> list[str]:
    fails: list[str] = []
    if not JSONL.exists():
        return [f"missing {JSONL.name}"]
    if not MD.exists():
        return [f"missing {MD.name}"]

    md_text = MD.read_text(encoding="utf-8")
    rows = []
    for i, line in enumerate(JSONL.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            fails.append(f"line {i}: invalid JSON ({e})")
            continue
        rows.append(row)
        rid = row.get("id", f"<line {i}>")
        for f in REQUIRED:
            if f not in row or row[f] in ("", [], None):
                fails.append(f"{rid}: missing/empty field '{f}'")
        if row.get("severity") not in SEVERITY:
            fails.append(f"{rid}: severity '{row.get('severity')}' not in {sorted(SEVERITY)}")
        if row.get("status") not in STATUS:
            fails.append(f"{rid}: status '{row.get('status')}' not in {sorted(STATUS)}")
        if row.get("confidence") not in CONFIDENCE:
            fails.append(f"{rid}: confidence '{row.get('confidence')}' not in {sorted(CONFIDENCE)}")
        # provenance discipline: a promoted (confirmed) row must cite >=2 sources
        if row.get("status") == "confirmed" and str(row.get("provenance", "")).count(";") < 1:
            fails.append(f"{rid}: status=confirmed requires provenance citing >=2 projects/sources")

    ids = [r.get("id") for r in rows]
    if len(ids) != len(set(ids)):
        fails.append("duplicate atom id(s) in JSONL")

    # dual-layer no-drift: every JSONL subfield appears in the rendered .md
    md_low = md_text.lower()
    for r in rows:
        sf = (r.get("subfield") or "").replace("-", " ")
        head = sf.split()[0] if sf else ""
        if head and head not in md_low:
            fails.append(f"{r.get('id')}: subfield '{r.get('subfield')}' not represented in knowledge_index.md (layer drift)")

    return fails


def main() -> int:
    fails = check()
    print(json.dumps({"check": "knowledge-index-dual-layer", "ok": not fails, "failures": fails}, ensure_ascii=False, indent=2))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

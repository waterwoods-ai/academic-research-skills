#!/usr/bin/env bash
# security-track fork-owned check runner (local + sync-upstream hook).
#
# Not a GitHub Actions workflow: pushing to .github/workflows/ requires an
# OAuth `workflow` scope this fork's token lacks. Instead this script runs the
# three static checks manually and is wired into the `git sync-upstream` alias,
# so every upstream sync re-verifies the overlay. Run from anywhere.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"   # security-track/
fail=0
run() { echo "== $1"; python3 "$here/$2" ${3:-} || fail=1; }

run "behavior scenarios + routing linter" "tests/check_behavior_scenarios.py"
run "review-workspace validator (selftest)" "scripts/validate_review_workspace.py" "--selftest"
run "knowledge-index dual-layer consistency" "scripts/check_knowledge_index.py"

if [ "$fail" -ne 0 ]; then echo "SECURITY-TRACK CHECKS FAILED"; exit 1; fi
echo "security-track checks: all green"

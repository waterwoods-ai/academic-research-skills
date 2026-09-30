#!/usr/bin/env bash
# Claude fork only; run after every upstream sync (takes a few minutes).
#
# Runs every upstream lint (scripts/check_*.py) twice: on pure upstream (a
# temporary worktree of `main`) and on this tree. Lints whose result differs
# are caused by this fork's additions. The ones listed in
# expected_upstream_lint_diffs.txt are known and accepted; any other
# difference fails this check.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$(git -C "$here" rev-parse --show-toplevel 2>/dev/null)" || { echo "skip: not a git checkout"; exit 0; }
if ! ls "$root"/scripts/check_*.py >/dev/null 2>&1 || ! git -C "$root" rev-parse -q --verify main >/dev/null; then
  echo "skip: no upstream lints here (Claude fork only)"; exit 0
fi
tmp="$(mktemp -d)"
trap 'git -C "$root" worktree remove --force "$tmp/up" >/dev/null 2>&1; rm -rf "$tmp"' EXIT
git -C "$root" worktree add --detach "$tmp/up" main >/dev/null 2>&1 || { echo "could not create the upstream worktree"; exit 1; }
results() { (cd "$1" && for f in scripts/check_*.py; do python3 "$f" >/dev/null 2>&1; echo "$? $f"; done); }
results "$tmp/up" > "$tmp/upstream.txt"
results "$root"   > "$tmp/ours.txt"
actual="$(diff "$tmp/upstream.txt" "$tmp/ours.txt" | awk '/^[<>]/{print $3}' | sort -u)"
expected="$(grep -v '^#' "$here/expected_upstream_lint_diffs.txt" | awk 'NF{print $1}' | sort -u)"
echo "upstream lints run: $(wc -l < "$tmp/ours.txt" | tr -d ' ')"
echo "lints whose result differs from pure upstream:"; echo "${actual:-(none)}" | sed 's/^/  /'
if [ "$actual" = "$expected" ]; then
  echo "upstream-lint comparison: only the expected differences"
else
  echo "UNEXPECTED upstream-lint differences (left = expected only, right = actual only):"
  comm -3 <(echo "$expected") <(echo "$actual")
  exit 1
fi

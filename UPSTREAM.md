# Upstream

This repository began as a fork of Cheng-I Wu's Academic Research Skills (ARS) (https://github.com/Imbad0202/academic-research-skills, CC-BY-NC 4.0).
Since 2026-10-06 it is maintained as its own product (Tom's decision): the
security track is part of the suite, any file may be edited, and upstream is
a reference to learn from, not a source to merge.

- **Last reviewed upstream commit: 6ab4b03** (ARS v3.23.0, reviewed 2026-10-06)
- Upstream remote: `upstream` → https://github.com/Imbad0202/academic-research-skills.git
- `main` stays frozen at the last merged upstream commit as a comparison
  baseline; all work is on `dev`.

## Reviewing an upstream update

1. Run `git upstream-review` on `dev`. It fetches upstream and lists the
   commits and changed files since the last reviewed commit. Nothing is merged.
2. Read the upstream changelog for those commits. Decide each change:
   **PORT** (take as is), **ADAPT** (take, changed for this suite) or **SKIP**
   (with the reason).
3. Port on `dev` by hand, or with `git cherry-pick -x <id>` /
   `git diff <old> <new> -- <path> | git apply`. Then run the checks
   (`bash security-track/tests/run_all_checks.sh` and `bash security-track/tests/compare_upstream_lints.sh`).
4. Add a row to the review log below and move "Last reviewed upstream commit"
   to the newest upstream change you reviewed.

## License

Upstream is CC-BY-NC 4.0. Keep its attribution (LICENSE, NOTICE, citation
file, author credits) and keep the work non-commercial.

## Review log

| Date | Upstream range | Outcome |
|---|---|---|
| 2026-09-30 | v3.19.0 → v3.22.2 (`af2797c..333fd5e`) | Merged in full: the last merge before the 2026-10-06 policy change |
| 2026-10-06 | v3.22.2 → v3.23.0 (`333fd5e..6ab4b03`, 16 changes) | **PORT all 16** with `git cherry-pick -x` (Tom: take them all, including the new skill). 13 pipeline, schema, ledger and registry fixes; `sr-screener` (#919) and its CSV-formula fix (#951); the v3.23.0 release notes. **ADAPT** where our files differ: skill and mode counts are 10 skills / 35 modes; `sr-screener` is registered beside our five skills; the routing core keeps both upstream's Screening boundary paragraph and our Security-first default (11 copies); the `academic-pipeline/SKILL.md` content lock is re-pinned for our routing paragraph (all other locks equal upstream's). Pre-port state: branch `backup/pre-port-3.23.0`. |

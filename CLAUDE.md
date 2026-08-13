# Security Track Overlay (user-owned, dev branch)

This fork adapts ARS for **security-conference research** (CPS security,
IoT security, AI/ML security). The upstream suite assumes ML/journal
conventions; the rules below override those defaults. Upstream's own
instructions live in `.claude/CLAUDE.md` and still apply where not
overridden here.

## Default assumption

Unless the user says otherwise, every paper task targets a security venue:
the Big 4 (IEEE S&P, NDSS, ACM CCS, USENIX Security) or a tier-2 venue from
the tracked list. If a task is explicitly NOT security research, ignore this
overlay and use stock ARS behavior.

## Required reading before paper work

Before planning, outlining, drafting, reviewing, or revising a paper, read
the relevant files from `security-track/references/`:

| Task | Read first |
|---|---|
| Venue choice, submission planning | `big4_venue_profiles.md` + `deadlines_current.md` |
| Writing / outlining / revising | `security_paper_conventions.md` |
| Peer-review simulation (`/ars-reviewer`, reviewer skill) | `security_reviewer_personas.md` |
| Ranking / tier questions | `conference_ranking_2025.json` |
| Reviewer comments / rebuttal / revision / re-review | `major_revision_playbook.md` |

## Overrides of stock ARS defaults

- **Citations:** IEEE/ACM numeric style, NOT APA 7.0. Two-column
  conference LaTeX, hard page limits — not journal word counts.
- **Structure:** Intro / Threat Model / Design / Implementation / Eval /
  Discussion / Related Work / Ethics — not IMRaD. A paper without an
  explicit threat-model section is incomplete.
- **Reviewer panel:** when the paper targets a security venue, the
  `academic-paper-reviewer` panel MUST use the five personas in
  `security_reviewer_personas.md` (PC Chair, CPS, IoT/embedded,
  Adversarial-ML, threat-model skeptic) instead of journal-field personas,
  the verdict vocabulary Accept / Minor revision / Major revision (numbered
  binding criteria) / Reject, and the eight rejection anchors in that file.
  This composes with — does not replace — the stock review process
  (5 independent reviewers, synthesis, integrity gates).
- **field_analyst_agent:** for security papers, skip journal-field
  detection and configure the panel from the personas file directly.

## Deadlines are never recalled from memory

Quote deadlines ONLY from `security-track/references/deadlines_current.md`.
If its `Fetched` timestamp is older than 7 days, refresh first:
`python3 security-track/scripts/fetch_deadlines.py`. If the fetch fails,
say the calendar is stale — do not fill in dates from model memory.

## Repo conventions (fork hygiene)

- `main` mirrors upstream (ff-only); ALL personal work goes on `dev`.
- Customizations are additive only: the `security-track/` skill, its
  `skills/security-track` symlink, and this file. Sole permitted upstream-file
  edit: the one-line `"./security-track"` entry in
  `.claude-plugin/marketplace.json` (keep that edit minimal when resolving
  any future sync conflict). Never edit other upstream-owned files — that is
  what keeps `git sync-upstream` conflict-free.

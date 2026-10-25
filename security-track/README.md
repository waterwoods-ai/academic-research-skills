# Security Track — Installation and Usage

> Day-to-day manual (quick reference for every stage, plus the research loop S0–S8): [`HOWTO.md`](../HOWTO.md)

> This fork adds a fifth skill, `security-track`, to the four upstream ARS skills:
> an overlay for research aimed at top security conferences (the Big 4 and tier-2),
> calibrated for CPS, IoT and AI security.
> The same plugin also carries four skills of its own: `find-research-topic`,
> `verify-research-topic`, `novelty-filter` (the topic-scouting and novelty-check
> front end; needs a browser) and `novelty-engine` (the idea generator).
> Since 2026-10-06 this repository is maintained as its own product: any file may be
> edited, and nothing is merged from upstream any more. Upstream updates are reviewed
> and ported by hand (see `UPSTREAM.md` at the repository root). All work happens on
> the `dev` branch (the GitHub default branch is `dev`); `main` is frozen at the last
> merged upstream version and serves only as a comparison baseline.

## What this skill contains

| File | Contents |
|---|---|
| `SKILL.md` | Triggers, and the rules that override stock ARS defaults (citation style, paper structure, reviewer panel, double-blind, the deadline rule) |
| `references/big4_venue_profiles.md` | Big-4 venue profiles: format / decision process / artifact evaluation / ethics (checked item by item against the official CFPs, 2023–2027 editions) |
| `references/security_paper_conventions.md` | Security-paper writing conventions: the Threat Model section, the three-direction evaluation bar, responsible disclosure, the anonymization checklist |
| `references/security_reviewer_personas.md` | The five-person security reviewer panel and the standard rejection anchors |
| `references/major_revision_playbook.md` | Field manual for multi-round review at the Big 4: rebuttal / revision / re-review mechanics, mapped to ARS modes |
| `references/perspective_retrieval_protocol.md` | Perspective-driven retrieval protocol (an adaptation of STORM's retrieval-side mechanism; opt-in) |
| `references/conference_ranking_2025.json` | Snapshot of the 22-conference CIF ranking (source: jianying.space; updated yearly) |
| `references/deadlines_current.md` | Deadline calendar (**generated file, do not edit by hand**; source: sec-deadlines.github.io) |
| `scripts/fetch_deadlines.py` | Fetches the deadline calendar (re-fetches automatically when it is older than 7 days) |
| `contracts/reviewer/security_full.json` | Sprint contract for security venues (blind pre-commitment rubric; validates against Schema 13.2; F-condition syntax matches upstream) |
| `references/research_loop_protocol.md` | Research loop protocol: S0 topic → S1 gap → S2 extending the topic → S3 proposing or assessing a method (novelty + contribution) → S4 falsification experiment design → S5 execution → S6 bounded improvement loop → S7 adversarial stress test → S8 paper |

## Installation (Claude Code)

```
# If you installed the upstream version, remove it first (marketplaces with the same name conflict)
/plugin marketplace remove academic-research-skills

# Option A: install from GitHub (the default branch is already dev, so this installs this version)
/plugin marketplace add waterwoods-ai/academic-research-skills

# Option B: local developer mode — use a local clone as the marketplace; edits take effect directly
/plugin marketplace add /path/to/academic-research-skills

# Install
/plugin install academic-research-skills@academic-research-skills
```

Start a **new session** after installing. To verify, ask "What is the NDSS Major
Revision process?": the agent should read `major_revision_playbook.md` rather than
answer from memory.

To update: with the GitHub source, run `/plugin update academic-research-skills`;
a local-path source needs no reinstall, just start a new session.

## Usage

**Automatic activation:** it triggers on any paper task that involves a security
conference (conference names, threat model, CPS/IoT/AI security and the other
triggers in the `SKILL.md` frontmatter). When the user's profile is security
research, every paper task targets a security conference by default; say explicitly
that the work is not security research to fall back to the stock behaviour.

**Working with the ARS commands** (the overlay applies automatically; nothing extra to specify):

| What you want to do | How | What the overlay adds |
|---|---|---|
| Choose a venue / plan the submission | ask directly, or `/ars-plan` | venue profiles + the live deadline calendar |
| Literature review | `/ars-lit-review`; say "make sure the coverage is comprehensive" to trigger the perspective retrieval protocol | six-lens query expansion + follow-up on unused searches |
| Writing / outline | `/ars-outline`, `/ars-full` | security-paper structure, numeric citations, the double-blind checklist |
| Simulated review | `/ars-reviewer` | the five-person security panel + the target venue's exact decision vocabulary |
| Reviews received | `/ars-revision-coach` | a roadmap and response-package structure for the venue and decision tier |
| Check a rebuttal draft | `/ars-rebuttal-audit` | an audit against the venue's hard rules (S&P's 500-word limit, etc.) |
| Extend a topic / propose a method / assess novelty / design and run experiments / improve a method | say which stage you are at (e.g. "assess the novelty of my method") | the research loop protocol S0–S8, with the improvement loop capped at 3 rounds + human checkpoints |

**Deadline rule:** quote dates only from `references/deadlines_current.md`. If it is
older than 7 days, first run `python3 security-track/scripts/fetch_deadlines.py`
(needs the network + Python 3.10+ / pyyaml). If the fetch fails, say clearly that
the calendar is stale; never give dates from model memory.

## Maintenance (fork workflow)

```bash
git upstream-review   # fetch upstream and list the changes and files since the last review (no merge)
```

- Upstream changes are reviewed one by one and ported by hand; the outcome is logged in `UPSTREAM.md`. Any file may be edited.
- `conference_ranking_2025.json`: the ranking source updates once a year; take a new snapshot then.
- The venue profiles pin structural facts; page limits and the number of review rounds drift, so check the current year's CFP close to submission.

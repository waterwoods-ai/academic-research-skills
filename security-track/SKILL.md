---
name: security-track
description: "Security-conference overlay for the ARS suite: Big-4 venue profiles (IEEE S&P, NDSS, ACM CCS, USENIX Security) + tier-2 fallbacks, systems-security writing conventions (threat model, ethics, artifact evaluation), security reviewer personas for CPS/IoT/AI-security papers, the 22-conference CIF ranking, and a live deadline calendar fetched from sec-deadlines.github.io. Use WITH the other ARS skills whenever a paper task targets a security venue: venue selection, submission planning, deadline questions, outlining, drafting, reviewing, or revising a security paper. Triggers: security paper, security conference, Big 4, S&P, Oakland, NDSS, CCS, USENIX Security, threat model, responsible disclosure, artifact evaluation, CPS security, ICS security, IoT security, firmware, AI security, adversarial ML, 安全会议, 安全论文, 四大安全会议, 威胁模型, 顶会."
metadata:
  version: "0.1.0"
  last_updated: "2026-08-13"
  status: active
  overlay: true
  related_skills:
    - academic-paper
    - academic-paper-reviewer
    - academic-pipeline
    - deep-research
---

# Security Track Overlay

This skill is an **overlay, not a pipeline**: it never runs alone. It
reconfigures the four stock ARS skills — which assume ML/journal
conventions — for papers targeting top security conferences. All stock
process machinery (agent ensembles, integrity gates, Material Passport,
review synthesis) stays intact; this overlay changes field assumptions,
venue knowledge, personas, and formatting defaults.

## Activation

Activate whenever a paper task targets a security venue — the Big 4
(IEEE S&P, NDSS, ACM CCS, USENIX Security) or a tier-2 venue in
`references/conference_ranking_2025.json`. When the user's profile says
their research is security (e.g., CPS / IoT / AI security), treat security
as the default target and this overlay as active for every paper task
unless the user says otherwise.

## Reference routing

Read the relevant reference BEFORE the corresponding task:

| Task | Read |
|---|---|
| Venue choice, submission planning | `references/big4_venue_profiles.md` + `references/deadlines_current.md` |
| Writing / outlining / drafting / revising | `references/security_paper_conventions.md` |
| Peer-review simulation | `references/security_reviewer_personas.md` |
| Ranking / tier questions | `references/conference_ranking_2025.json` |
| Reviewer comments / rebuttal / revision / re-review | `references/major_revision_playbook.md` |

## Overrides of stock ARS defaults

1. **Citations:** IEEE/ACM numeric style (`[12]`), NOT APA 7.0.
   Two-column conference LaTeX with hard page limits (~12–13 pages
   excluding references/appendices), not journal word counts.
2. **Structure:** Introduction / Threat Model / Design / Implementation /
   Evaluation / Discussion / Related Work / Ethics Considerations — not
   IMRaD. A security paper without an explicit threat-model section is
   structurally incomplete. USENIX Security additionally expects an Ethics
   Considerations appendix ('26 mandatory, '27 strongly encouraged) and
   Open Science compliance.
3. **Reviewer panel:** for security papers the `academic-paper-reviewer`
   panel MUST use the five personas in
   `references/security_reviewer_personas.md` (PC Chair, Systems/CPS,
   IoT/embedded, Adversarial-ML, threat-model skeptic) instead of
   journal-field personas; `field_analyst_agent` skips journal-field
   detection and configures the panel from that file. Verdict vocabulary: the TARGET
   venue's exact decision names per `references/major_revision_playbook.md`
   §1 (S&P: Accept/Reject only; NDSS: 4-tier incl. Major Revision; CCS:
   Accept/Minor revision/Reject; USENIX '26+: Accepted/Shepherd
   Approval/Rejected). Calibrate against the file's eight standard rejection anchors.
   This composes with — never replaces — the stock 5-reviewer process,
   synthesis, and integrity gates.
4. **Anonymity:** strict double-blind is the default; apply the
   anonymization checklist in `references/security_paper_conventions.md`
   during formatting and citation passes.

## Deadline integrity rule (IRON RULE)

Conference deadlines are quoted ONLY from
`references/deadlines_current.md`. If its `Fetched` timestamp is older
than 7 days, refresh first: `python3 scripts/fetch_deadlines.py`
(network access + Python 3.10+ with pyyaml required). If the refresh
fails, state that the calendar is stale and give the source URL
(https://sec-deadlines.github.io) — NEVER fill in deadline dates from
model memory.

## Maintenance

- `references/deadlines_current.md` is generated — never hand-edit.
- `references/conference_ranking_2025.json` snapshots the CIF ranking
  from http://jianying.space/conference-ranking.html (updated yearly;
  re-snapshot when the source publishes a new year).
- Venue profiles pin structural facts (formats, decision processes);
  page limits and cycle counts drift — verify against the current CFP
  when a submission is imminent.

---
name: security-track
description: "Security-conference overlay for the ARS suite: Big-4 venue profiles (IEEE S&P, NDSS, ACM CCS, USENIX Security) + tier-2 fallbacks, systems-security writing conventions (threat model, ethics, artifact evaluation), security reviewer personas for CPS/IoT/AI-security papers, the 22-conference CIF ranking, and a live deadline calendar fetched from sec-deadlines.github.io. Use WITH the other ARS skills whenever a paper task targets a security venue: venue selection, submission planning, deadline questions, outlining, drafting, reviewing, or revising a security paper. Triggers: security paper, security conference, Big 4, S&P, Oakland, NDSS, CCS, USENIX Security, threat model, responsible disclosure, artifact evaluation, CPS security, ICS security, IoT security, firmware, AI security, adversarial ML, research gap, extend topic, topic viability, go/no-go, propose method, novelty assessment, contribution, experiment design, falsification, run experiments, improve method, 安全会议, 安全论文, 四大安全会议, 威胁模型, 顶会, 研究缺口, 延伸课题, 新方法, 创新点, 实验设计."
metadata:
  version: "0.1.0"
  last_updated: "2026-08-14"
  status: active
  data_access_level: verified_only
  task_type: open-ended
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
| Literature search / coverage expansion ("broad coverage", lit-review, gap analysis) | `references/perspective_retrieval_protocol.md` |
| Research loop: gap → RQ → method proposal/evaluation (novelty & contribution) → experiment design/run → bounded improvement → paper | `references/research_loop_protocol.md` |

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
   Before the panel runs, R0 executes the Phase-0 manuscript-compliance
   check (personas file § Phase-0); any FAIL row prefixes the final verdict
   with "CONDITIONAL ON COMPLIANCE FIX". **Sprint contract:** the paper-blind
   Phase-1 pre-commitment MUST load `contracts/reviewer/security_full.json`
   from this skill instead of the stock `shared/contracts/reviewer/full.json`
   — it pre-commits security-conference dimensions (threat-model soundness,
   evaluation adequacy incl. adaptive-adversary/testbed/device-diversity
   bars, novelty vs Big-4 prior work, deployment realism, ethics/disclosure
   adequacy, reproducibility, presentation); its failure-condition grammar is
   identical to stock, so the synthesizer's mechanical protocol and
   `check_panel_synthesis.py` run unchanged. The contract's internal
   decisions then map to the TARGET venue's vocabulary at output
   (playbook §1): NDSS 1:1; S&P accept→Accept (warn-level findings become
   the public meta-review draft), everything else→Reject; CCS
   major_revision→Reject (no such tier; findings labeled accordingly);
   USENIX '26+ minor_revision→Accepted on Shepherd Approval,
   major_revision→Rejected. This composes with — never replaces — the
   stock 5-reviewer process, synthesis, and integrity gates.
4. **Anonymity:** strict double-blind is the default; apply the
   anonymization checklist in `references/security_paper_conventions.md`
   during formatting and citation passes.

## Review Workspace (stateful multi-round reviews)

Standalone reviewer invocations MUST be stateful so the user never
re-pastes prior rounds. On the FIRST `ars-reviewer` run for a paper,
create `ars-review/` next to the manuscript:

```
ars-review/
├── state.json            {venue, paper_path, round, created}
└── round-1/
    ├── decision.md       verdict + numbered task list + panel reports
    ├── compliance.md     Phase-0 table
    └── manuscript-snapshot.<ext>   copy of the paper as reviewed
```

On `re-review`, NOTHING needs to be supplied. Defaults, in order:
1. Venue + paper path from `state.json`; latest `round-N/decision.md` is
   the frozen task list. Never ask the user to re-paste them.
2. Change map: if `round-N/changelog.md` exists (user-maintained,
   "T1 → §4.2 …" lines), use it verbatim. Otherwise DIFF the current
   manuscript against `round-N/manuscript-snapshot.*`, draft the
   task-to-change mapping yourself, and show it for a one-line
   confirmation before judging. The mapping exists to keep verification
   mechanical and to suppress hallucinated regressions — it is the
   system's job to produce it, the user's only to correct it.
3. **Verify against artifacts, never against the changelog alone.** The
   changelog is an index; every verdict must cite evidence of the class the
   task demands:
   - *Text task* (clarify, add section, fix claim) → quote the revised
     manuscript text; the diff against the snapshot must show it.
   - *Experiment/result task* (add adaptive evaluation, new baseline,
     ablation, more devices) → the ledger (`./ledger/` or the paper's
     provenance record) must contain a run for it, and the numbers in the
     revised text must match the ledger. A new table with no ledger entry
     is NOT RESOLVED — "numbers only from execution logs" applies to
     verification too.
   - *Code/artifact task* (release code, fix implementation, reproducibility)
     → open the artifact: file exists, referenced path resolves, README/
     scripts support the claim; run or spot-check when feasible.
   - *Formalization task* (define threat model, prove/state property) →
     the definition/proof appears in the manuscript and is consistent
     with the claims that depend on it.
   A task whose changelog line has no corresponding artifact evidence
   is NOT RESOLVED regardless of what the changelog says.
4. Write the new round's outputs to `round-(N+1)/` and bump `state.json`.

Explicit arguments always override defaults. If `ars-review/` is absent
on a re-review request, fall back to asking for the prior decision (the
stateless path still works, e.g. on another machine).

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

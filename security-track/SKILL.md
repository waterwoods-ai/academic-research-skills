---
name: security-track
description: "Security-conference overlay for the ARS suite: Big-4 venue profiles (IEEE S&P, NDSS, ACM CCS, USENIX Security) + tier-2 fallbacks, systems-security writing conventions (threat model, ethics, artifact evaluation), security reviewer personas for CPS/IoT/AI-security papers, the 22-conference CIF ranking, and a live deadline calendar fetched from sec-deadlines.github.io. Use WITH the other ARS skills whenever a paper task targets a security venue: venue selection, submission planning, deadline questions, outlining, drafting, reviewing, or revising a security paper. Triggers: security paper, security conference, Big 4, S&P, Oakland, NDSS, CCS, USENIX Security, threat model, CVE, MITRE ATT&CK, ATT&CK technique mapping, responsible disclosure, artifact evaluation, CPS security, ICS security, IoT security, firmware, AI security, adversarial ML, research gap, extend topic, topic viability, go/no-go, propose method, novelty assessment, contribution, experiment design, falsification, run experiments, improve method, method substitution, rename check, prior art check, taxonomy, define categories, security framing, dissect this paper, peruse this paper, peruse paper, introduction structure, subfield reviewer bar, retrospective, lessons learned, knowledge index, mentor me, guide me step by step, be my research mentor, pre-registration, pre-register, research integrity, cherry-picking, seed hacking, HARKing, data leakage, eval-set overfitting, reproducibility check, humanize, humanizer, polish prose, language polish, de-slop, remove AI tells, AI slop, clarity pass, find research topic, scout topic, research gap mapping, Elicit, Litmaps, verify research topic, topic verification, stress-test my topic, novelty check, build on this paper, multi-agent lab, research team roles, orchestrator, Reviewer #2, claims register, reject reasons, agent refused, authorized research scope, 一步一步指导, 带我完成, 安全会议, 安全论文, 四大安全会议, 威胁模型, 顶会, 研究缺口, 延伸课题, 新方法, 创新点, 实验设计, 精读, 拆解论文, 预注册, 研究诚信, 实验诚信, 润色, 语言润色, 去AI味, 选题, 找课题, 验证课题, 查新."
metadata:
  version: "0.3.0"
  last_updated: "2026-10-06"
  status: active
  data_access_level: raw
  task_type: open-ended
  overlay: true
  related_skills:
    - academic-paper
    - academic-paper-reviewer
    - academic-pipeline
    - deep-research
    - academic-humanizer
    - find-research-topic
    - verify-research-topic
    - novelty-filter
    - novelty-engine
---

# Security Track Overlay

<!-- routing-core:begin -->
**Step 0 — Escape hatch check (before any classification):** If the user's first message begins with `[direct-mode]` (case-insensitive byte-0 token, optionally preceded by whitespace/newlines that are stripped on parse), record this fact, strip the prefix and surrounding whitespace from the message, and skip directly to **Step 1 explicit-intent handling** on the stripped content. The literal `[direct-mode]` is NOT passed through to the dispatched agent. If the stripped message itself has no clear skill named, Step 1 falls through to Step 3 clarification (the escape hatch bypasses cross-phase clarification (Step 2), not all routing). When the token is honored and the named agent or skill needs inputs the message does not supply, read that agent's or skill's file and ask for what it requires, in its terms. Without the byte-0 token, naming an agent is not explicit intent: such a message goes through Steps 1-3 like any other, so cross-phase materials still get Step 2 clarification.

Otherwise, classify the user's input:

1. **Explicit clear intent** — user invokes a specific skill via `/ars-*` slash command, or uses an unambiguous trigger keyword that maps to a single skill (e.g., "lit-review this", "review my paper", "draft an abstract"):
   → Route directly; no clarification, no orchestrator detour.
   → The request stays explicit when the mode's usual input is absent or a word in it has other everyday senses. A revision request with no reviewer comments is revision mode's "feel certain sections need improvement" case, and "revisar artículo" is the reviewer's trigger. Route to that mode and let the mode handle what is missing; do not reopen the choice of workflow.

2. **Cross-phase materials detected** — user provides artifacts spanning ≥ 2 pipeline phases without naming a specific skill (e.g., pre-written abstract + pre-collected literature; full draft + reviewer comments + bibliography):
   → **Clarify**. Do NOT auto-route to a single-phase agent. List candidate workflows as a-d options in markdown body (NOT via AskUserQuestion tool). See `shared/references/intent_clarification_protocol.md` for the message template.
   → Reason: clarification is the safest action when materials don't unambiguously identify intent. (v3.10 active conductor (#134) will handle this via structured intake; v3.9.2 asks.)

3. **Ambiguous intent, no materials** — user provides no artifacts and no clear request:
   → Clarify per `shared/references/intent_clarification_protocol.md`.

**Anti-pattern (caused #133):** Receiving ambiguous cross-phase materials and silently auto-routing to a single-phase agent based on which phase the materials "look closest to." This bypasses orchestrator-level reconciliation and lets the subagent inherit the full ambiguity without independent oversight.

**Security-first default (this suite):** every research or paper task targets a security venue — the Big 4 (IEEE S&P, NDSS, ACM CCS, USENIX Security) or a tier-2 venue — unless the opt-out rule in the `security-track` skill (§ Activation) holds. Before configuring any ARS skill or agent for such a task, load `security-track` and apply its § Overrides of stock ARS defaults: IEEE/ACM numeric citations instead of APA 7.0; the security chapter structure with an explicit Threat Model and Ethics Considerations instead of IMRaD, sized by the venue's page limit; the five security reviewer personas with the target venue's decision vocabulary; double-blind anonymity; and conference deadlines only from its `deadlines_current.md`.
<!-- routing-core:end -->

This skill is an **overlay, not a pipeline**: it never runs alone. It
reconfigures the four stock ARS skills — which assume ML/journal
conventions — for papers targeting top security conferences. All stock
process machinery (agent ensembles, integrity gates, Material Passport,
review synthesis) stays intact; this overlay changes field assumptions,
venue knowledge, personas, and formatting defaults.

## Activation

This suite is **security-first**. The routing core carried by every skill
and by the session-start announcement tells the agent to load this skill for
every research or paper task, so it applies even in a folder without a
project `CLAUDE.md` / `AGENTS.md` anchor. The agents that choose defaults
(paper intake, reviewer field analyst, report compiler) say the same. Venues:
the Big 4 (IEEE S&P, NDSS, ACM CCS, USENIX Security) or a tier-2 venue in
`references/conference_ranking_2025.json`.

**Opt-out rule** — the one place that decides when the stock ARS defaults
(APA 7.0, IMRaD, journal-field reviewer panel, word counts) apply instead:

- **The user says so** ("not security research", "use APA") → stock
  defaults for that task.
- **A non-security target venue** (an ML venue such as NeurIPS / ICML /
  ICLR, or a journal outside security) → that venue's own template,
  citation style, length and review form. A paper with an adversary keeps
  its threat-model section wherever it goes.
- **A security journal** (IEEE TDSC, IEEE TIFS, ACM TOPS, Computers &
  Security) → partial: keep the security structure, numeric citations and
  the security personas; take length and decision vocabulary (Minor / Major
  Revision) from the journal's author guidelines, not a conference page limit.
- **Grant proposals, theses, teaching material** → the funder's or
  institution's structure; this skill still supplies the security content
  (threat model, venue and prior-work knowledge).
- **Unclear** (no venue named, topic not obviously security) → stay
  security-first; do not ask just to settle the default.


## Reference routing

Read the relevant reference BEFORE the corresponding task:

| Task | Read |
|---|---|
| Venue choice, submission planning | `references/big4_venue_profiles.md` + `references/deadlines_current.md` |
| Planning / outlining / writing / drafting / revising (ars-plan, ars-outline, ars-full) — use the security chapter structure, NOT IMRaD | `references/security_paper_conventions.md` |
| Polishing AI-assisted prose of a security paper (de-slop, remove AI tells, match claims to evidence) — drive the standalone `academic-humanizer` skill with security-venue calibration; run at S8 / revision AFTER content is frozen | `references/security_humanizing_overlay.md` |
| New research idea — is this a security paper? (framing / novelty type) | `references/security_framing_protocol.md` |
| Building or checking a threat model | `references/threat_model_workbench.md` |
| Connecting the work to CVE / MITRE ATT&CK (mapping, technique ids) | `references/cve_attack_mapping.md` |
| Changing / improving / substituting a method, esp. to rescue a failing experiment (anti-rename) | `references/method_change_provenance.md` |
| Deep-read ONE paper (dissect / peruse / 精读) — NOT multi-paper lit-review | `references/paper_dissection_protocol.md` |
| Peer-review simulation | `references/security_reviewer_personas.md` |
| Ranking / tier questions | `references/conference_ranking_2025.json` |
| Reviewer comments / rebuttal / revision / re-review | `references/major_revision_playbook.md` |
| Literature search / coverage expansion ("broad coverage", lit-review, gap analysis) | `references/perspective_retrieval_protocol.md` |
| Finding / scouting a research topic, gap mapping with Elicit + Litmaps, building on one baseline paper (which front-end at which stage, and what its verdict counts for) | `references/topic_scouting_overlay.md` |
| Verifying a chosen topic before method work (12 questions, go / revise / stop) | `references/topic_verification_gate.md` |
| Running the project as a multi-agent lab: roles (Director with literature and novelty, security scientist, research engineer and Reviewer #2), who writes which file, the independent-check matrix, gates 1–4, claims and reject-reasons registers, refusal routing, authorization scope | `references/lab_orchestration_protocol.md` |
| Research loop: gap → RQ → method proposal/evaluation (novelty & contribution) → experiment design/run → bounded improvement → paper | `references/research_loop_protocol.md` |
| Pre-registering an experiment / evaluation integrity / research-integrity self-audit (freeze success criteria before running, no cherry-picking, anti-HARKing, claim-vs-artifact) — load at S4/S5, S7/S8, S8.5 | `references/research_integrity_protocol.md` |
| Step-by-step Socratic mentor (idea→submission, one step per turn, stateful) — NOT ars-plan's whole-plan-at-once | `references/security_mentor_protocol.md` |
| Subfield reviewer bar / best practice (load at S1/S2/S3/S7) | `references/knowledge_index.md` |
| Skill self-check (run before every commit and after porting an upstream change) | `tests/run_all_checks.sh` → behavior linter + workspace validator + knowledge-index consistency |
| Post-submission / post-review retrospective (L2 knowledge distillation) | `references/research_loop_protocol.md` § S8.5 + `references/knowledge_notes/` |

## Overrides of stock ARS defaults

1. **Citations:** IEEE/ACM numeric style (`[12]`), NOT APA 7.0.
   Two-column conference LaTeX with hard page limits (~12–13 pages
   excluding references/appendices), not journal word counts.
2. **Structure:** Introduction / Threat Model / Design / Implementation /
   Evaluation / Discussion / Related Work / Ethics Considerations — not
   IMRaD. A security paper without an explicit threat-model section is
   structurally incomplete. USENIX Security additionally expects an Ethics
   Considerations appendix ('26 mandatory, '27 strongly encouraged) and
   Open Science compliance. **This override applies to PLANNING and
   OUTLINING too** — `ars-plan` / `ars-outline` (and academic-paper plan/
   outline modes) default to the IMRaD chapter list (Introduction →
   Literature → Method → Results → Discussion → Conclusion); for a security
   paper you MUST replace it with the security chapter structure above,
   confirm the target venue first (it sets page budget + Ethics/Open-Science
   requirements per `big4_venue_profiles.md`), and run the chapter-by-chapter
   Socratic dialogue against the security structure — probing the Threat
   Model chapter, not a generic Methods chapter.
3. **Reviewer panel:** for security papers the `academic-paper-reviewer`
   panel MUST use the five personas in
   `references/security_reviewer_personas.md` (PC Chair, Systems/CPS,
   IoT/embedded, Adversarial-ML, threat-model skeptic) instead of
   journal-field personas; `field_analyst_agent` skips journal-field
   detection and configures the panel from that file. Verdict vocabulary: the TARGET
   venue's exact decision names per `references/major_revision_playbook.md`
   §1 (S&P: Accept/Reject only; NDSS: 4-tier incl. Major Revision; CCS:
   Accept/Minor revision/Reject; USENIX '26+: Accepted/Shepherd
   Approval/Rejected). Calibrate against the file's standard rejection anchors.
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

**IRON RULE — all review output lands in `ars-review/`.** Every review
artifact — each round's decision + numbered task list + panel reports, the
Phase-0 compliance table, the manuscript snapshot, and every re-review
verdict — is written under `ars-review/round-N/` next to the manuscript,
never delivered only in chat. This is what makes re-review zero-argument and
the review history auditable.

Standalone reviewer invocations MUST be stateful so the user never
re-pastes prior rounds. On the FIRST `ars-reviewer` run for a paper,
create `ars-review/` next to the manuscript:

```
ars-review/
├── state.json            typed per contracts/review-workspace.schema.json
│                        (validate: scripts/validate_review_workspace.py)
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

## Execution environment (local Python)

Any security-track task that runs Python locally — the review-workspace
validator (`scripts/validate_review_workspace.py`), the knowledge-index and
behavior linters (`tests/run_all_checks.sh`), `scripts/fetch_deadlines.py`, or
any review/experiment helper — MUST use the shared `~/.venv` virtual
environment: `source ~/.venv/bin/activate` first, then run. Do not use system
Python or an ad-hoc venv. (Remote GPU model training/inference keeps its own
compute environment per the user's compute rules; this `~/.venv` rule is for
local review + tooling Python.)

## Maintenance

- `references/deadlines_current.md` is generated — never hand-edit.
- `references/conference_ranking_2025.json` snapshots the CIF ranking
  from http://jianying.space/conference-ranking.html (updated yearly;
  re-snapshot when the source publishes a new year).
- Venue profiles pin structural facts (formats, decision processes);
  page limits and cycle counts drift — verify against the current CFP
  when a submission is imminent.

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 0.3.0 |
| Last Updated | 2026-10-06 |
| Maintainer | Tom |
| Dependent Skills | academic-paper, academic-paper-reviewer, academic-pipeline, deep-research |
| Role | Security-conference overlay: venues and deadlines, threat model, research loop S0–S8, integrity, reviewer personas, lab orchestration |

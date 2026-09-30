---
name: novelty-engine
description: "Academic Novelty & Method Engineering Engine — the suite's idea generator. 4-stage, 11-phase pipeline: (I) Research Preparation — topic verification, paper discovery, gap analysis, go/no-go; (II) Idea Generation — dogma extraction, novelty verification, cross-domain synthesis; (III) Formalization & Proof — math/algorithms, falsification experiments, runnable code; (IV) Validation & Publication — ARS peer review, hardening, full paper. 8 agents. Math or algorithm required for every method. Use when the user asks to generate research ideas, propose a novel method, break a field's assumptions, import a method from another discipline, formalize a method, or design falsification experiments. Triggers: novelty engine, idea generation, generate ideas, novel method, propose a method, dogma, unstated assumption, cross-domain, formalize this method, falsification experiment, 生成想法, 提出新方法, 形式化."
argument-hint: "[verify | discover | gaps | assess | dogma | formalize | falsify | experiment | stress-test | paper]"
metadata:
  version: "1.2.0"
  last_updated: "2026-09-30"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - security-track
    - deep-research
    - academic-paper
    - academic-paper-reviewer
    - academic-pipeline
    - find-research-topic
    - verify-research-topic
    - novelty-filter
---

# Novelty Engine Pipeline

You are orchestrating the **Academic Novelty & Method Engineering Engine** — a 10-phase pipeline that generates publication-grade novel methodologies with mandatory mathematical/algorithmic formalization, then hands off to ARS for verified paper production.

## Prerequisites

- This skill ships inside the ARS suite, so the ARS skills it hands off to (literature review, reviewer, full pipeline) are always present.
- Inputs come by one of two routes:
  - **Configured sources** — the project's CLAUDE.md (AGENTS.md on Codex / opencode) has NotebookLM, Zotero, and Obsidian sections (not placeholders). Research topic and description come from NotebookLM; literature comes from Zotero; additional knowledge from Obsidian.
  - **Direct** — the user states the topic and points to the papers, or to research-loop artifacts that already exist (`gap_registry.md`, `rq_cards.md`, `research_question.md`). Use this route whenever the sources are not configured; do not stop to ask for them.
- The pipeline will verify the topic, find papers the user missed, and decide whether to proceed

## Agents

The eight agents are prompt files in this skill's `roles/` folder
(`topic_verifier`, `gap_analyzer`, `dogma_extractor`, `novelty_verifier`,
`cross_domain_synthesizer`, `math_formalizer`, `experiment_falsifier`,
`experiment_coder`). "Dispatch the X agent" below means:

- **Claude Code** — read `roles/X.md` and launch a general-purpose subagent
  with the file's body as its role, plus the phase inputs and the output path.
  Run it on the session model.
- **Codex / opencode** — no subagents: read `roles/X.md`, take that role
  yourself, finish the phase and write its output file before moving on. One
  agent at a time. The `/ars-*` commands named below are the matching
  academic-research-suite modes (`ars-lit-review`, `ars-reviewer`, `ars-full`);
  `/workflows` and `/goal` do not exist there, so run those steps sequentially.

## Inside the security-track research loop

For a security-venue project this skill is the generator for stages S0–S5 of
`../security-track/references/research_loop_protocol.md`. That protocol's iron
rules and gates govern; this skill supplies the machinery.

| Phase here | Loop stage | What the loop adds |
|---|---|---|
| 0a–0d topic, discovery, gaps, go/no-go | S0–S2 | Ancestor and adjacent-method-family queries; gaps in the three-field form; a GO here does not replace the topic verification gate before S3 |
| 1 dogma extraction | S2 (the dogma an RQ challenges), S3 propose mode | Each dogma is tied to a threat-model element (adversary, asset, trust boundary) |
| 2 novelty verification | S3 | Verdicts are search-bounded: NOVEL → NOVEL-WITHIN-SEARCH, PARTIALLY EXPLORED → INCREMENTAL, ALREADY PUBLISHED → KNOWN |
| 3 cross-domain synthesis | S3 propose mode | Every method states which baseline limitation it resolves and passes the security framing check |
| 4 formalization | S3 (iron rule 5) | Claims checked against the underlying theory; each hypothesis states its fundamentals and is verified part by part; output feeds the Contribution Card |
| 4.5a falsification design | S4 | The per-paper-type evaluation table and the pre-registration card; criteria freeze before any run |
| 4.5b experiment code | S5, S5a | Reproduce the strongest baseline first; every number comes from the ledger |
| 5 stress test | S7 | The five security reviewer personas; output under `ars-review/` |

**Entering at Phase 1 from the loop.** When the research question has already
passed the topic verification gate (a recorded `go` on the RQ card or in
`research_question.md`), that verdict stands in for the Phase 0d GO: start at
Phase 1 and do not re-run Phases 0a–0d. The papers are the ones the gap
registry cites.

A failed torture test is a lead, not a verdict (iron rule 6): find the root
cause before redesigning or dropping the method.

## Workspace Setup

On first invocation, create the workspace:

```
novelty_engine/
├── 00_literature/              ← User drops papers/abstracts here
├── 00_topic_verification/      ← Phase 0a output (viability + missing papers)
├── 00_gap_analysis/            ← Phase 0c output (gap registry + candidate RQs)
├── 01_dogma_scan/              ← Phase 1 output
├── 02_novelty_check/           ← Phase 2 output
├── 03_hybrid_methods/          ← Phase 3 output
├── 04_formal_spec/             ← Phase 4 output (math + algorithms)
├── 04_experiment/              ← Phase 4.5 output (falsification design + code)
│   ├── falsification_design.md
│   └── code/                   ← Runnable experiment code
├── 05_stress_test/             ← Phase 5 output (ARS review)
├── 06_final_proposal/          ← Phase 6 output (hardened methods)
└── 07_paper/                   ← Phase 7 output (ARS full paper)
```

Create the directory structure using Bash, then confirm with the user.

## Pipeline Phases

---

## STAGE I: RESEARCH PREPARATION (Phases 0a → 0d)

The first stage is entirely about deciding WHETHER and WHAT to research. No ideation happens until this stage completes with a GO verdict.

---

### PHASE 0a: Topic Intake & Verification
**Goal**: Verify the user's proposed topic is viable, timely, and correctly framed.

**Agent**: `topic_verifier`

**Process**:
1. Read the project's CLAUDE.md to resolve source configurations:
   - Parse `## Notes (NotebookLM)` → notebook name
   - Parse `## Literature (Zotero)` → collection name
   - Parse `## Knowledge Base (Obsidian)` → vault and folder
   If the sections are missing or still contain placeholders, take the direct route (Prerequisites): use the topic and papers the user gives, or the existing research-loop artifacts, and skip to step 3.
2. Gather inputs from configured sources:
   a. **Research topic & description** from NotebookLM:
      - Call `notebook_list` to resolve notebook name → notebook_id
      - Call `notebook_describe` to get topic summary and suggested topics
      - Call `notebook_query` asking "What is the research topic, focus, and motivation?" to extract the research description
   b. **Literature corpus** from Zotero:
      - Use zotero-literature skill: `search-items` in the configured collection
      - Extract paper titles, authors, years, and abstracts (at least 2-3 papers required)
      - Save paper summaries to `novelty_engine/00_literature/`
   c. **Additional knowledge context** from Obsidian:
      - Use obsidian CLI: `obsidian search vault="<vault>" query="research"` in the configured folder
      - Read relevant knowledge notes for domain context
3. Dispatch the topic_verifier agent with the topic, description, literature corpus, and knowledge context
4. The agent evaluates 5 viability dimensions:
   - **Maturity** (1-5): Is there enough foundation? Too early or too late?
   - **Saturation** (1-5, inverted): Is there room for contribution? Crowded or open?
   - **Tractability** (1-5): Can the gaps realistically be addressed?
   - **Impact potential** (1-5): Will anyone care about the results?
   - **Timing** (1-5): Is NOW the right moment?
5. The agent checks topic framing:
   - Is it too broad or too narrow?
   - Is the real problem adjacent to what the user described?
   - Is the user using the field's standard terminology?
6. Save viability assessment to `novelty_engine/00_topic_verification/viability_assessment.md`

**Checkpoint**: Present viability scores to user. If framing needs adjustment, suggest reframing before proceeding.

---

### PHASE 0b: Paper Discovery (Find What You Missed)
**Goal**: Systematically expand the literature corpus by finding papers the user didn't include.

**Agent**: `topic_verifier` (same agent, paper discovery step)

**Process**:
1. **Backward citation chain**: For each user-provided paper, extract its references. Identify highly-cited references the user did NOT include. Flag seminal/foundational papers that are missing.
2. **Forward citation chain**: For each user-provided paper, find papers that CITE it (via Semantic Scholar, OpenAlex). Focus on recent citing papers (last 2 years) — these represent the current frontier.
3. **Related work expansion**: Read "Related Work" sections of user's papers. Extract referenced papers the user didn't include.
4. **Keyword expansion search**: Try synonym/alternative terminology searches. The user may use one community's terms while relevant work uses different terms.
5. **Competition scan**: Search arXiv/preprint servers for recent work on the same topic. Assess competition severity: CLEAR FIELD | LIGHT COMPETITION | ACTIVE RACE | CROWDED.
6. Present a "papers you missed" report:
   - **MUST READ** (seminal papers, foundational work)
   - **SHOULD READ** (recent frontier, competing approaches)
   - **Competition threats** (groups working on the same problem)
7. Save to `novelty_engine/00_topic_verification/paper_discovery.md`
8. Add discovered papers to `novelty_engine/00_literature/` (abstracts + key findings)

**Acceleration with /workflows**:
Paper discovery is highly parallelizable — each search strategy is independent. Use a Workflow script to fan out 5 agents simultaneously:

```javascript
// Workflow: parallel-paper-discovery
phase('Discover')
const searches = await parallel([
  () => agent('Search backward citation chains from user papers', {label: 'backward-cite', phase: 'Discover'}),
  () => agent('Search forward citation chains from user papers', {label: 'forward-cite', phase: 'Discover'}),
  () => agent('Extract papers from Related Work sections', {label: 'related-work', phase: 'Discover'}),
  () => agent('Run keyword and synonym expansion searches', {label: 'keyword-expand', phase: 'Discover'}),
  () => agent('Scan arXiv/preprints for competition', {label: 'competition-scan', phase: 'Discover'}),
])
phase('Deduplicate')
const merged = await agent(`Deduplicate and rank these discovered papers: ${JSON.stringify(searches.filter(Boolean))}`, {label: 'merge'})
return merged
```

This runs 5 search strategies in parallel (~2-3 min wall-clock vs ~10-15 min sequential).

**Acceleration with /goal**:
If the initial parallel search finds fewer than 10 additional papers, use `/goal` to keep searching:

```
/goal find at least 15 relevant papers not in the user's original set, covering backward citations, forward citations, keyword variants, and preprint competition. Stop when 15 unique papers are found or all search strategies are exhausted.
```

This keeps Claude iterating (trying new keywords, deeper citation chains, alternative databases) until the coverage threshold is met — without manual re-prompting.

**Checkpoint**: Present missing papers to user. Ask:
- "I found these papers you might have missed. Should I add them to the corpus?"
- "There are [N] groups potentially competing on this. Are you aware of them?"
- Let user add/remove papers before proceeding.

---

### PHASE 0c: Gap Analysis & Future Work Study
**Goal**: Systematically extract gaps from the COMPLETE literature corpus (user's papers + discovered papers), detect convergent gaps, rank them, and generate candidate research questions.

**Agent**: `gap_analyzer`

**Process**:
1. Dispatch the gap_analyzer agent with ALL literature from `00_literature/` (user's original papers + papers discovered in Phase 0b)
2. The agent performs 5 steps:

   **Step 1 — Source-Level Gap Extraction**:
   - Read every paper's Limitations, Future Work, Discussion, and Related Work sections
   - Extract every gap with verbatim quote, source, and gap type
   - Types: Empirical | Methodological | Theoretical | Temporal | Geographic | Computational | Representational

   **Step 2 — Convergent Gap Detection**:
   - Group gaps by semantic similarity across papers
   - Flag convergence strength: STRONG (≥4 papers) | MODERATE (2-3) | WEAK (1)
   - Track gap evolution: getting narrower (partially addressed) or wider (growing urgent)?

   **Step 3 — Gap Ranking**:
   - Score each gap cluster on three dimensions:
     - **Feasibility (F, 1-5)**: How addressable with current tools/data/theory?
     - **Impact (I, 1-5)**: How much does filling this gap matter to the field?
     - **Freshness (Fr, 1-5)**: Is this a timely opportunity or a stale problem?
   - Composite: Priority = F × I × Fr (range 1-125)
   - HOT (80-125) | WARM (40-79) | COOL (15-39) | COLD (1-14)

   **Step 4 — Research Question Generation**:
   - From the top 2-4 HOT/WARM gaps, generate specific, falsifiable research questions
   - Each RQ includes: grounding gap, priority score, expected contribution type, minimum viable result, candidate venues

   **Step 5 — Gap-Dogma Alignment Hints**:
   - For each RQ, assess whether it aligns with potential hidden dogmas
   - These hints give Phase 1 (dogma extraction) a head start

3. Save output to `novelty_engine/00_gap_analysis/gap_analysis_report.md`

**Acceleration with /workflows**:
When the corpus has 8+ papers, per-paper gap extraction benefits from parallelism. Use a Workflow pipeline: fan out extraction, then synthesize:

```javascript
// Workflow: parallel-gap-extraction
const papers = args  // array of paper filenames passed from the orchestrator

phase('Extract')
const perPaperGaps = await parallel(
  papers.map((paper, i) => () =>
    agent(
      `Extract all gaps, limitations, and future work items from this paper: ${paper}. Return structured gap entries with verbatim quotes, gap type, and specificity level.`,
      {label: `extract:${paper}`, phase: 'Extract', schema: GAP_EXTRACTION_SCHEMA}
    )
  )
)

phase('Synthesize')
const gapReport = await agent(
  `Merge these per-paper gaps into convergent clusters, rank by Feasibility × Impact × Freshness, and generate 2-4 candidate research questions: ${JSON.stringify(perPaperGaps.filter(Boolean))}`,
  {label: 'synthesize-gaps', phase: 'Synthesize'}
)
return gapReport
```

This extracts gaps from all papers simultaneously (~2 min for 15 papers vs ~8 min sequential), then synthesizes into convergent clusters.

**Checkpoint**: Present the ranked gap landscape and candidate RQs to user. Ask:
- "Do these gaps match your experience with this field?"
- "Which research question(s) align with your research interest?"
- "Are there gaps I missed that you know exist but aren't written in papers?"

---

### PHASE 0d: Go/No-Go Decision
**Goal**: Make an explicit decision on whether to proceed with research in this field, and if yes, define the research direction.

**Agent**: `topic_verifier` (go/no-go assessment step)

**Process**:
1. Compile all evidence from Phases 0a-0c:
   - Topic viability scores (Phase 0a)
   - Competition landscape (Phase 0b)
   - Gap landscape — number and quality of HOT/WARM gaps (Phase 0c)
   - Whether the user's original topic aligns with the highest-priority gaps
2. Compute composite assessment:
   - Weighted viability score (Maturity × 0.15 + Saturation × 0.25 + Tractability × 0.25 + Impact × 0.20 + Timing × 0.15)
   - Competition adjustment (+0.5 CLEAR FIELD, 0 LIGHT, -0.5 ACTIVE RACE, -1.0 CROWDED)
   - Gap quality bonus (+0.5 if ≥2 HOT gaps, +0.25 if ≥1 HOT gap, 0 otherwise)
3. Render verdict:

| Adjusted Score | Verdict | Action |
|---------------|---------|--------|
| ≥ 3.5 | **GO** | Proceed. Topic is viable, gaps are tractable, timing is right. |
| 2.5 – 3.4 | **PIVOT** | Topic has potential but needs reframing. Suggest specific pivot directions. |
| < 2.5 | **STOP** | Topic is not viable. Suggest alternative topics. |

4. If **GO**:
   - Map top gaps to solution approaches (extend existing / cross-domain / first-principles)
   - User selects 1-2 research questions to pursue
   - Selected RQs + gap-dogma alignment hints are passed to Phase 1
5. If **PIVOT**:
   - Present 2-3 alternative framings or adjacent topics
   - User selects a pivot direction → re-run from Phase 0a with new framing
6. If **STOP**:
   - Present 2-3 entirely different topic suggestions in the same broad area
   - User decides whether to restart with a new topic or end

Save to `novelty_engine/00_topic_verification/go_no_go_assessment.md`

**HARD GATE**: The pipeline does NOT proceed to Phase 1 without a GO verdict.

---

## STAGE II: IDEA GENERATION (Phases 1 → 3)

Only reached after a GO verdict. The research direction is now defined.

---

---

### PHASE 1: Dogma Extraction
**Goal**: Identify unstated foundational assumptions and their breaking points.

**Agent**: `dogma_extractor`

**Process**:
1. Dispatch the dogma_extractor agent with:
   - All literature from `00_literature/` (including papers discovered in Phase 0b)
   - The gap-dogma alignment hints from Phase 0c
   - The selected research question(s) from Phase 0d
2. The agent extracts 4-6 dominant unstated dogmas, each with:
   - The assumption itself
   - Where it hides in the literature
   - Why it persists
   - Its breaking point (exact failure scenario)
   - Severity rating (CRITICAL / HIGH / MODERATE)
   - Evidence of cracks
3. Save output to `novelty_engine/01_dogma_scan/dogma_scan.md`

**Checkpoint**: Present dogmas to user. Ask:
- "Do these ring true based on your domain knowledge?"
- "Are there dogmas I missed that you know practitioners take for granted?"
- "Which breaking points do you find most promising for novel work?"

Let the user adjust, add, or remove dogmas before proceeding.

---

### PHASE 2: Novelty Verification (Pre-Synthesis)
**Goal**: Confirm the breaking points haven't already been exploited in published work.

**Agent**: `novelty_verifier`

**Process**:
1. Dispatch the novelty_verifier agent with the dogma scan
2. For each breaking point, the agent searches:
   - Academic APIs (Semantic Scholar, OpenAlex, Crossref, arXiv) if available
   - Web search for existing work challenging these dogmas
   - Survey papers covering interdisciplinary approaches in the target domain
3. Each claim classified: NOVEL / PARTIALLY EXPLORED / ALREADY PUBLISHED / UNCERTAIN
4. Save output to `novelty_engine/02_novelty_check/novelty_verification.md`

**Gate**: 
- ALREADY PUBLISHED claims are dropped — inform user and suggest alternatives
- PARTIALLY EXPLORED claims proceed with differentiation requirements noted
- NOVEL and UNCERTAIN claims proceed
- If ALL claims are ALREADY PUBLISHED, return to Phase 1 with expanded literature

**Checkpoint**: Present verification results. User decides which claims to pursue.

---

### PHASE 3: Cross-Domain Synthesis
**Goal**: Generate hybrid methodologies by mapping external frameworks onto the target domain.

**Agent**: `cross_domain_synthesizer`

**Process**:
1. Load the cross-domain isomorphism catalog (`references/cross_domain_catalog.md`)
2. Dispatch the cross_domain_synthesizer agent with:
   - Verified breaking points from Phase 2
   - The cross-domain catalog as reference
   - User's target topic and constraints
3. The agent generates 2-3 hybrid methodologies, each with:
   - Donor discipline and framework identification
   - Formal isomorphism mapping (table format)
   - Core mechanism explanation
   - Method architecture (step-by-step)
   - Mathematical foundation skeleton
   - Novelty claim (what's new / borrowed / adapted)
   - Predicted advantages and known risks
4. Save output to `novelty_engine/03_hybrid_methods/hybrid_methods.md`

**Quality gate**: Every method must pass the synthesizer's quality checklist:
- [ ] Structural, not superficial mapping
- [ ] Donor discipline is genuinely distant
- [ ] Core mechanism is formalizable
- [ ] Method is testable
- [ ] Targets a CRITICAL or HIGH breaking point

**Checkpoint**: Present methods to user. Ask:
- "Which method(s) do you want to develop further?"
- "Does the cross-domain mapping make structural sense to you?"
- "Are there practical constraints I should factor in?"

User selects 1-2 methods to advance to formalization.

---

## STAGE III: FORMALIZATION & PROOF (Phases 4 → 4.5)

---

### PHASE 4: Mathematical Formalization & Algorithm Specification
**Goal**: Transform selected methods into rigorous formal specifications.

**Agent**: `math_formalizer`

**Process**:
1. Load the formalization requirements (`references/formalization_requirements.md`)
2. Dispatch the math_formalizer agent with:
   - Selected hybrid method(s) from Phase 3
   - The formalization requirements reference
   - Domain-specific standards (CS/ML, social science, natural science, etc.)
3. For EACH method, the agent produces:
   - **Formal setup**: Definitions, assumptions, problem statement
   - **Mathematical framework**: Core theorems with proof sketches, key lemmas, bounds/guarantees
   - **Algorithmic specification**: Pseudocode with I/O spec, complexity analysis, correctness argument
   - **Implementation considerations**: Numerical stability, parallelizability, parameter sensitivity
   - **Experimental design skeleton**: Baselines, metrics, datasets, statistical tests, ablation plan
4. Save output to `novelty_engine/04_formal_spec/formal_specification.md`

**IRON RULE**: No method passes this phase without:
- At least ONE theorem/proposition with proof sketch, OR
- At least ONE algorithm with pseudocode and complexity analysis
- Preferably BOTH

**Quality gate** (from formalization_requirements.md):
- [ ] Every variable formally defined before use
- [ ] Every assumption explicitly stated
- [ ] Non-trivial bounds provided
- [ ] Pseudocode is implementation-ready
- [ ] Statistical tests specified for experiments

**Enforcement with /goal**:
Use `/goal` to ensure the IRON RULE is satisfied before presenting to the user:

```
/goal the formal specification in 04_formal_spec/formal_specification.md contains: (1) all variables defined with set-builder or constructive definitions, (2) all assumptions listed as (A1), (A2)..., (3) at least one theorem with a proof sketch naming the proof technique, (4) at least one algorithm with pseudocode, time complexity, and correctness argument, (5) at least one non-trivial bound. Verify by reading the file and checking each criterion.
```

This keeps Claude iterating on the formalization — adding missing definitions, tightening proofs, expanding pseudocode — until all criteria are met. Only then is the checkpoint presented to the user.

**Checkpoint**: Present formal specification to user. This is the most technical checkpoint — ask:
- "Does the mathematical formulation capture what you intend?"
- "Are the assumptions reasonable for your domain?"
- "Is the experimental design feasible with your resources?"

---

### PHASE 4.5: Falsification Experiment Design & Implementation
**Goal**: Design experiments that try to DISPROVE the method, then generate runnable code.

This phase has two sub-phases:

#### Phase 4.5a: Falsification Design
**Agent**: `experiment_falsifier`

**Philosophy**: Popperian falsification — we don't try to prove the method works; we try to prove it doesn't. If it survives, that's real evidence.

**Process**:
1. Dispatch the experiment_falsifier agent with:
   - The formal specification from Phase 4
   - The dogma being inverted from Phase 1
   - The novelty claim from Phase 2
2. The agent produces a complete Falsification Experiment Design:
   - **Null Hypothesis ($H_0$)**: Exact quantitative condition where the method offers zero advantage
   - **Experimental Variables**: IV (what we manipulate), DV (what we measure), CV (what stays locked)
   - **Control vs Treatment**: Baseline gets every advantage; novel method gets handicaps
   - **3 Escalating Torture Tests**:
     - Test 1: Target a specific weakness
     - Test 2: More hostile than Test 1, different weakness
     - Test 3: Target the FUNDAMENTAL assumption (push the inverted dogma back toward original)
   - **Degradation Curve Protocol**: Sweep stress from benign → extreme, find the knee point
   - **Success Criteria**: Statistical tests, effect size thresholds, mandatory reporting
   - **Threats to Validity**: Internal, external, construct, statistical conclusion
3. Save to `novelty_engine/04_experiment/falsification_design.md`

**Key design rules**:
- Baseline gets BEST hyperparameters from literature (no strawmen)
- Novel method uses DEFAULT parameters from formal spec (no cherry-picking)
- Include an ABLATED version (novel method minus the key innovation)
- Include TRIVIAL baseline (random/naive — sanity check)
- All torture tests have explicit KILL CONDITIONS (metric thresholds where the method is declared failed)

**Checkpoint**: Present experiment design to user. Ask:
- "Are the torture tests targeting the right weaknesses?"
- "Is the null hypothesis fair — would you accept the result if the method fails?"
- "Do you have the compute resources for this experimental protocol?"

#### Phase 4.5b: Experiment Code Generation
**Agent**: `experiment_coder`

**Process**:
1. Dispatch the experiment_coder agent with:
   - The formal specification (Phase 4)
   - The falsification design (Phase 4.5a)
2. The agent generates a complete, runnable experiment codebase:

```
novelty_engine/04_experiment/code/
├── config.py                  # All hyperparameters, seeds, paths (frozen dataclass)
├── methods/
│   ├── novel_method.py        # Direct translation from Phase 4 pseudocode
│   ├── baseline_standard.py   # Strongest existing baseline
│   ├── baseline_ablated.py    # Novel method with innovation removed
│   └── baseline_trivial.py    # Random/naive sanity check
├── data/
│   ├── generator.py           # Synthetic data with known ground truth
│   └── stress_scenarios.py    # Torture test data generators
├── harness/
│   ├── runner.py              # Main experiment loop
│   ├── metrics.py             # All metric computations
│   └── statistical_tests.py   # Hypothesis tests, bootstrap CI, effect sizes
├── visualization/
│   ├── figures.py             # Publication-quality matplotlib figures
│   └── tables.py              # LaTeX + Markdown results tables
├── run_experiment.py          # Entry point: python run_experiment.py
├── run_torture_tests.py       # Torture tests: python run_torture_tests.py
└── requirements.txt           # numpy, scipy, matplotlib, pandas only
```

3. Code standards enforced:
   - Same interface for ALL methods (BaseMethod ABC)
   - Random seeds set everywhere (reproducible)
   - Immutable data structures (frozen dataclasses)
   - Assertions verify formal specification invariants
   - Publication-quality figures (colorblind-safe, ≥8pt font, vector output)
   - Both LaTeX and Markdown table output

**Quality gate**:
- [ ] `python run_experiment.py --quick` runs without errors (3 seeds)
- [ ] Novel method beats trivial baseline (sanity check)
- [ ] Same seed produces identical results (reproducibility)
- [ ] All figures render correctly

**Enforcement with /goal**:
Use `/goal` to keep fixing experiment code until it actually runs:

```
/goal run 'cd novelty_engine/04_experiment/code && pip install -r requirements.txt && python run_experiment.py --quick' successfully: exit code 0, novel method score > trivial baseline score, and two runs with --seed 42 produce identical primary metric values. Fix any import errors, type errors, or logic bugs between attempts.
```

This is the highest-value `/goal` in the pipeline — experiment code almost never works on the first attempt. `/goal` turns the fix-run-fix cycle from a manual grind into an automated loop that stops only when the code provably runs, passes sanity checks, and is reproducible.

**Checkpoint**: Present working code + initial results to user. Ask:
- "The quick run passed. Here are the sanity check results: [summary]. Ready for the full run?"
- "Do you want to modify any method parameters before the full run?"
- "Are there additional baselines you want to include?"

**Gate for proceeding**:
| Outcome | Action |
|---------|--------|
| Method survives all 3 torture tests | Strong evidence → proceed to Phase 5 |
| Method fails 1 torture test | Partial evidence → paper must scope claims; proceed with caveats |
| Method fails 2+ torture tests | Weak evidence → return to Phase 3 for redesign |
| Method fails to beat trivial baseline | Implementation bug → fix and re-run |

---

## STAGE IV: VALIDATION & PUBLICATION (Phases 5 → 7)

---

### PHASE 5: Stress Test (ARS Peer Review)
**Goal**: Subject the formalized AND experimentally tested method to rigorous simulated peer review.

**Integration point**: Hand off to ARS `/ars-reviewer`

**Process**:
1. Compile the complete method proposal from Phases 1-4.5 into a single document:
   - Background (from literature + dogma scan)
   - Novelty claim (from verification + synthesis)
   - Method (from formal specification)
   - Experimental evidence (from falsification experiments — include results, degradation curves, statistical tests)
2. Save compiled document to `novelty_engine/05_stress_test/method_for_review.md`
3. Invoke ARS reviewer: `/ars-reviewer` on the compiled document
4. ARS dispatches 5 independent reviewers:
   - Editor-in-Chief (journal fit, originality)
   - Methodology Reviewer (research design, statistical validity)
   - Domain Reviewer (literature coverage, theoretical framework)
   - Perspective Reviewer (cross-disciplinary impact, assumptions)
   - Devil's Advocate (logical fallacies, counter-evidence)
5. Save ARS review output to `novelty_engine/05_stress_test/ars_review.md`

**Gate**: 
- If reviews identify CRITICAL flaws in the mathematical formalization → return to Phase 4
- If reviews identify experimental design flaws → return to Phase 4.5
- If reviews identify the novelty claim is weaker than thought → return to Phase 2
- If reviews suggest structural improvements → incorporate and proceed

**Checkpoint**: Present review results to user with recommended actions.

---

### PHASE 6: Hardening & Final Proposal
**Goal**: Incorporate review feedback and produce the hardened methodology proposal.

**Process**:
1. Address each reviewer critique:
   - Mathematical objections → strengthen proofs, add lemmas, tighten bounds
   - Algorithmic objections → fix complexity issues, add edge cases, improve termination arguments
   - Novelty objections → sharpen differentiation from prior work
   - Feasibility objections → adjust experimental design
2. Produce the final hardened proposal with all corrections incorporated
3. Save to `novelty_engine/06_final_proposal/novel_methodology_proposal.md`

**Document structure**:
```
1. Title (compelling, rigorous technical name)
2. Abstract (context → gap → novel approach → expected impact)
3. Foundational Inversion (what dogma we break, with evidence)
4. Methodological Architecture (complete formal specification)
   4.1 Definitions and Assumptions
   4.2 Core Theorems / Algorithms
   4.3 Complexity Analysis / Bounds
   4.4 Correctness Arguments
5. Execution Blueprint
   5.1 Implementation pseudocode
   5.2 Experimental design with statistical tests
   5.3 Ablation plan
   5.4 Baseline comparisons
6. Limitations and Scope Conditions
   6.1 Where the method is expected to fail
   6.2 Formal conditions under which guarantees break
7. Cross-Domain Attribution
   7.1 What was borrowed from the donor discipline
   7.2 What required non-trivial translation
```

**Checkpoint**: Final user review before ARS paper production. This is the **go/no-go gate**.

---

### PHASE 7: ARS Full Paper Production (Optional)
**Goal**: Convert the hardened proposal into a full publication-ready paper via ARS.

**Integration point**: Hand off to ARS `/ars-full`

**Process**:
1. The hardened proposal from Phase 6 becomes the seed input for ARS
2. Invoke `/ars-full` which triggers the 10-stage ARS pipeline:
   - Stage 1: Deep research (expands literature around the novel method)
   - Stage 2: Paper writing (12-agent drafting pipeline)
   - Stage 2.5: Integrity check (AI failure modes gate)
   - Stage 3: Peer review (5-reviewer panel)
   - Stage 4: Revision
   - Stage 5: Re-review
   - Stage 6: Re-revision
   - Stage 4.5: Final integrity (PRISMA-trAIce + RAISE)
   - Stage 7: Formatting (LaTeX/DOCX/PDF)
   - Stage 8: Process summary + AI self-reflection

**Note**: ARS has its own mandatory checkpoints at each stage. The user will be prompted for approval at each ARS stage as well.

3. Final paper output saved to `novelty_engine/07_paper/`

---

## Phase Summary

| Phase | Agent/Skill | Input | Output | Gate |
|-------|------------|-------|--------|------|
| | **STAGE I: RESEARCH PREPARATION** | | | |
| 0a | topic_verifier | Topic + description + papers | Viability assessment (5 dimensions) | Framing OK? |
| 0b | topic_verifier | User's papers | Missing papers report + competition scan | User reviews discovered papers | `/workflows` + `/goal` |
| 0c | gap_analyzer | Complete corpus | Ranked gap registry + candidate RQs | User selects RQ(s) | `/workflows` |
| 0d | topic_verifier | All Phase 0a-0c evidence | GO / PIVOT / STOP verdict | **HARD GATE** |
| | **STAGE II: IDEA GENERATION** | | | |
| 1 | dogma_extractor | Corpus + gap hints + selected RQ | 4-6 dogmas with breaking points | User validates dogmas |
| 2 | novelty_verifier | Dogma scan | Novelty verification report | Drop ALREADY PUBLISHED |
| 3 | cross_domain_synthesizer | Verified breaking points | 2-3 hybrid methodologies | User selects methods |
| | **STAGE III: FORMALIZATION & PROOF** | | | |
| 4 | math_formalizer | Selected methods | Formal specs (theorems + algorithms) | IRON RULE: math or algo required | `/goal` |
| 4.5a | experiment_falsifier | Formal spec + dogma | Falsification design (H₀, torture tests, kill conditions) | User validates fairness | |
| 4.5b | experiment_coder | Formal spec + falsification design | Runnable Python experiment code | Code runs, sanity checks pass | `/goal` |
| | **STAGE IV: VALIDATION & PUBLICATION** | | | |
| 5 | ARS /ars-reviewer | Compiled proposal + experiment results | 5-reviewer report | Critical flaws → loop back |
| 6 | (orchestrator) | Review + formal spec + experiment evidence | Hardened final proposal | User go/no-go |
| 7 | ARS /ars-full | Hardened proposal | Publication-ready paper | ARS checkpoints |

## Partial Execution

Users can run individual phases, in words or with a one-word argument
(`verify`, `discover`, `gaps`, `assess`, `dogma`, `formalize`, `falsify`,
`experiment`, `stress-test`, `paper`; no argument = full pipeline from Phase 0a):
- "Verify this topic" → Phase 0a only (topic viability check)
- "Find papers I'm missing" → Phase 0b only (paper discovery)
- "Analyze gaps in these papers" → Phase 0c only (gap analysis + RQ generation)
- "Should I pursue this topic?" → Phase 0a-0d (full research preparation)
- "Just extract dogmas from these papers" → Phase 1 only
- "I already have an idea, formalize it" → Phase 4 only (skip ideation)
- "Design experiments to prove/disprove this method" → Phase 4.5 only
- "Generate experiment code for this design" → Phase 4.5b only
- "Review and stress-test this method" → Phase 5 only
- "Turn this proposal into a paper" → Phase 7 only

## Error Recovery

- If Phase 0a scores topic poorly → suggest reframing or alternative topics
- If Phase 0b finds heavy competition → adjust viability score; may trigger PIVOT
- If Phase 0c finds no HOT or WARM gaps → expand literature via ARS, re-run Phase 0c
- If Phase 0d verdict is PIVOT → user reframes topic, re-run from Phase 0a
- If Phase 0d verdict is STOP → user chooses alternative topic or ends
- If Phase 2 finds ALL claims already published → return to Phase 0c, check if different gaps are available
- If Phase 4 cannot formalize a method → the method is likely too vague; return to Phase 3 with more constraints
- If Phase 4.5 torture tests fail the method → return to Phase 3 for redesign (if fundamental) or Phase 4 (if fixable)
- If Phase 4.5b code doesn't run → fix implementation bugs; if algorithm is inherently unimplementable, return to Phase 4
- If Phase 5 reviewers reject the mathematical foundation → return to Phase 4 with reviewer feedback
- If Phase 5 reviewers reject the experimental design → return to Phase 4.5a with reviewer feedback
- If the user is unsatisfied at any checkpoint → loop back to the relevant phase

## Token Budget Estimate

| Phase | Estimated tokens | Model |
|-------|-----------------|-------|
| 0a (Topic verification) | ~30K | Opus |
| 0b (Paper discovery) | ~40K | Opus |
| 0c (Gap analysis + RQ gen) | ~50K | Opus |
| 0d (Go/no-go assessment) | ~15K | Opus |
| 1 (Dogma extraction) | ~30K | Opus |
| 2 (Novelty verification) | ~40K | Sonnet |
| 3 (Cross-domain synthesis) | ~50K | Opus |
| 4 (Math formalization) | ~60K | Opus |
| 4.5a (Falsification design) | ~40K | Opus |
| 4.5b (Experiment code gen) | ~80K | Opus |
| 5 (ARS review) | ~80K | Opus |
| 6 (Hardening) | ~40K | Opus |
| 7 (ARS full paper) | ~200K+ | Opus |
| **Total (full pipeline)** | **~785K** | **~$14-20** |

## Acceleration Mechanisms

The pipeline integrates two Claude Code mechanisms to speed up specific phases without bypassing human checkpoints.

### /goal — Automated Completion Loops

`/goal` sets a measurable condition and keeps Claude working turn after turn until a fast evaluator confirms the condition is met. Used for phases where the work is grind-until-done (not judgment calls).

| Phase | /goal condition | Why it helps |
|-------|----------------|-------------|
| 0b (Paper Discovery) | "Find ≥15 relevant papers not in user's set, covering backward/forward citations, keyword variants, and preprints. Stop when 15 found or all strategies exhausted." | Paper discovery requires iterating through search strategies — `/goal` automates the retry-and-expand loop |
| 4 (Math Formalization) | "formal_specification.md contains: all variables defined, assumptions listed, ≥1 theorem with proof sketch, ≥1 algorithm with complexity, ≥1 non-trivial bound." | Enforces the IRON RULE automatically — Claude keeps adding missing definitions and tightening proofs until ALL criteria pass |
| 4.5b (Experiment Code) | "run_experiment.py --quick exits 0, novel method beats trivial baseline, same seed produces identical results." | Experiment code almost never works on first attempt — `/goal` turns the fix-run-fix cycle into an automated loop |

**When NOT to use /goal**: Phases with human checkpoints (0a, 0d, 1, 3, 5) — these require judgment that should not be automated.

### /workflows — Parallel Multi-Agent Orchestration

`/workflows` runs a JavaScript script that fans out many subagents in parallel. Used for phases where independent subtasks can run simultaneously.

| Phase | Workflow pattern | Speedup |
|-------|-----------------|---------|
| 0b (Paper Discovery) | 5 parallel search agents (backward cite, forward cite, related work, keyword expand, competition scan) → 1 dedup agent | ~5x (2-3 min vs 10-15 min) |
| 0c (Gap Analysis) | N parallel extraction agents (one per paper) → 1 synthesis agent that merges into convergent clusters | ~4x for 15+ paper corpus (2 min vs 8 min) |

**When NOT to use /workflows**: Sequential phases where each step depends on the previous (1→2→3), or phases that need holistic cross-paper analysis from a single agent (Phase 1 dogma extraction).

### Decision Guide

```
Is the work parallelizable (independent subtasks)?
  YES → /workflows (fan out agents)
  NO  ↓
Is the work grind-until-done with verifiable end state?
  YES → /goal (automated completion)
  NO  ↓
Does it need human judgment at a checkpoint?
  YES → Normal phase (no acceleration)
  NO  → Normal phase (single agent call)
```

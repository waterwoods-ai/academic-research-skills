# Big-4 operating model: evidence first

Decided by the PI on 2026-11-20, after two real rejections of the same paper (IEEE S&P
2027 #869, NDSS 2027 #2609) and the process audit of 2026-11-03 (18 projects, 67
simulated review rounds, no Big-4 acceptance). Both real panels agreed the problem was
timely; both rejected on evidence and contribution, not on writing. Sixteen internal
rounds between the two submissions fixed the specification gaps, closed every evidence
gap by narrowing a sentence, and lowered the scores.

**Principle.** A Big-4 paper is a finding the community did not have, supported by
evidence on real systems at a scale a reviewer accepts. Writing and simulated review
polish a finding; they do not produce one. The lab's time goes to the finding and its
evidence. This file overrides any stage rule that conflicts with it.

## 1. Portfolio: at most two active papers

- At most **two** projects are ACTIVE at a time. Every other project is FROZEN with a
  one-line reason and a reevaluate-when condition in its `decisions.md`.
- A third project starts only when an active one is submitted, frozen or killed by a
  recorded PI decision. Agents do not start work on a frozen project.
- The active list is in `lab_capacity.md` at the research root (PI-owned). If the file
  is missing, ask the PI which two projects are active before any stage work.

## 2. Paper types the lab takes on

The lab takes on **measurement, attack and defense** papers (PI, 2026-11-20). No type
is excluded. What differs is the evidence each type owes, and the lab's means (two
shared RTX 4090 hosts, no testbed, no device fleet, one PI) decide whether a given
topic can pay for it:

| Type | Evidence a Big-4 panel expects |
|---|---|
| **Measurement** of a real software or service ecosystem | the population (hundreds to thousands of real artifacts), a reproducible pipeline, findings that hold across it |
| **Attack / vulnerability discovery** on real, deployed or production-grade systems | confirmed flaws or working attacks on named real systems, responsible disclosure, root-cause taxonomy |
| **Defense** | a real system or testbed, the cheapest existing control as baseline, every designed component evaluated, adaptive attackers, harm demonstrated without the defense and prevented with it, the operating cost (false positives, overhead) across settings |
| **Benchmark / SoK** | a measurement finding that stands by itself; case by case, PI decides |

The paper type is named on the gap card at S1.5; the evidence bar (section 3) takes
its scale from exemplars of that type and its floor from that type's defect list. A defense paper is the most expensive of the three
for this lab: its bar is checked first against what the lab can run. A topic of any
type whose closing experiment needs a testbed, devices or data the lab lacks is
FILLED-FOR-US (`gap_deep_dive_protocol.md` test 3), whatever its novelty.

## 3. The evidence bar: exemplars and the type's defect list, set before the build

At S1.5, with the gap card, Claude writes `evidence_bar.md`. It has two parts and the
closing experiment must pass both.

**Part A, exemplars: how much evidence.**

1. Pick **three accepted papers of the same type** from the last three years of the
   Big 4 (the target venue first). Peruse each (`paper_dissection_protocol.md`).
2. Record for each: number and kind of real systems, scale (n), baselines, adaptive or
   adversarial evaluation, disclosure, artifact.
3. On each row the project is at least at the level of the weakest of the three.

The exemplars set the scale and nothing else. A weakness in an exemplar is not a
licence to repeat it: published Big-4 papers carry known defects (every one of 30
top-venue ML-security papers had at least three of the ten pitfalls of Arp et al.;
tier-1 systems-defense papers averaged five benchmarking crimes in van der Kouwe et
al.), and reviewers reject on the defect they see, not by comparison with what was
accepted before (Soneji et al., S&P 2022: 52 distinct red flags, far more concrete
than any acceptance criterion).

**Part B, defect list: what must not be wrong.** Every item below that applies to the
paper type gets one line in `evidence_bar.md`: how the closing experiment meets it, or
why it does not apply. "Stated as a limitation" does not meet an item.

| Applies to | The closing experiment must show |
|---|---|
| **Every type** | The kind of claim is named: prevalence, exploitability, root cause, generality, or harm prevented. A finding or a tool is a result, not a claim. |
| | Real systems. Simulation or emulation only with evidence of what it stands for, and never as the only target of a headline claim. |
| | Baselines that are current, configured at their best, and include the simplest method that could work. |
| | Repeated runs with the number of trials stated, variance or confidence intervals, and a statistical test whose assumptions hold. |
| | Each result explained: outliers and surprising numbers investigated, a null result traced to its cause from the raw data. |
| | A threat model that fixes the attacker's knowledge, capabilities and budget, and does not change between sections. |
| | Ethics and disclosure analysed when the project starts (stakeholders, harm, consent, vendor contact), not written at submission. |
| | Every table and figure regenerable from the artifact by someone outside the project. |
| **Defense** | How far the bar is raised and what attack surface remains. |
| | An adaptive attacker who knows the defense and was designed against it. |
| | Harm reached without the defense and prevented with it. |
| | The full cost on a realistic workload: false positives and negatives, latency, memory; absolute numbers; several operating points. |
| | Every designed component evaluated, or removed from the design. |
| **Attack / vulnerability discovery** | Target selection justified; targets are current versions of real systems. |
| | Impact measured across the affected population, not counted in CVEs. |
| | Disclosure before submission: to whom, when, and the outcome. |
| | For a bug-finding tool: ground-truth bugs, documented seeds, at least 10 trials of 24 hours or a justified timeout, ablations. |
| **Measurement** | The setup documented exactly (tools, versions, vantage points, dates), since small differences change results. |
| | Sampling bias and the time window stated, with what the sample represents. |
| | Calibration: outliers examined, consistency checks, more than one vantage point or method where the measurement can lose data. |
| | Minimal collection, identification and opt-out for active measurement; an ethics section even for reused data. |
| **Any paper that trains or evaluates a model** | The ten pitfalls of Arp et al. checked one by one (sampling bias, label inaccuracy, data snooping, spurious correlations, biased parameter selection, inappropriate baseline, inappropriate measures, base-rate fallacy, lab-only evaluation, inappropriate threat model); training data precedes test data in time and class ratios are realistic. |

Sources: Arp et al., "Dos and Don'ts of Machine Learning in Computer Security"
(USENIX Security 2022); van der Kouwe et al., "Benchmarking Crimes" (arXiv 2018);
VUSec, "Threats to Validity and Relevance in Security Research"; Carlini et al., "On
Evaluating Adversarial Robustness" (arXiv 2019); Klees et al., "Evaluating Fuzz
Testing" (CCS 2018); Schloegel et al., "SoK: Prudent Evaluation Practices for Fuzzing"
(S&P 2024); Pendlebury et al., TESSERACT (USENIX Security 2019); Paxson, "Strategies
for Sound Internet Measurement" (IMC 2004); Demir et al., "Reproducibility and
Replicability of Web Measurement Studies" (WWW 2022); Durumeric et al., "Ten Years of
ZMap" (IMC 2024); Partridge and Allman, "Addressing Ethical Considerations in Network
Measurement Papers" (CACM 2016); the reviews of S&P 2027 #869 and NDSS 2027 #2609.
For a sub-area with its own published evaluation guidance, add that guidance to the
list in `evidence_bar.md`.

**If the closing experiment cannot pass both parts,** with its cost, the PI decides
before any build: tier-2 target by decision, or the project does not start.

Gate 1 refuses a project whose `evidence_bar.md` lacks either part. Codex checks the
file at the gap pre-review: are the exemplars of the same type, and is any Part B item
answered by a limitation instead of evidence.

## 4. Time goes to evidence

| Phase | Share of the project | Ends with |
|---|---|---|
| Gap, deep-dive, four tests, evidence bar, gap pre-review | 2–3 weeks | Gate 1 |
| Evidence: core experiment first, then the rest | 2–4 months | headline result |
| Writing | last ~3 weeks | draft |
| Internal review | at most 3 rounds | submission decision |

Agent effort follows the same split: Claude and GLM spend most of their hours
collecting evidence (scanning the ecosystem, reproducing baselines, running
experiments, preparing disclosures); Codex spends most of its hours attacking the gap
and the closing experiment before the build.

## 5. No headline result, no paper

- Drafting starts only when the **headline result** exists: one sentence a reviewer
  would cite, with the table or figure that supports it, from the evidence ledger.
- At Gate 1 the PI sets a **headline date**. On that date, without the result: the PI
  decides kill, pivot (back to S1.5) or one dated extension. The direction check
  (`gap_deep_dive_protocol.md` Part C) is written for that decision. Narrowing the
  claim until some result fits it is not an outcome.

## 6. Review is bounded and calibrated by real outcomes

- **At most three scientific rounds per draft.** Packaging items (artifact links,
  formatting, bundle contents) go to a checklist and never open a round.
- **An internal Accept is not a submission decision.** It means "ready for a human
  read". Before submission at least one human (the PI or an outside reader) reads the
  paper cold and the PI records the decision.
- **Calibration record.** After every real review, append to `review_calibration.md`
  at the research root: venue, real scores, the internal panel's last verdict, each
  real concern the internal panel had not raised, and each concern the internal rounds
  had closed by wording. Reviewer #2 reads this file before every internal round.
- **Resubmission table.** Before a rejected paper is submitted again, every concern of
  the real reviews gets a row in `resubmission_table.md`: concern, kind (evidence /
  specification / presentation), how it was closed, where the evidence is. An evidence
  concern closed only by wording keeps the paper out of a venue of the same tier; the
  PI decides lower tier or more work.

## 7. What success is measured by

Not acceptance at the first try: Big-4 acceptance rates are below 20% and good papers
are often submitted more than once. The measure after each real review is whether the
scores moved up and whether a reviewer argued for the paper. A paper that returns from
a second venue with the same evidence concerns has not been revised; it has been
reworded.

## Who does what

| Item | Does | Checks | Decides |
|---|---|---|---|
| Active list, freezes | PI | Claude (reports stale ACTIVE projects) | PI |
| Evidence bar: three exemplars and the type's defect list | Claude | Codex (gap pre-review) | PI at Gate 1 |
| Headline date and its decision | Claude (direction check) | Codex (opinion) | PI |
| Round cap, human read | Claude (counts, stops at 3) | Codex | PI |
| Calibration record, resubmission table | Claude | Codex | PI before resubmission |

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

Chosen for the evidence the lab can afford (two shared RTX 4090 hosts, no testbed, no
device fleet, one PI). Until the PI changes this:

| Type | Evidence a Big-4 panel expects | In scope |
|---|---|---|
| **Measurement** of a real software or service ecosystem | the population (hundreds to thousands of real artifacts), a reproducible pipeline, findings that hold across it | yes |
| **Vulnerability discovery / attack** on real, deployed or production-grade software | confirmed flaws in named real systems, responsible disclosure, root-cause taxonomy | yes |
| **Defense system** | a real system or testbed, the cheapest existing control as baseline, adaptive attackers, demonstrated harm prevented | not now |
| **Benchmark / SoK** | only with a measurement finding that stands by itself | case by case, PI decides |

A topic whose closing experiment needs a testbed, devices or data the lab lacks is
FILLED-FOR-US (`gap_deep_dive_protocol.md` test 3), whatever its novelty.

## 3. The evidence bar comes from exemplars, set before the build

At S1.5, with the gap card:

1. Pick **three accepted papers of the same type** from the last three years of the
   Big 4 (the target venue first). Peruse each (`paper_dissection_protocol.md`).
2. Record for each, in `evidence_bar.md`: number and kind of real systems, scale (n),
   baselines, adaptive or adversarial evaluation, disclosure, artifact.
3. The project's bar is the **weakest of the three on each row**. The closing
   experiment must meet it, with its cost. If it cannot, the PI decides before any
   build: tier-2 target by decision, or the project does not start.

Gate 1 refuses a project without `evidence_bar.md`.

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
| Evidence bar from three exemplars | Claude | Codex | PI at Gate 1 |
| Headline date and its decision | Claude (direction check) | Codex (opinion) | PI |
| Round cap, human read | Claude (counts, stops at 3) | Codex | PI |
| Calibration record, resubmission table | Claude | Codex | PI before resubmission |

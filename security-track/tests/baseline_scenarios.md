# Baseline Failure Scenarios (Custom — Security Track)

> RED-phase test prompts for the security-track behavioral additions, per the
> superpowers writing-skills discipline: each scenario names the mistake an
> agent makes WITHOUT the skill loaded, and the behavior the skill must
> produce. Manual verification — paste the scenario into a fresh session
> (Claude Code / Codex / opencode) and compare against "expected". Not wired
> to CI (behavior checks, not static lint).

## S-1 · Security framing (`security_framing_protocol.md`)

**Prompt:** "My idea: a new perturbation method that makes an image
classifier misclassify with 98% success. Is this a strong security
contribution for S&P?"

- **Baseline failure:** praises the 98% number and the novelty of the
  perturbation; treats a higher attack-success rate as the contribution.
- **Expected with skill:** emits `SECURITY FRAMING RISK`; runs the framing
  chain; asks *which security property is actually violated, for whom, under
  what realistic threat model*; notes a higher ASR ≠ a security contribution.

## S-2 · Threat model stress (`threat_model_workbench.md`)

**Prompt:** "My defense assumes the attacker has white-box access to the
model and unlimited queries. Under that, my method blocks the attack. Write
the threat model section."

- **Baseline failure:** writes the section accepting the white-box +
  unlimited-query assumptions as given.
- **Expected with skill:** fills the 11 fields; runs the three stress tests —
  flags the white-box + unlimited-query assumptions as needing deployment
  justification (custom-fit test), asks whether a weaker attacker still
  motivates the defense, and whether a stronger attacker makes it trivial.

## S-3 · Single-paper dissection (`paper_dissection_protocol.md`)

**Prompt:** "Here is a paper [attach/point to one]. Summarize the related
work."

- **Baseline failure:** produces a flat prose summary of the paper's related
  work section.
- **Expected with skill:** recognizes a single-paper deep-read request;
  produces the 8-question skeleton (Threat Model separated from Assumptions),
  reconstructs the argument chain and names the weakest link, labels the
  Introduction P1–P7, and lists the reviewer questions the evaluation
  invites — not a related-work paraphrase. (If the user truly wants
  multi-paper breadth, it routes to `perspective_retrieval_protocol.md`.)

## S-4 · Novelty type (`security_framing_protocol.md`)

**Prompt:** "We release a new 50k-sample dataset of IoT malware. That's our
main contribution. Good enough for CCS?"

- **Baseline failure:** treats the dataset as an automatic contribution.
- **Expected with skill:** applies "a new dataset ≠ automatically a security
  contribution"; asks what the security community *learns* that it did not
  know before; classifies the novelty type and checks framing risk.

## S-5 · Evaluation completeness (`research_loop_protocol.md` S4 checklist)

**Prompt:** "My attack works on the target system. Evaluation done, right?"

- **Baseline failure:** agrees the evaluation is complete.
- **Expected with skill:** pulls the attack-paper checklist — asks for
  adaptive-defense results, weaker/stronger-attacker sweeps, stealthiness,
  transferability, cost, failure cases; closes with "what experiment would a
  hostile reviewer request?"

## S-6 · Method-substitution under failure (`method_change_provenance.md`)

**Prompt:** "My OTA problem: model params are altered before signing, so the
signature is valid over malicious params; my behavior-detection method
underperforms. Let's instead add a separate signature scheme and call it
D-Crypto."

- **Baseline failure:** accepts the substitute, adopts the name "D-Crypto",
  presents it as the new contribution.
- **Expected with skill:** runs the three provenance checks — (1) scenario
  fidelity: a separate signature addresses build/provenance integrity, a
  different pipeline point; flags it may not solve "first signing already
  covered tampered params"; (2) prior-art identity: strips the name, matches
  it to in-toto/SLSA/TUF/Uptane; verdict RENAME; (3) demands ADOPT+CITE
  (novelty dropped) or a proven genuine delta. Does not let a renamed
  known method pass as novel.

## S-7 · Self-invented taxonomy (`security_framing_protocol.md`)

**Prompt:** "I'll classify the attacks into three types D1, D2, D3 that I
define. Write the taxonomy section."

- **Baseline failure:** writes the section using the self-invented D1/D2/D3.
- **Expected with skill:** first searches for an established taxonomy for
  this attack class; if one exists, adopts+cites it and maps onto it; only
  keeps a self-made scheme with justified lineage; warns that an
  unprovenanced taxonomy is a reviewer attack surface.

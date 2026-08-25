# Security Subfield Knowledge Index (L1) — Custom, Security Track

> An always-surfaced map of security research subfields: for each, the one
> load-bearing best practice and the *subfield-specific reviewer bar* a Big-4
> panel applies. Adapted from AIBuildAI-2's two-level knowledge system
> (arXiv:2605.27873): this is the L1 index; the L2 evolution engine is the
> S8.5 Retrospective in `research_loop_protocol.md`, which proposes edits
> here as real projects finish. Read this at S1/S2/S3/S7 to load the bar the
> paper will actually be judged against.
>
> **Provenance discipline:** rows are seeded from durable community norms
> (Carlini/Athalye adaptive-eval, Arp et al. ML-security pitfalls, the
> 219-best-paper calibration, official CFPs). A row edited by the L2
> retrospective must cite the project + venue that produced the lesson; a
> lesson from one paper is a hypothesis, not a law — mark it `provisional`
> until a second project confirms it.

> **Dual layer (RW atoms pattern):** the canonical machine store is
> `knowledge_index.jsonl` (one reviewer-bar atom per row, with `applies_when`
> / `fails_when` / `severity` / `status`); this `.md` is its rendered human
> view. The S8.5 retrospective appends/promotes JSONL rows;
> `scripts/check_knowledge_index.py` guards the two layers against drift and
> keeps `status` orthogonal to `confidence`.

## How to use

1. Identify the paper's subfield(s) — many papers span two (e.g. an IoT
   firmware side-channel is IoT/embedded + side channels).
2. Load each row's **reviewer bar** as a hard constraint into S3 (Contribution
   Card), S4 (validation plan), and S7 (stress test).
3. Missing your subfield? Add a row via the S8.5 retrospective, not ad hoc.

## L1 cards

| Subfield | One load-bearing best practice | The subfield-specific reviewer bar |
|---|---|---|
| **Threat modeling (cross-cutting)** | State adversary capability/knowledge/position explicitly; declare out-of-scope | Assumptions realistic for the deployment; weaker-attacker still motivates it, stronger-attacker doesn't trivialize it (`threat_model_workbench.md`) |
| **Adversarial ML (attacks/defenses)** | Evaluate against an ADAPTIVE, defense-aware adversary | No adaptive eval = desk-level reject (Carlini & Wagner 2017; Athalye 2018); strongest published attacks correctly tuned; no gradient masking |
| **ML-for-security detection** | Realistic base rates + temporally-split data | Base-rate fallacy addressed; no future leakage; false-positive cost at deployment scale (Arp et al., "Dos and Don'ts of ML in Security", USENIX'22) |
| **Fuzzing / bug-finding / tooling** | Find real, deeper bugs on real targets vs strongest existing fuzzers | Real-world targets not toys; bugs triaged/reported (CVEs); fair baseline tuning + seed/coverage methodology (SoK: Prudent Fuzzing Eval, S&P'24) |
| **Side channels (micro-arch / timing)** | Constant-time claims proven, not asserted | Real hardware (not simulation-only); leakage model stated; end-to-end key/secret recovery, not just a distinguisher |
| **CPS / ICS security** | Real testbed or hardware-in-the-loop; quantify PHYSICAL consequence | Physical impact measured, not packet-level success; control-loop latency/safety budget respected; sim needs a fidelity argument |
| **IoT / embedded / firmware** | Device/vendor diversity matched to the generality claim | Root cause is a vulnerability CLASS not one vendor's bug; realistic attacker position (LAN? pairing-time? internet-facing?); disclosure + CVEs |
| **Supply-chain / OTA / attestation** | Position against in-toto / SLSA / TUF / Uptane / Sigstore / Notary | A "new" signing/attestation scheme not positioned against these reads as a RENAME (`method_change_provenance.md`); state the pipeline point you protect |
| **Crypto / formal methods** | Validation is a PROOF (increasingly machine-checked), not an experiment | Soundness of the proof + cryptanalytic effort; empirical work here is performance, not correctness (research_loop S4 exception row) |
| **Network / protocol security** | Attack works over the real protocol against a real stack | Realistic on-path/off-path position; standards-compliant target; measurement at internet scale where claimed |
| **Web / application security** | Prevalence measured at scale + working end-to-end PoC | Large-scale prevalence study or real-site PoC; responsible disclosure; not a single hand-built demo |
| **Measurement / empirical studies** | Rule out that the finding is a measurement artifact | Multiple vantage points; ground-truth validation; robustness to methodology choices; scanning ethics/IRB |
| **Privacy (PETs / inference attacks)** | Quantify the privacy property against a stated adversary | Realistic auxiliary-knowledge assumption; privacy metric matches the threat (not just "similarity"); utility cost stated |
| **Usable security / human factors** | Methodological rigor + disconfirming evidence sought | Sampling justified; inter-coder reliability; rival interpretations considered; IRB |
| **SoK / systematization** | A genuine organizing insight, not a survey | New taxonomy with lineage (not self-invented, `security_framing_protocol.md`); note CCS does not accept SoK |
| **Disclosure / ethics (cross-cutting)** | Coordinated-disclosure narrative with dates/CVEs/embargo | Adequacy judged, not just presence; IRB not a safe harbor; USENIX Ethics Considerations section (`security_paper_conventions.md`) |

## Per-venue quick reminders (details in `big4_venue_profiles.md`)

- S&P: Accept/Reject only; public meta-review. NDSS: only venue with Major
  Revision; most IoT/embedded/protocol-friendly. CCS: ML-and-Security track,
  Open Science appendix MUST, no SoK. USENIX: Ethics + Open Science, largest
  volume, pragmatic systems culture.

## Provenance log (L2 appends here)

Structured lessons distilled by the S8.5 retrospective land in
`knowledge_notes/` and, once confirmed, promote into the L1 cards above with
a citation to the originating project + venue. Until promoted they stay in
`knowledge_notes/` as `provisional`.

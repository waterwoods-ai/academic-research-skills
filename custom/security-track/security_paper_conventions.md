# Systems-Security Paper Writing Conventions (Custom — Security Track)

> Custom overlay for ARS, `dev` branch only. How Big-4 security papers are
> written, where that differs from the ML/journal conventions the stock ARS
> skills assume. Calibrated for CPS / IoT / AI-security research.

## Canonical structure (attack or defense paper)

1. **Abstract** — problem, gap, approach, headline result with numbers, impact
   (e.g., "affects N devices / M vendors", "CVE-XXXX assigned").
2. **Introduction** — motivation → limitation of prior work → insight →
   explicit contribution list (3–5 bullets, each falsifiable). End with an
   artifact-availability sentence when open-sourcing.
3. **Background** — only what a general security reviewer needs; assume no
   domain expertise in your specific CPS/IoT stack.
4. **Threat Model** (own section, non-negotiable) — see below.
5. **Design / Attack methodology** — system overview figure early; design
   goals as named properties (G1, G2, ...).
6. **Implementation** — LoC, languages, hardware/testbed inventory; enough
   detail for artifact evaluation.
7. **Evaluation** — research questions (RQ1..RQn) mapped to experiments.
8. **Discussion** — limitations, generalizability, countermeasures (for
   attacks), deployment cost (for defenses).
9. **Related Work** — grouped thematically; positioning table if crowded field.
10. **Ethics Considerations** — mandatory at USENIX, expected everywhere.
11. **Conclusion** — short; no new claims.

## Threat model section

The single biggest structural difference from ML papers. It must state:

- **Adversary capabilities and position** — network access? physical access?
  co-located app? compromised sensor? Be exhaustive and explicit.
- **Adversary knowledge** — white/gray/black-box, and *why that level is
  realistic for the deployment scenario* (AI-sec papers die here: a
  white-box assumption needs deployment justification).
- **Out of scope** — state it explicitly; reviewers respect declared
  boundaries and punish silent ones.
- **Trust assumptions** — trusted components, TCB size.

CPS/IoT specifics: physical-access and supply-chain assumptions must be
stated; "attacker on the same LAN" needs justification post-segmentation-era.
AI-sec specifics: specify the attack surface (training data, model weights,
query API, physical sensor channel) and the adaptive-adversary setting.

## Evaluation norms (what reviewers check)

- **CPS:** real testbed or hardware-in-the-loop strongly preferred; pure
  simulation needs a fidelity argument. Safety implications quantified
  (e.g., physical consequence of the attack, not just packet-level success).
- **IoT:** device diversity (N devices, M vendors) determines perceived
  generality; lab-only single-device studies read as case studies.
  Large-scale measurement needs an ethics-reviewed scanning methodology.
- **AI security:** adaptive attacks are the bar (attacker aware of the
  defense) — static-baseline-only evaluations are a standard rejection
  reason. Compare against published attack implementations, report compute,
  release code.
- End-to-end PoC beats component-level metrics. "We demonstrate the full
  attack on a real X" is worth more than any table.

## Ethics and responsible disclosure

- Offensive results: document vendor coordination — who was notified, when,
  response, CVE IDs, agreed embargo. A "we disclosed to all affected
  vendors on DATE; CVE-XXXX was assigned" paragraph is standard.
- Measurement studies: IRB status (or why exempt), opt-out honoring,
  data minimization, no interaction with production systems beyond need.
- Human subjects (user studies on IoT devices etc.): IRB approval stated.
- USENIX: dedicated "Ethics Considerations" + "Open Science" compliance
  sections are mandatory checklist items, drafted at outline time.

## Style deltas vs. the stock ARS (ML/journal) assumptions

| Dimension | Stock ARS default | Security Big-4 |
|---|---|---|
| Citation format | APA 7.0 prose citations | Numeric `[12]`, IEEE/ACM style |
| Layout | Journal / single column | Two-column conference LaTeX |
| Abstract | ~250w structured | ~200w, impact-led, unstructured |
| Named-section contract | IMRaD | Intro/Threat Model/Design/Eval/Discussion |
| Review target | Journal R&R letters | Rebuttal + major-revision criteria list |
| Anonymity | Often single-blind | Strict double-blind incl. artifacts |
| Word-count gates | Journal word limits | Hard page limits (12–13pp excl. refs) |

## Anonymization checklist (double-blind)

- Own prior work cited in third person ("Doe et al. [3]" not "our prior work").
- Artifact links anonymized (anonymous.4open.science or AE-provided channel).
- Acknowledgments, grant numbers, IRB institution names stripped.
- Vendor-disclosure narrative phrased without identifying the authors' org.
- PDF metadata scrubbed.

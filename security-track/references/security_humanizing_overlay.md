# Security Humanizing Overlay (Custom — Security Track)

> Calibrates the standalone **`academic-humanizer`** skill
> (AIScientists-Dev/academic-humanizer, MIT; builds on blader/humanizer +
> ARMS) for security-conference prose. That skill strips AI *tells* and
> matches claims to evidence while preserving every number, result, and
> citation — and it is NOT a tool for evading AI-use disclosure. This overlay
> keeps all of that and re-points its field defaults (which assume
> ML venues / NSF-NIH grants) at the Big-4 security venues, the same way the
> rest of the security-track re-points stock ARS. It is a **prose polish, run
> after content is frozen — never a content generator.**

## When to run it (and when NOT to)

- **Run at S8 (paper writing/polish) and on revision passes**, AFTER the
  Contribution Card claims and the Provenance Ledger numbers are frozen
  (`research_loop_protocol.md` S4 design freeze + `research_integrity_
  protocol.md` §1 pre-registration). It cleans wording; it must never be the
  step that first sets or changes a claim's substance.
- **Do NOT** run it to draft content, invent motivation, or generate claims.
  It edits prose you already stand behind.

## Register: security conferences, not ML venues or grants

Drive the humanizer's Layer 5 (voice/venue) to the **SECURITY REGISTER**:
IEEE/ACM two-column conference prose — S&P / NDSS / CCS / USENIX Security are
terse, direct, systems-precise, results-forward. This is NOT the ICLR/NeurIPS
default and NOT the Nature/PNAS expository register.

- **Skip Layer 6 (NSF/NIH funding-proposal mode) unless the user is actually
  writing a grant/proposal.** The user's default output is security
  *conference papers*, whose structure (Introduction / Threat Model / Design /
  Implementation / Evaluation / Discussion / Related Work / Ethics — see
  `security_paper_conventions.md`) is not an NSF/NIH grant. Apply the paper
  layers (1–5), not Layer 6, to a conference submission.

## Integrity binding (this overlay's hard constraints)

The humanizer's Layer 3 ("never invent, drop, or alter a number, equation, or
citation") stays absolute. In the security track it is TIGHTENED and EXTENDED:

- **Claim-strength moves in one direction only: down.** Layer 4 may only
  *downgrade* an over-claim to match its evidence (e.g. "prove" → "show").
  It may **never inflate** a claim — never "suggests" → "shows", never widen a
  scope, never strengthen a verb. Any wording near a frozen/pre-registered
  result must preserve the claimed magnitude exactly. This composes with the
  claim-strength ladder and `research_integrity_protocol.md`; it never
  overrides the numbers-from-ledger rule.
- **Preserve verbatim, like citations:** CVE IDs (`CVE-YYYY-NNNNN`), MITRE
  ATT&CK technique/tactic IDs (`Txxxx`, `TAxxxx`, ICS-matrix ids), formal
  threat-model quantifiers, theorem/lemma statements, algorithm and metric
  names, and defined terms. A polish pass does not touch an identifier
  (`cve_attack_mapping.md`).
- **Load-bearing scope hedges are Layer-3 protected.** "under our threat
  model", "for the devices we tested", "assuming a same-LAN attacker",
  "no prior work within our search" — these bound the claim and are NOT AI
  vagueness. Keep them; de-slopping must not delete a qualifier that a
  reviewer relies on (`threat_model_workbench.md`, search-bounded novelty).

## Security-specific tells to also catch (beyond the ML examples in the skill)

- **Threat-model prose:** keep adversary capability/knowledge/position
  statements crisp and consistent; do not "smooth" a capability claim into
  vagueness — an imprecise threat model is a standard reject
  (`security_reviewer_personas.md` R4).
- **Ethics / disclosure narrative:** de-slop it, but keep it SUBSTANTIVE
  (named stakeholders, dates, CVEs, embargo) — never trim it to boilerplate;
  a boilerplate ethics section fails the Phase-0 compliance check
  (`security_reviewer_personas.md` P0-1).
- **Significance hype vs. real threat:** replace "paves the way / paramount
  importance" with the concrete security consequence (which property is
  violated, for whom, under what conditions — the "so what" test in
  `threat_model_workbench.md`), not with more abstraction.

## Output

The humanizer returns cleaned text + a change report. In the security track
the report MUST additionally confirm: no CVE/ATT&CK ID altered, no claim
strengthened (only downgrades), no scope hedge removed, and Layer 6 not
applied to a conference paper. If any claim looked under-supported, it is
flagged for the author — never silently strengthened or papered over.

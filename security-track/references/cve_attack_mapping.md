# CVE & MITRE ATT&CK Mapping Protocol (Custom — Security Track)

> Security papers routinely connect to CVE and MITRE ATT&CK — it grounds the
> work in the real threat landscape, sharpens the threat model, and gives
> reviewers a shared frame. This protocol makes the check a first-class step:
> during research, ask whether a real mapping exists; if it does, establish
> it with a canonical, verifiable ID. It is NOT a decoration to sprinkle on —
> a wrong technique id or a fabricated CVE is a credibility hit, the same
> class of failure as a renamed method (`method_change_provenance.md`).

## IRON RULES

1. **Only real, verifiable references.** Every CVE (`CVE-YYYY-NNNNN`) must
   resolve on the CVE List / NVD; every ATT&CK id (`Txxxx`/`Txxxx.yyy`,
   tactic `TAxxxx`, group `Gxxxx`, software `Sxxxx`) must exist in the
   current ATT&CK version — state which version (e.g. ATT&CK v15,
   Enterprise/ICS/Mobile matrix). No invented or approximate ids.
2. **The mapping must actually hold.** Map to the technique the work truly
   exercises, not the nearest-sounding one. A forced or over-broad mapping
   (tagging T1059 because "there's a script somewhere") is worse than none —
   reviewers check.
3. **Absence is a valid, statable outcome.** If no CVE/ATT&CK relation
   genuinely applies (pure theory, a new attack class with no assigned
   technique yet), say so explicitly — do not manufacture one. Proposing a
   NEW technique/sub-technique is itself a contribution, but must be argued
   as an extension of the matrix with lineage, not a silent self-coinage
   (same discipline as taxonomy provenance in `security_framing_protocol.md`).

## When to run the check (and what to establish)

Run at M3 (threat model), S3 (Contribution Card), S4 (evaluation), and M8
(writing). Ask: does this work connect to a known vulnerability or a known
adversary behavior? Then, by paper type:

| Paper type | CVE relation | ATT&CK relation |
|---|---|---|
| **Attack / offensive** | If you found a new exploitable flaw, pursue a CVE (coordinated disclosure → CNA → id); cite it once assigned. If you exploit a known flaw, cite its CVE. | Map the attack to the ATT&CK **technique(s)** it realizes (tactic → technique → sub-technique). If it is a genuinely new behavior, argue a candidate technique. |
| **Defense** | Cite the CVE class(es) the defense addresses, if applicable. | State exactly which ATT&CK techniques the defense detects/prevents/mitigates — and, honestly, which it does NOT (adaptive-attacker bar still applies). |
| **Measurement / empirical** | Use CVEs as the population (e.g. coverage over a CVE set) with the query/date. | Use ATT&CK as the coding frame for observed behaviors; report inter-rater agreement if human-coded. |
| **ML-for-security detection** | Map detected threats to CVE/ATT&CK to show real-world relevance, not just dataset labels. | Map detection coverage to ATT&CK techniques; a gap in coverage is an honest limitation, not a hidden one. |
| **Crypto / formal** | Usually N/A — state it. | Usually N/A — state it. |

## How to establish and record the mapping

For each relation, record a row in `attack_map.md` (per project):

```
| Our element | Relation | Canonical ID | ATT&CK version | Evidence it holds | Verified |
|---|---|---|---|---|---|
| §5 spoofing attack | realizes | T0856 (Spoof Reporting Message) | ATT&CK v15 ICS | our PoC sends forged reporting msgs matching the technique's definition | NVD/ATT&CK checked <date> |
```

- **Verified** column is mandatory — like the numbers-from-ledger rule, an
  unverified id is not usable. Check the id against the live source and stamp
  the date (mirrors the deadline-calendar freshness discipline).
- In the paper, weave the ids into the Threat Model and Evaluation sections
  (an ATT&CK mapping table is common and reviewer-friendly); do not bolt a
  detached "ATT&CK appendix" with no in-text argument.
- For a defense, an ATT&CK coverage table (technique → detected/prevented/
  out-of-scope) is a strong, honest way to state scope.

## Domain anchor — CPS/IoT/OTA (your track)

Use the **ATT&CK for ICS** matrix for CPS/OT work (techniques are `Txxxx`
in the ICS matrix, e.g. manipulation of control, spoof reporting message),
not the Enterprise matrix. For OTA/supply-chain, connect to Enterprise
Supply Chain Compromise (T1195) and its sub-techniques, and to relevant CVEs
in the update/attestation stack — alongside the framework positioning
(in-toto/SLSA/TUF/Uptane) from `method_change_provenance.md`.

## Reviewer angle (why this matters at a Big-4 venue)

Reviewers use ATT&CK/CVE to sanity-check that a paper addresses a real
threat, not a contrived one. A correct mapping answers "is this a real
adversary behavior?" before they ask. A wrong/forced mapping does the
opposite — it signals the authors do not know the landscape. Establish the
relation when it genuinely exists; state its absence when it does not.

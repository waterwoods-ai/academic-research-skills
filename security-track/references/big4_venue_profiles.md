# Big-4 Security Venue Profiles (Custom — Security Track)

> Custom overlay for ARS, maintained on the `dev` branch only. Not part of upstream.
> Scope: the four top-tier security conferences, calibrated for research in
> **CPS security, IoT security, and AI/ML security**.
> Concrete deadline dates are NEVER stored here — they are pulled from
> https://sec-deadlines.github.io into `deadlines_current.md` by
> `fetch_deadlines.py` at every upstream sync. Page limits shift year to year;
> verify against the current CFP. Structural facts below are stable as of early 2026.

## Venue ranking context

Canonical ranking source: http://jianying.space/conference-ranking.html
(CIF-based, updated yearly; snapshot in `conference_ranking_2025.json`).
Big-4 CIF 2025: IEEE S&P 3.05 (#1), NDSS 2.46 (#3), ACM CCS 2.45 (#4),
USENIX Security 2.15 (#6). Acceptance rates 14.6%–19.1% (2016–2025 average).

---

## 1. IEEE S&P ("Oakland")

| Attribute | Value |
|---|---|
| Organizer / when | IEEE Computer Society TC-SP; May, San Francisco |
| Submission model | Multiple cycles per year — live dates: `deadlines_current.md` |
| Format | IEEE two-column (IEEEtran conference), ~13 pages **excluding** references and appendices |
| Anonymity | Fully double-blind; anonymize artifacts and cite own prior work in third person |
| Decisions | **Accept / Reject only** (all revision decisions abolished in 2024); early-reject round; every accepted paper gets a public <500-word meta-review + optional author response, with a shepherd striking concerns the camera-ready fixes |
| Ethics | Research Ethics Committee reviews flagged papers; ethics alone can reject; vendor disclosure required no later than the rebuttal deadline |
| Artifact evaluation | Yes — post-acceptance, badge system (Available / Functional / Reproduced) |
| Citation style | IEEE numeric `[1]` |

**Fit notes (CPS/IoT/AI):** S&P regularly publishes CPS/ICS attack + defense
papers and top-tier adversarial-ML work. Highest bar of the four for both
novelty and evaluation depth; a CPS paper without a physical or
high-fidelity testbed component is at a disadvantage. AI-security papers are
expected to evaluate against **adaptive adversaries**, not just static baselines.

## 2. NDSS

| Attribute | Value |
|---|---|
| Organizer / when | Internet Society (ISOC); February, San Diego |
| Submission model | 2 cycles per year — live dates: `deadlines_current.md` |
| Format | NDSS's own LaTeX template, ~13 pages excluding references and appendices |
| Anonymity | Double-blind |
| Decisions | Accept / Minor Revision / Major Revision / Reject — **the only Big-4 venue retaining a true Major Revision** (criteria-bound task list, same-cycle ~4–5-week resubmission, at most one per edition) |
| Ethics | Ethics statement expected; measurement and vulnerability studies scrutinized |
| Artifact evaluation | Yes — badge system |
| Citation style | IEEE-style numeric |

**Fit notes:** Strong network/systems flavor — historically the most receptive
of the four to IoT/embedded and protocol-level work (firmware analysis, IoT
platform security, automotive, wireless). Network-facing CPS work (e.g.,
ICS protocol security) fits well. AI-security papers appear but the
network/system angle should be foregrounded.

## 3. ACM CCS

| Attribute | Value |
|---|---|
| Organizer / when | ACM SIGSAC; October/November, rotating |
| Submission model | 2 rounds per year — live dates: `deadlines_current.md` |
| Format | ACM `sigconf` two-column, ~12 pages excluding references and well-marked appendices |
| Anonymity | Double-blind |
| Decisions | Accept / Minor revision / Reject (**no Major Revision category**; "Administrative Reject" = desk rejection); topic-track reviewing (submit to a named track); Minor revision resolves in the same cycle via a "separate note" mapping revisions to reviewer comments |
| Ethics | Ethics + responsible-disclosure paragraph expected for offensive results |
| Artifact evaluation | Yes — ACM badge system (Artifacts Available / Evaluated / Results Reproduced) |
| Citation style | ACM numeric |

**Fit notes:** Largest of the four (≈200 papers/year), broadest topical spread,
and has an explicit ML-and-security track — the highest-volume Big-4 outlet
for AI-security work. CPS/IoT papers land in the applied-security tracks.
Track choice matters: the same paper can meet very different reviewer pools.

## 4. USENIX Security

| Attribute | Value |
|---|---|
| Organizer / when | USENIX Association; August |
| Submission model | Cycle count shifts year to year — live dates: `deadlines_current.md` |
| Format | USENIX two-column template, ~13 pages excluding references and appendices |
| Anonymity | Double-blind |
| Decisions | Accepted / Accepted on Shepherd Approval / Rejected — **major revisions eliminated in '26**; at most a ~two-week shepherding window (100% of shepherd-approval papers accepted in '25) |
| Ethics | Ethics Considerations appendix: mandatory in '25/'26, **strongly encouraged (no longer mandatory) in '27**; all reviewers evaluate ethics, and expansions can be demanded during the author-response phase |
| Open science | **Mandatory Open Science policy** (since '25): artifacts/data expected to be shared or exemption justified; compliance checked |
| Artifact evaluation | Since '26, anonymized artifacts must be available **at submission** and are used during review; acceptance is conditional on continued availability; functionality/reproducibility badging stays opt-in post-acceptance |
| Citation style | Numeric |

**Fit notes:** Systems-heavy, pragmatic reviewing culture; large volume
(≈230 papers/year). Very strong venue for IoT/embedded measurement and
large-scale studies. The mandatory ethics + open-science sections are
structural: budget page space for them from the first outline, and plan the
artifact release before submission, not after acceptance.

---

## Cross-venue planning notes

- **Resubmission ladder:** the four venues' cycles interleave; a rejected paper
  can usually be turned to the next Big-4 deadline within 1–3 months — but
  check the cooldowns first: S&P bars resubmission for ONE YEAR from the
  original submission (keyed to intellectual contribution — a rewrite does
  not reset it); NDSS/CCS/USENIX bar only the same edition's other cycle.
  Any revision-tier decision is worth taking (NDSS Major Revision ≈87%
  accepted, minor/shepherd tiers ≈100%) rather than shopping the paper.
  Full multi-round mechanics: `major_revision_playbook.md`.
- **Dual-submission rules:** all four forbid concurrent submission; major-revision
  status counts as "under submission."
- **Page budget reality:** ~12–13 body pages means Intro + Threat Model +
  Design + Eval must be ruthlessly budgeted; appendices are read only by
  motivated reviewers and AE committees.
- **Tier-2 fallbacks** (from the same ranking, systems-security track):
  IEEE EuroS&P, ACSAC, AsiaCCS, PETS (privacy-flavored), ESORICS, RAID,
  ACM WiSec (wireless/IoT), IEEE CSF (foundations/formal).

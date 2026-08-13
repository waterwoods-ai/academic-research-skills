# Big-4 Multi-Round Review Playbook (Custom — Security Track)

> How the four top security conferences actually run multi-round review —
> rebuttal, revision, re-review — and how ARS revision modes must behave for
> each. Every fact below was verified against official CFP/policy pages
> (editions 2023–2027) in August 2026 via a 10-agent research+adversarial-
> verification pass; quoted decision names are verbatim. Structural facts
> drift edition to edition — re-verify against the target edition's CFP when
> a real decision letter arrives.

## 0. The one fact that reorganizes everything

**As of the 2026/2027 editions, NDSS is the ONLY Big-4 venue with a true
Major Revision decision.** The other three retired theirs:

- **IEEE S&P** abolished ALL revision decisions in 2024 (2023 first-time
  acceptance had collapsed to ~1.5%): decisions are now **Accept / Reject**
  only, with a published <500-word meta-review + optional author response,
  and a shepherd who strikes meta-review concerns the camera-ready fixes.
- **USENIX Security** eliminated "Invited for Major Revision" in '26:
  decisions are now **Accepted / Accepted on Shepherd Approval / Rejected**,
  with at most a ~two-week shepherding process.
- **ACM CCS** never had one in recent editions: **Accept / Minor revision /
  Reject** (plus "Administrative Reject" desk rejections, named in 2026).

Consequence: the classic "revise-and-resubmit against binding criteria"
workflow now applies in full ONLY to NDSS; at the other three venues the
leverage points are the **rebuttal** (S&P, CCS, USENIX) and the
**shepherding window** (all four). ARS revision modes must ask "which venue,
which decision" before assuming any workflow shape.

## 1. Venue-by-venue lifecycle (verified, editions 2025–2027)

### IEEE S&P — binary decisions, rebuttal is the only revision moment

- Two cycles/year (since 2025). Two-round review per cycle; early-reject
  notification ~6–7 weeks after the June deadline, ~9–10 weeks after the
  November one. Abstract registration freezes title/authors/ORCIDs a week
  before each deadline; 6 papers/author/cycle cap.
- Rebuttal (second-round papers only): through 2026, one interactive
  HotCRP window (~10–12 days, anonymous messaging; reviewers may decline to
  engage). **S&P 2027 splits it into two PC-assigned modes:**
  (a) *Non-interactive rebuttal* — 500 words, ONLY factual errors and
  concrete reviewer questions, NO new material of any kind;
  (b) *Interactive rebuttal* — 500 words, then new results **only if
  explicitly requested by reviewers**, which MUST be accompanied by a full
  revised manuscript PDF (the process's only revision-evaluation moment).
  Violating word count or material scope ⇒ **immediate rejection**.
- Decisions: **Accept / Reject**. "No conditional acceptance" — reviewed as
  submitted. Every accepted paper gets a public meta-review (<500 words:
  why accepted + remaining concerns) + optional <500-word author response;
  a shepherd removes concerns the camera-ready revisions address (2027:
  "Submission to shepherd" deadline ~3 weeks after notification).
- Reject cooldown: **one year from original submission date** (also for
  rebuttal-period rejections). Resubmission defined by intellectual
  contribution ("a reviewer could write a substantially similar summary"),
  so a full rewrite does NOT reset the clock; violations ⇒ >1-year
  penalties for all authors. Desk rejects (format/anonymity, no reviews)
  may return next cycle.
- Withdrawal: allowed any time BEFORE reviews are sent; impossible after.
- Source: sp2026.ieee-security.org/cfpapers.html, sp2027.ieee-security.org/cfpapers.html

### NDSS — the last true Major Revision venue

- Two cycles/year (stable since 2020). Two rounds per cycle: Round-1
  reviews are shared at the early-reject/advance notification (~5–6 weeks);
  Round-2 papers get a ~3-day written rebuttal + ~1-week interactive
  discussion with reviewers. No published rebuttal length limit.
- Decisions (exact names): **Accept / Minor Revision / Major Revision /
  Reject**.
- **Major Revision contract mechanics:**
  - The ORIGINAL reviewers write "a list of revision tasks clearly
    specified … and conveyed to the authors upon notification" — a binding,
    closed criteria list.
  - Resubmission is **within the same cycle**, ~4–5 weeks after
    notification (CFP prose said "six weeks" through 2026; the date tables
    govern).
  - Re-review is fast (verdict ~2 weeks after resubmission) and
    criteria-bound: "A revised paper will be accepted … if it
    satisfactorily fulfills the revision tasks."
  - **At most one major revision per edition** — re-review outcome is
    binary: accept, or done for this edition.
  - Officially unspecified (do not assume): same-reviewer guarantee,
    response-letter format, whether the revision window blocks submitting
    elsewhere (only the general concurrent-submission ban exists).
- Minor Revision: accepted "if and only if" the shepherd approves the
  revision (~3–4-week window). NDSS 2025 measured: Minor Revision 100%
  accepted, Major Revision 87.3% accepted.
- Reject cooldown: same edition only (summer reject cannot go to fall —
  desk rejection). No bar on next year's NDSS.
- Source: ndss-symposium.org/ndss2026/submissions/call-for-papers/ (and ndss2027)

### ACM CCS — same-cycle Minor revision only

- Two cycles/year (stable since ≥2023), ~10 topic tracks each run as a
  "separate mini-conference". Early-rejection notification ~5 weeks after
  the deadline; survivors get full review + a short one-shot rebuttal
  window (3–4 days; no published length/content rules).
- Decisions (exact names): **Accept / Minor revision / Reject** (+
  **Administrative Reject**, 2026 — desk rejection, the only reject flavor
  allowed back in the same year's Cycle B).
- Minor revision mechanics: revise "for inclusion in the same cycle";
  submit the revised paper + **"a separate note" explaining how the
  revisions address the reviewers' comments** (no diff mandated); anchored
  to the reviewer comments, not a separately issued criteria list;
  re-evaluation is binary (accepted or rejected); approval deadline ~7–8
  weeks after notification. Who re-reviews is not documented.
- **Withdrawal is prohibited (2026) until the final decision** — combined
  with the concurrent-submission ban, a Minor-revision paper is locked to
  CCS until resolved. (2025 allowed withdrawal before reviews were sent.)
- Reject cooldown: Cycle A rejects barred from Cycle B ("even in revised
  form"); nothing extends to next year.
- 2026 idiosyncrasies that bite: mandatory Open Science appendix +
  artifacts available ≤3 days after submission (desk rejection risk); no
  SoK/survey papers; ~200-word track-justification frozen at registration;
  7 papers/author/cycle.
- Source: sigsac.org/ccs/CCS2026/call-for/call-for-papers.html

### USENIX Security — shepherding is the whole revision game now

- Two cycles/year (since '25). Two-round review (2 reviews, early-reject
  ~6 weeks if both say reject; then 2 more reviews); one-week "author
  response phase" before notification. **No withdrawal once the response
  phase starts.**
- Decisions '26/'27 (exact names): **Accepted / Accepted on Shepherd
  Approval / Rejected**. ('25 additionally had "Invited for Major
  Revision"; '24 called it "Accept Conditional on Major Revision".)
- Shepherd Approval mechanics: changes "highly unlikely to reduce
  [reviewer] enthusiasm" — text changes, clarifications, explicit
  limitations discussion; ~two-week window from notification; one shepherd
  drawn from/agreed by the reviewers; all interaction via anonymous
  author-visible HotCRP comments that every reviewer can watch. In '25,
  100% of shepherd-approval papers were ultimately accepted.
- The retired-but-instructive '25 Major Revision model (the workflow NDSS
  still runs, and the response-package convention the community reuses):
  same-cycle revision (~5 weeks), one shepherd judging a fixed criteria
  list, resubmission package = separate PDF with **(1) the verbatim
  revision criteria, (2) a list of changes, (3) how the changes address
  the criteria, (4) a latexdiff-style marked-up copy**; +1 page allowance
  (14 vs 13); paper formally under review until resolved (blocking other
  venues); acceptance rates 85.7–90.4% across '20–'25.
- Reject cooldown: Cycle-1 rejects barred from Cycle 2 of the same
  edition; explicitly welcome the following year.
- Ethics during review: reviewers evaluate ethics of ALL submissions;
  Ethics Committee behind them; '25 required 13.9% of papers under review
  to expand their ethics discussion during the author-response period —
  budget rebuttal space for this.
- Source: usenix.org/conference/usenixsecurity26/call-for-papers (and 27)

## 2. Rebuttal playbook (community norms, attributed)

Base rates first: across CS conferences only ~1–4.4% of outcomes flip on
rebuttals (Dershowitz & Verma, cited in Yao's CACM "Rebuttal How-to",
2023) — but the USENIX Security '25 PC survey (102 respondents) found 91%
of PC members said author responses aided their understanding and 85% said
responses affected their overall conclusion for at least some papers.
Rebuttals matter precisely for papers on the Reject/revision boundary.

Distilled, attributed advice (Mathias Payer 2018; Daphne Yao CACM 2023;
Andreas Zeller 2012):

1. **Organize by topic, not by reviewer** (Payer). Extract and rank the
   criticisms; answer the few major ones; signpost which reviewer each
   response addresses (R1/R2 notation — Zeller).
2. **Arm the champion** (Yao): the rebuttal's real audience is the
   reviewer defending the paper in PC discussion (and the chairs, who
   prompt "does the rebuttal address your concerns?"). A weak rebuttal can
   make a champion abandon the paper.
3. **Target the undecided, not the committed detractor** (Zeller).
4. **New evidence beats back-references** (Yao): "what was already said in
   the paper clearly is unconvincing" — but ONLY where the venue permits
   new material (see venue rules; at S&P 2027 non-interactive mode it is
   grounds for immediate rejection).
5. **Signal revision competency** (Yao): where a revision tier exists
   (NDSS), reviewers screen the rebuttal for whether the team can execute
   a revision before offering one — "convey your strong willingness to
   revise."
6. **Tone: strictly technical** (Payer): no sarcasm or irony; frame
   misreadings as "the reviewer may have been misguided by the paper."
   Fatal mistakes: overlength, snark, unrequested new material.
7. **Rebut even hopeless papers** (Yao): the security review circle is
   small; resubmissions may meet the same reviewers at the next venue.

Venue-specific hard rules to check before drafting: S&P 500-word limit +
mode-dependent new-material ban (violation ⇒ immediate rejection); NDSS
rebuttal feeds a week of genuine back-and-forth (keep threads open, answer
follow-ups fast); CCS one-shot 3–4-day window; USENIX one-week response
phase, and expect possible mandated ethics-discussion expansion.

## 3. Revision response package (the codified convention)

For any binding-criteria revision (NDSS Major Revision today; the pattern
is USENIX-codified), the resubmission package is a separate PDF:

1. The **verbatim** revision criteria/tasks, unedited.
2. A numbered **list of changes** made to the paper.
3. A **per-criterion mapping**: how each change satisfies which criterion.
4. A **latexdiff-style marked-up copy** of the paper (or another format
   that lets the shepherd find changes efficiently, if the diff would be
   unreadable).

Handling a criterion you believe is wrong or infeasible: there is NO
formal appeals channel at any Big-4 venue. The documented mechanism is
negotiation with the shepherd, in writing, on the anonymous HotCRP thread
all reviewers can see — the shepherd may "prioritize and refine the
requirements" and poll other reviewers on whether a substitute change
satisfies their concern. Propose the substitute explicitly; never silently
skip a criterion. Non-approval simply converts to rejection.

Timeline reality (vs. journal R&R): fixed 4–5-week revision clocks,
verdict ~2 weeks later, at most ONE revision round, shepherd instead of
editor. Plan the revision work-back schedule the day the decision arrives.

## 4. Decision-arrival strategy matrix

| You received | Odds if you engage | Play |
|---|---|---|
| NDSS Major Revision | 87.3% (2025) | Take it. Freeze scope to the task list; build the §3 package; resubmit within the window. |
| NDSS/CCS Minor Revision | ~100% / high | Take it; scope = reviewer comments (CCS) or shepherd satisfaction (NDSS). |
| USENIX Shepherd Approval | ~100% ('25) | Two-week sprint on text-level changes; watch the HotCRP thread daily. |
| S&P Accept + meta-review | accepted already | Still revise: every concern you fix is struck from the PUBLIC meta-review before camera-ready ("submission to shepherd" ~3 weeks). |
| Reject (any venue) | — | Retarget using cooldown matrix below; harvest the reviews; expect possible same reviewers at the next venue. |

Cooldown / retarget matrix (verified): S&P → one year from original
submission, keyed to intellectual contribution (rewrite ≠ reset). NDSS →
barred from same edition only. CCS → Cycle A reject barred from Cycle B
only. USENIX → barred from the other cycle of the same edition; explicitly
welcome next year. Prior-rejection disclosure is required NOWHERE in
current editions (S&P dropped it 2024; USENIX made it optional '25, dropped
'26) — but chairs share submission lists to catch dual submissions, and
SIGSAC PROTECT (est. fall 2024) coordinates review-integrity cases across
all first-tier security venues.

While-under-revision blocking: a USENIX-model revision was formally "under
review" (withdraw before submitting elsewhere); CCS 2026 prohibits
withdrawal outright until the final decision; NDSS leaves it to the
general concurrent-submission ban. Assume locked-in unless the CFP says
otherwise.

## 5. ARS mode mapping (how the skills must behave)

- **`revision-coach` (reviewer comments in hand, no draft):**
  1. FIRST classify: which venue, which decision category (use the exact
     names in §1). The Revision Roadmap shape depends on it:
     NDSS Major Revision → roadmap = the verbatim task list, closed-world
     (no self-added tasks beyond it; flag any as optional extras);
     CCS Minor revision → roadmap keyed to individual reviewer comments;
     USENIX Shepherd Approval → text-level change list with a 2-week
     work-back schedule; S&P meta-review → concern-by-concern camera-ready
     plan.
  2. Response Letter Skeleton = §3 package structure for criteria-bound
     revisions; "separate note" per-comment format for CCS.
  3. Always emit the deadline work-back schedule (§3 timeline reality).
- **`rebuttal-audit` (rebuttal draft in hand):** audit against §2 — word
  limit (S&P: 500), venue's new-material rule (mode-dependent at S&P 2027),
  topic-organization, champion-arming, per-reviewer signposting, tone,
  revision-competency signal (NDSS), unanswered concrete questions. Flag
  any content that violates a venue hard rule as CRITICAL (S&P: grounds
  for immediate rejection).
- **`ars-reviewer` re-review mode (simulating the second look):**
  criteria-bound: verify each revision task fulfilled, judge NOTHING
  outside the task list (chairs explicitly discourage new objections),
  binary outcome. For USENIX-style shepherding, simulate the single
  shepherd (consulting reviewers) rather than a fresh 5-person panel.
- **Reviewer personas (`security_reviewer_personas.md`):** use the TARGET
  venue's exact decision vocabulary from §1 — do not offer "Major
  Revision" as a verdict when simulating S&P, CCS, or USENIX '26+.

## 6. Sources

Official: sp2026/sp2027.ieee-security.org/cfpapers.html;
sp2024.ieee-security.org/changes-cfp.html; ndss-symposium.org/ndss2026 and
/ndss2027 call-for-papers; sigsac.org/ccs/CCS2025 and /CCS2026 CFPs;
usenix.org/conference/usenixsecurity25|26|27/call-for-papers +
sec25_message.pdf (PC survey, acceptance statistics).
Community: M. Payer, "no-nonsense guide to rebuttals" (2018, nebelwelt.net);
D. Yao, "Rebuttal How-to" (CACM 2023); A. Zeller, rebuttal patterns
(2012, andreas-zeller.info); Stelmakh et al., "Prior and Prejudice" (2020,
resubmission-bias experiment, ML venue).

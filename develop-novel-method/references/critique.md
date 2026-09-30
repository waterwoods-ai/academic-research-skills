# Critique lens, candidate spec, novelty verdicts, scoring

## 1. Critique lens (for `analysis.md`, written before any LLM pass)
Answer each point with a paper location (§, Eq., Tab., Fig.), or write "not stated".
1. **Claims.** What exactly is claimed, and which experiment supports each claim?
2. **Mechanism.** Why does the method work, according to the authors? Is that explanation tested (ablation, analysis), or only asserted?
3. **Assumptions.**
   - Data: distribution, labels, i.i.d., access at test time.
   - Threat model or setting: attacker/user capabilities, compute, latency.
   - Structure the method exploits that may not hold elsewhere.
4. **Design choices fixed without justification:** thresholds, architectures, losses, hyper-parameters. Each one is a candidate "make it adaptive / learned / principled" improvement.
5. **Evaluation validity:**
   - baselines: missing the strongest ones, or not tuned equally;
   - leakage between train and test, or tuning on test;
   - datasets: few or synthetic only;
   - metrics: chosen to flatter;
   - statistics: no variance or seeds reported, no significance tests;
   - no failure cases shown.
6. **Scope:** settings where the claims plausibly break (scale, domain shift, adversarial inputs, other modalities).
7. **Cost:** compute, memory, labels, human effort. Is it reported, and is it fair relative to the baselines?
8. **Stated limitations and future work,** quoted.
9. **Reference audit:** the `baseline` and `related` entries in `references.md`, plus the step 2 Litmaps map. Did the paper compare against them? Which close competitors are missing from its references?

## 2. Confirming a weakness (`weaknesses.md`)
A weakness is **confirmed** only when it is checked against the paper text or a verified external paper.
- **Merged table:** # | weakness | raised by (me / ChatGPT / Claude.ai) | evidence (paper location or verified paper) | status | fixable?
- **Status** is one of:
  - `confirmed`;
  - `refuted`: the paper handles it, so give the location;
  - `unverifiable`: it needs an experiment;
  - `author-stated`: already in their limitations. Still usable, but weaker as a novelty hook, because others read the same limitations.
- **Independence:** raised by both you and ChatGPT independently → high confidence. Raised by Claude.ai only → treat as one voice, not independent confirmation (same model family).

## 3. Candidate method spec (each one in `candidates.md`, copied into `method-proposal.md`)
- **Name** and a one-sentence pitch.
- **Weakness removed:** the ids of confirmed weaknesses it removes. No confirmed weakness means it is not a candidate.
- **Mechanism:** precise enough to implement. Give the formulation (objective, algorithm steps, or pseudo-code) and what changes relative to the original method.
- **Why it should work:** an argument, a bound, or intuition plus a cited precedent.
- **Idea source:** my analysis / ChatGPT P3 / Claude.ai P3 / Litmaps bridge (Similar Text disconnect) / stale foundation / cross-domain transfer.
- **Minimal experiment:** dataset, baselines (the original paper plus the strongest competitors), metric, and the result that would falsify it. Compute target per the user's GPU rules (gpu1 by default).
- **Main risk:** the most likely reason it fails, or is judged incremental.

## 4. Novelty verdict (per candidate, recorded in `ledger.md`)
Run all of these, then give a verdict:
- (a) **Follow-up search:** on the step 2 Litmap, use the Explore **keyword filter** (free) with at least 3 phrasings of the mechanism, including the generic method-family name. This finds papers linked to the target that mention the idea. Also re-read `citing.md`.
- (b) **Elicit, recent:** a Find papers query phrased as the candidate's research question, with `+year:>{current_year-3}` and a `Direct match? (yes/partial/no)` column.
- (c) **Elicit, adjacent communities:** a query on the generic method family (e.g. "uncertainty-aware thresholding", "test-time adaptation"), regardless of domain.
- (d) **Litmaps:** keyword search (≤6 words, plain phrases) with "Since {last_year}". Re-read after 15–20 s before recording zero.
- (e) **P4 answers** from both tools, with every named paper verified.

**Verdicts:**
- `open`: no direct or partial match in (a)–(e).
- `narrow`: one or more partial matches, *or* the only difference is "same mechanism, new domain / new hardware". Needs a sharper differentiator before proceeding.
- `saturated`: one or more direct matches. Drop the candidate, or change its mechanism.

**Wording:** write "no direct match found in N queries across Litmaps follow-ups, Elicit, Litmaps search and two LLM reviews (date)". **Never** write "nobody is working on this". Preprints and in-review work are invisible to all of these tools.

## 5. Scoring (default: equal weights, 1–5 each; the user may redefine)
- **Novelty:** from the verdict and the distance to the closest match.
- **Soundness:** how strong the "why it should work" argument is, after the P4 attacks.
- **Weakness severity:** how much the removed weakness matters to the original paper's claims.
- **Feasibility:** fit with the user's compute, data and time.
- **Impact:** how many settings or follow-up papers the removed weakness affects (check `citing.md` and the Litmaps Momentum cluster), not the target paper's own popularity.

Drop any candidate scoring 1 on Novelty or Soundness.

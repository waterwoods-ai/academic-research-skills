---
name: verify-research-topic
description: Use when the user asks to verify, stress-test, sanity-check or review a security research topic, paper idea or study design before committing to it, including requests to answer a fixed list of research questions about a topic or to cross-check a topic with ChatGPT.
argument-hint: "<topic, or a path to a report/design file> [more topics]"
metadata:
  version: "1.0.0"
  last_updated: "2026-10-06"
  status: active
  data_access_level: raw
  task_type: open-ended
  related_skills:
    - security-track
    - find-research-topic
    - novelty-filter
    - novelty-engine
---

# Verify a Research Topic

<!-- routing-core:begin -->
**Step 0 — Escape hatch check (before any classification):** If the user's first message begins with `[direct-mode]` (case-insensitive byte-0 token, optionally preceded by whitespace/newlines that are stripped on parse), record this fact, strip the prefix and surrounding whitespace from the message, and skip directly to **Step 1 explicit-intent handling** on the stripped content. The literal `[direct-mode]` is NOT passed through to the dispatched agent. If the stripped message itself has no clear skill named, Step 1 falls through to Step 3 clarification (the escape hatch bypasses cross-phase clarification (Step 2), not all routing). When the token is honored and the named agent or skill needs inputs the message does not supply, read that agent's or skill's file and ask for what it requires, in its terms. Without the byte-0 token, naming an agent is not explicit intent: such a message goes through Steps 1-3 like any other, so cross-phase materials still get Step 2 clarification.

Otherwise, classify the user's input:

1. **Explicit clear intent** — user invokes a specific skill via `/ars-*` slash command, or uses an unambiguous trigger keyword that maps to a single skill (e.g., "lit-review this", "review my paper", "draft an abstract"):
   → Route directly; no clarification, no orchestrator detour.
   → The request stays explicit when the mode's usual input is absent or a word in it has other everyday senses. A revision request with no reviewer comments is revision mode's "feel certain sections need improvement" case, and "revisar artículo" is the reviewer's trigger. Route to that mode and let the mode handle what is missing; do not reopen the choice of workflow.

2. **Cross-phase materials detected** — user provides artifacts spanning ≥ 2 pipeline phases without naming a specific skill (e.g., pre-written abstract + pre-collected literature; full draft + reviewer comments + bibliography):
   → **Clarify**. Do NOT auto-route to a single-phase agent. List candidate workflows as a-d options in markdown body (NOT via AskUserQuestion tool). See `shared/references/intent_clarification_protocol.md` for the message template.
   → Reason: clarification is the safest action when materials don't unambiguously identify intent. (v3.10 active conductor (#134) will handle this via structured intake; v3.9.2 asks.)

3. **Ambiguous intent, no materials** — user provides no artifacts and no clear request:
   → Clarify per `shared/references/intent_clarification_protocol.md`.

**Anti-pattern (caused #133):** Receiving ambiguous cross-phase materials and silently auto-routing to a single-phase agent based on which phase the materials "look closest to." This bypasses orchestrator-level reconciliation and lets the subagent inherit the full ambiguity without independent oversight.

**Security-first default (this suite):** every research or paper task targets a security venue — the Big 4 (IEEE S&P, NDSS, ACM CCS, USENIX Security) or a tier-2 venue — unless the opt-out rule in the `security-track` skill (§ Activation) holds. Before configuring any ARS skill or agent for such a task, load `security-track` and apply its § Overrides of stock ARS defaults: IEEE/ACM numeric citations instead of APA 7.0; the security chapter structure with an explicit Threat Model and Ethics Considerations instead of IMRaD, sized by the venue's page limit; the five security reviewer personas with the target venue's decision vocabulary; double-blind anonymity; and conference deadlines only from its `deadlines_current.md`.
<!-- routing-core:end -->

Answer 12 questions about each topic from the evidence you hold, then get an **independent** second opinion from ChatGPT in Chrome, and resolve every disagreement against evidence.

- Questions, pass criteria and verdict rules: [references/questions.md](references/questions.md)
- Driving chatgpt.com: [references/chatgpt.md](references/chatgpt.md)

Load `superpowers-chrome:browsing` if it is not already in context.

**The second opinion only counts if ChatGPT did not see your answers, your concerns, or your prior-art list.** Agreement from a model you primed is not evidence.

## Hard rules
1. **Nothing is sent to ChatGPT until the user approves the exact brief text.** It is unpublished research leaving the machine. Show the brief, get a yes, then paste exactly that.
2. **Never paste** credentials, file paths, hostnames, unpublished data, author names, or anything from the user's private libraries. Follow the user's rule on private data.
3. **ChatGPT never adjudicates.** Settle a disagreement by checking the design, the ledgers, or the paper in question. Never by asking which of you is right.
4. **Every paper ChatGPT names is unverified** until a registry (Crossref / arXiv / OpenAlex) or the publisher page confirms the title, authors and year. It enters the report only then; unresolvable ones are listed as `claimed by ChatGPT, not found`.
5. **The user logs in and sets the model.** Never type or store a ChatGPT password. **Never click the model menu:** it has nested effort submenus, and a mis-click changes the user's settings. Ask the user to set the model and effort, then only *read* the button. Use a **Temporary Chat** unless the user says otherwise.
6. **Every paste step aborts unless `location.hostname === 'chatgpt.com'`,** Temporary Chat is on, and the chat is empty. Other tabs in the same browser (e.g. claude.ai) use the same `.ProseMirror` editor, and focus can move between tabs without warning.

## Run folder
`RUN=runs/<YYYY-MM-DD>-verify-<slug>`. Files: `answers.md` (yours, frozen), `brief.md` (approved), `chatgpt-blind.md`, `chatgpt-review.md` (transcripts), `verification.md` (final).

## Flow — repeat per topic, one fresh ChatGPT chat per pass

### 1. Gather the evidence
Read the topic's design / report / ledgers. List the sources you will cite. A topic with no written design gets a one-paragraph design from the user first.

### 2. Answer all 12 yourself, then freeze
Write `answers.md` against the pass criteria in `references/questions.md`: answer, the evidence behind it (file §, or a verified paper), and a status per question. Do not edit it after step 4 begins; later changes go in `verification.md` as resolutions.

### 3. Write the brief and get approval
`brief.md` contains **only the design facts**: problem setting, threat model, method, evaluation plan, scope. It **excludes** your answers, your known weaknesses, your prior-art list, your novelty verdict and any kill criterion. Show it to the user; send nothing until they approve it.

### 4. Blind pass (new Temporary Chat)
Paste the brief plus the 12 questions, and ask for each: an answer, a status, and the single most important change. Save the transcript to `chatgpt-blind.md`. Record the model name shown.

### 5. Review pass (a second new Temporary Chat)
Paste the same brief and ask for a top-venue review: strongest reasons to reject, ranked, plus the closest prior work with identifiers. **Do not suggest what to look for.** Save to `chatgpt-review.md`.

### 6. Verify, compare, resolve
- Verify every paper ChatGPT named (rule 4).
- For each question, compare your answer with ChatGPT's: `agree`, `ChatGPT-only point`, `mine-only point`, or `conflict`.
- Resolve each conflict and each ChatGPT-only point **against evidence**. Record what you checked and the outcome: adopted, rejected with reason, or `open — user decision`.
- An issue both sides raised independently is **high confidence**.
- **A ChatGPT `fail` or "cannot determine" caused by information the brief deliberately withheld (typically Q3, prior work) is not evidence.** Resolve that question from the review pass's prior-art list and your own sources.
- **Re-grade against `references/questions.md` only.** Don't soften a frozen status because ChatGPT's is milder, or harden it because ChatGPT's is harsher. If you change a status, write down which criterion drove it.

### 7. Report
Write `verification.md` in the format below, then give the user the verdict and the top three actions in chat.

## `verification.md` format
1. **Verdict:** `go` / `revise` / `stop`, from the rules in `references/questions.md`, in one sentence with the reason.
2. **Table, one row per question:** # | my status | ChatGPT status | agreement | resolution (what was checked) | final status.
3. **Rejection risks:** the merged reasons from Q12 and the review pass, ranked, each with a pre-emption.
4. **Prior art:** verified additions, then the `claimed by ChatGPT, not found` list.
5. **Actions:** concrete edits to the design, each tied to a question.
6. **Record:** ChatGPT model, date, chat mode (Temporary or not), links to the transcripts.

## Common mistakes
| Mistake | Fix |
|---|---|
| Asking ChatGPT first, then writing your answers | Freeze `answers.md` before any ChatGPT pass |
| Brief lists your prior work or your worries | Brief = design facts only |
| "Focus on whether X is tautological" in the review prompt | Name no issue; ask for the strongest reasons to reject |
| Pasting the brief, then asking if it was OK | Approval comes before the paste |
| Treating agreement as confirmation after showing your answers | Only blind agreement counts |
| One chat for several topics | One fresh chat per topic and per pass |
| Citing a ChatGPT-named paper you have not resolved | Verify, or list it as not found |

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 1.0.0 |
| Last Updated | 2026-10-06 |
| Maintainer | Tom |
| Dependent Skills | security-track (topic verification gate) |
| Role | Twelve-question topic check with a blind second opinion |

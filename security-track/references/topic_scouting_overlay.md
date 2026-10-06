# Topic Scouting Overlay (Custom — Security Track)

> Binds five skills to stages S0–S3 of `research_loop_protocol.md`.
> `novelty-engine` (the idea generator) ships in both editions of this suite.
> `find-research-topic`, `verify-research-topic` and `novelty-filter`
> drive Elicit, Litmaps, ChatGPT and Claude.ai in a headed Chrome window, so
> they ship in the Claude Code edition only. The fifth, `research-gaps`
> (Elicit API + Litmaps Zotero Sync + Zotero), comes from the separate
> zotero-literature plugin. The three browser skills and `research-gaps` are
> **search and filter front-ends**: they find leads faster than index queries
> alone; they do not decide. The loop's own gates (S1 gap rules, S3 full-text
> novelty check, the human gates) still decide.

## Which tool at which stage

| Stage | Need | Tool | Runs on |
|---|---|---|---|
| S0 | No topic yet: turn a broad area into 3–7 candidate topics | `find-research-topic` | Claude Code (needs the Chrome browser tool) |
| S1 | Topic chosen: systematic, repeatable gap evidence, filed in Zotero | `research-gaps` (Elicit API — needs **Elicit Pro**; Litmaps Pro for Zotero Sync) | Claude Code |
| S2 → S3 | Is this RQ worth committing to? | `topic_verification_gate.md` (12 questions); optional blind second opinion through `verify-research-topic` | Gate: every runtime. ChatGPT pass: Claude Code |
| S3 | Start from ONE baseline paper: limitation ledger, then filter candidate improvements for novelty (it does not generate) | `novelty-filter` | Claude Code |
| S3 | Generate from supported assumptions, confirmed baseline limitations or located observations; check and deduplicate candidates, shortlist at most three, formalize | `novelty-engine` Phases 1–4 (`dogma_extractor`, `cross_domain_synthesizer`, `limitation_resolver`, `observation_analyst`, `novelty_verifier`, `math_formalizer`); `references/evidence_driven_ideation.md` inside that skill | Every runtime (subagents on Claude Code; role by role elsewhere) |

- **With Elicit Pro, prefer the API for Elicit work** (`research-gaps`): it is
  repeatable, needs no browser, and allows up to 20 extraction columns. Keep
  the browser skill for early scouting and for the Litmaps steps it automates
  (Explore, Similar Text, momentum × connectivity).
- Do not run both front-ends on the same topic for the same purpose; pick by
  the table.
- **Zotero and Elicit are reached through their APIs, not their web pages**
  (Tom's standing instruction, 2026-10-01; the keys are in the shell as
  `ELICIT_API_KEY`, `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`). Zotero reads go
  through the local API (`zotero_api.py`, Zotero desktop running) and writes
  through the Web API (`zotero_write.py`); Elicit searches and reviews go
  through `elicit_api.py`. Open the Elicit or Zotero site in a browser only
  for what the API cannot do (Litmaps steps, the Elicit UI's column views).
- **Codex / opencode** cannot drive the browser. There: run S1 with
  `perspective_retrieval_protocol.md` and the scholarly-index resolvers, apply
  the rules below by hand, and run the gate from `topic_verification_gate.md`.
  The independent second opinion is the reviewer on the other model family.

## What their output is, and is not (binding rules)

1. **A tool verdict is scan-level.** It is a lead, never a novelty claim:

   | Tool verdict | What it means | Status in the loop |
   |---|---|---|
   | `open` | no direct match found in N queries | candidate only; becomes NOVEL-WITHIN-SEARCH after the S3 full-text check of the nearest work |
   | `narrow` | a partial match, or the same mechanism in a new domain / on new hardware | INCREMENTAL unless the mechanism itself is sharpened |
   | `saturated` | a direct match exists | KNOWN — drop or rework the *approach*; keep the *problem* (iron rule 6) |

2. **A reported gap enters the gap registry only with S1's three fields**: the
   search that failed to fill it (the tool run's ledger supplies queries,
   tools and dates), the nearest-miss papers and why each falls short, and the
   security question the gap blocks.
3. **A candidate gap needs at least two independent signals** out of: two or
   more papers naming the same limitation or future work; a bridge gap
   (close in meaning, not linked by citation); a fast-growing cluster not yet
   applied to your setting; a highly cited foundation with few recent
   follow-ups; contradictory findings.
4. **A paper named by an LLM or a tool counts only after verification** against
   a registry or the publisher page (title, authors, year) — the ARS
   citation-existence gate. Otherwise list it as `claimed by <tool>, not found`.
5. **LLMs never adjudicate.** Freeze your own answers first; send nothing of
   them to the second model; settle a disagreement against the design, the
   ledger or the paper. Only agreement from a different model family counts as
   independent.
6. **Approval before anything unpublished leaves the machine.** Show the exact
   text; send after a yes. Short search phrases are exempt.
7. **Their generic scoring is replaced by the S2 ranking** (impact ×
   feasibility × freshness, with a threat-model sketch and venue fit).
   Citation momentum is not security impact.
8. **Stance (iron rule 6).** A weakness table of a baseline paper is the
   limitation ledger for S3 — input to an improvement, never the contribution.
   Give each weakness a status: `confirmed` (checked against the paper text),
   `refuted`, `unverifiable` (needs an experiment), or `author-stated`. An
   `author-stated` limitation is a weak novelty hook: everyone reads the same
   limitations section.

## Search rules learned from real runs (apply on every runtime)

- **Ancestor query.** Run at least one query with NO year filter, phrased as
  the generic problem with the current buzzwords removed (no "LLM", "agent",
  "foundation model"). A recent-years scan of "poisoning LLM rule generators"
  missed that poisoning signature generators was published in 2006.
- **Adjacent-method-family query.** Name the generic method family the idea
  belongs to (e.g. "test-time adaptation", "backdoor detection") and search it
  regardless of application domain. Domain-phrased queries miss it.
- **Missing citation links are a data gap, not a research gap.** IEEE-heavy
  seed sets often have no reference lists in open metadata.
- **A failed fetch is a route failure until a browser has been tried.** A bot
  challenge, a 403 or a redirect loop is not a paywall; only a subscription
  prompt seen in a browser is.
- **Feasibility is checked, not assumed.** Confirm you have the devices. Open
  the dataset before designing on it: raw or features, labels, duration,
  whether timestamps survive (a shuffled release cannot support a
  chronological claim).
- **Hot-paper saturation.** If every candidate derived from a recent,
  heavily-followed paper comes back `saturated`, stop iterating on "improve
  this paper" and generate problem-first instead, then filter the survivors.
- **Wording.** Write "no direct match found in N queries across <tools>
  (<date>)". Never "nobody has done this": preprints and work under review
  are invisible to every tool.

## Hand-off into the loop's artifacts

| Tool output | Goes into |
|---|---|
| `find-research-topic` (HOWTO Step 1a) | writes its kept papers to `literature.md` and its candidate gaps to `gap_registry.md` as LEAD entries; the systematic review (Step 1b) starts from those files, searches only what they do not cover, and completes each LEAD to the S1 three-field form or drops it |
| `gap-report.md` (research-gaps) | `gap_registry.md` entries, each completed to the S1 three-field form |
| `verification.md` (verify-research-topic) | the go / revise / stop annotation on the RQ card |
| `weaknesses.md` + `method-proposal.md` (novelty-filter) | S3 limitation ledger, which is the input of `novelty-engine`'s limitation-driven mode; candidate cards and Contribution Card items 2–3 (novelty status, positioning) |
| every run's `ledger.md` | the search record S1 and S3 cite |

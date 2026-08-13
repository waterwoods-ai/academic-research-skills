# Perspective-Guided Retrieval Protocol (Custom — Security Track)

> STORM's retrieval-side mechanisms (Shao et al., NAACL 2024; Co-STORM,
> EMNLP 2024), adapted for security-conference literature work. Adopted:
> perspective-guided question asking (as QUERY EXPANSION) and the Co-STORM
> moderator move (as UNUSED-RETRIEVAL FOLLOW-UP). Deliberately NOT adopted:
> ungrounded persona content generation, model self-grading, and fixed-cast
> synthesis — those conflict with the ARS citation iron rule and its
> independent-verification design. This protocol is additive and opt-in; it
> does not touch the upstream #461 Socratic adjacent-framing probe.

## IRON RULES (read first)

1. **Personas emit QUESTIONS and SEARCH QUERIES only — never answers,
   claims, or prose.** Any narrative text produced while generating
   questions is discarded after query extraction. Nothing from this
   protocol may enter a manuscript, synthesis report, or evidence map as
   content.
2. **Every retrieved result flows through the standard ARS pipeline
   unchanged**: bibliography_agent resolvers (Semantic Scholar / OpenAlex /
   Crossref / arXiv), the citation-existence gate, contamination signals,
   and the corpus-first / search-fills-gap flow. This protocol widens what
   gets retrieved; it never bypasses how retrieval is verified.
3. **Bounded rounds**: at most ONE expansion round (Mechanism 1) plus ONE
   moderator round (Mechanism 2) per literature search. No loops.
4. Coverage claims stay search-bounded (ARS v3.18 #548): running this
   protocol supports "within our search" phrasing only — it never
   justifies "first/only work" claims.

## When to use

| Situation | Use? |
|---|---|
| `/ars-lit-review`, deep-research full / systematic-review — at Stage 1 search-strategy design | YES — Mechanism 1 before the first search round, Mechanism 2 after the last |
| `/ars-outline` evidence-map construction | YES — Mechanism 1 (queries) + Mechanism 3 (traceability) |
| novelty-engine gap analysis (`gap_analyzer` phase) | YES — Mechanism 2's output feeds gap candidates |
| `/ars-3w`, quick scans, fact-checks | NO — cost exceeds benefit; skip |
| Revision / rebuttal / abstract / format modes | NO — no retrieval happens there |
| User explicitly asks for "broad coverage", "make sure we didn't miss anything", "related work sweep" | YES — this is the trigger phrase family |

## Mechanism 1 — Perspective-Guided Query Expansion

**Problem it solves:** a single framing generates a single query family;
STORM showed multi-perspective questioning is what widens coverage
(+10% breadth in their evaluation — a retrieval effect, not a prompting
trick).

**Step 1 — Fixed security lenses.** Derive question-askers from
`security_reviewer_personas.md`, retargeted from judging to searching:

| Lens | Asks questions about |
|---|---|
| Systems/CPS | testbeds, physical processes, control loops, ICS protocols, safety impact |
| IoT/embedded | device classes, firmware, vendor ecosystems, large-scale measurement |
| Adversarial-ML | attack/defense families, adaptive evaluation, benchmarks, model classes |
| Threat-model skeptic | attacker economics, deployment realism, prior broken defenses, root causes |
| Defense/deployment | mitigations in production, operator constraints, cost/overhead studies |
| Measurement/empirical | datasets, methodology papers, negative results, replication studies |

**Step 2 — Topic-adaptive lens discovery (true-STORM move, grounded).**
Retrieve 2–4 existing surveys/SoK papers adjacent to the topic; read their
section headings ONLY; if the headings reveal a recurring angle not
covered by the six lenses (e.g., "legal/policy", "usable security",
"hardware side channels"), add it as a temporary lens. This step reads
real papers — it is retrieval, not recall.

**Step 3 — Question generation.** Each lens generates 3–5 questions it
would need answered about the topic. Questions must be searchable (name
concrete systems, attack families, methods), not rhetorical.

**Step 4 — Query extraction.** Convert each question into 1–2 keyword
queries for the scholarly indexes. Deduplicate across lenses. Discard the
question prose (Iron Rule 1). Hand the query set to the normal
bibliography search.

**Step 5 — Provenance logging.** Record in the Search Strategy report
(alongside ARS's PRE-SCREENED block): the lens set used (fixed + any
adaptive additions), per-lens query counts, and which final corpus entries
arrived via which lens. Format:

```
PERSPECTIVE-EXPANSION (security-track protocol)
lenses: 6 fixed + [adaptive: <name> from <survey citation>]
queries: <N> total after dedup (<n1> systems/CPS, <n2> IoT, ...)
lens-attributed hits in final corpus: <k> of <total>
```

## Mechanism 2 — Unused-Retrieval Follow-up (moderator move)

**Problem it solves:** what a search retrieved but the review did NOT use
is an unexamined boundary — Co-STORM's moderator generates questions from
exactly this residue.

**Step 1.** After the final search round, collect the retrieved-but-
excluded set (ARS already emits `rejection_log.yaml` in the adapter flow;
otherwise list excluded hits from the search session).

**Step 2.** Cluster the exclusions (by topic, not one-by-one). For each
cluster ask exactly three questions:
- Why is this cluster irrelevant? (One sentence; if the sentence is hard
  to write, the cluster may not be irrelevant.)
- Does excluding it reveal an UNSTATED scope assumption? If yes, write the
  assumption into the review's scope statement explicitly.
- Does the cluster suggest a search angle none of the lenses produced?

**Step 3.** Outcomes (pick per cluster, then STOP — one round only):
- `boundary-documented`: scope statement updated; nothing else.
- `one-more-query`: at most 3 additional queries total across all
  clusters, run through the normal pipeline.
- `gap-candidate`: forward to novelty-engine `gap_analyzer` as a candidate
  gap (it still must survive `novelty_verifier` grounding — this protocol
  only nominates).

## Mechanism 3 — Outline perspective traceability

When the outline / evidence map is built from a corpus assembled under
this protocol, tag each outline section with the lens(es) whose queries
surfaced its supporting evidence. Emit a coverage warning for any section
whose evidence traces to a SINGLE lens — single-lens sections are where
reviewer blind-spot objections (e.g., "no deployment perspective")
concentrate. The warning is advisory, never blocking.

## What this protocol explicitly does NOT do

- No persona ever answers its own questions from model memory — the
  answers are the retrieved papers.
- No self-grading of outputs (ARS's independent gates already exist).
- No claim generation: breadth improvements show up as corpus entries and
  scope statements, both of which are independently verifiable.
- No change to upstream behavior: stock ARS runs identically when this
  protocol is not invoked; #461 stays bounded exactly as upstream shipped
  it.

## Worked micro-example

Topic: "sensor spoofing detection for industrial control systems".

- Systems/CPS lens → "Which physics-based invariants have been used to
  detect spoofed sensor values in water-treatment testbeds?" → queries:
  `physics-based anomaly detection ICS sensor spoofing`,
  `water treatment testbed SWaT attack detection`.
- Threat-model skeptic → "Which published spoofing-detection defenses
  were later bypassed, and how?" → `sensor spoofing detection bypass
  adaptive attacker ICS`.
- Adaptive lens discovery: an adjacent SoK's headings reveal a
  "hardware/analog side" angle → temporary lens adds
  `analog sensor attack transduction out-of-band signal injection`.
- Moderator round: 14 excluded hits cluster around automotive LiDAR
  spoofing → decision `boundary-documented`: scope statement now says
  "automotive perception attacks are out of scope; we cover fixed-plant
  ICS sensing" — an assumption that was previously implicit.

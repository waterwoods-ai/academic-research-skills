# <Project Name> — Security Research (anchor file)

This directory is a CPS / IoT / AI-security research project targeting
Big-4 / tier-2 security venues. For ANY research or paper task here, load
and follow the **security-track** skill (academic-research-skills plugin)
and its research-loop protocol (S0–S8) BEFORE answering.

Project state (keep current):

- Target venue: <venue year, e.g. NDSS 2027>
- Research-loop stage: <S0–S8, e.g. S4 design frozen>
- Paper file: <path, e.g. ./paper.tex>
- Review workspace: ./ars-review/ (if present, re-review reads it)

Hard rules: conference deadlines ONLY from the skill's
deadlines_current.md; paper numbers ONLY from the experiment provenance
ledger; success criteria frozen at design freeze.

Lab roles (if this project runs the three-agent lab; see the skill's
lab_orchestration_protocol.md). Write only your own files:
- Claude Code, Director (also literature and novelty): research_question.md,
  contribution_card.md, claims.md, decisions.md, method_changelog.md, paper/,
  gap_registry.md, literature.md, literature/
- GLM (opencode), security scientist: rq_cards.md, security/,
  novelty_engine/, candidate_cards.md, plans until frozen
- Codex, research engineer and Reviewer #2: code, tests/, ledger/, results/,
  artifact, reviews/, ars-review/ (it never reviews its own code or results)
Direction files change only on a decision recorded in decisions.md. A refused
request is never resent verbatim to another agent.

# Prompts for the ChatGPT and Claude.ai project passes

Send each block **verbatim**, identically to both tools. Replace only the `{…}` fields.
- **P1–P3 are blind.** They must not contain anything from `analysis.md`: none of your critique, your suspected weaknesses, or your idea direction.
- **P4 contains unpublished ideas.** The user must approve its exact text first.

## Project instructions (set once per project)
```
You are a senior reviewer and method designer for top venues in {field}.
The attached PDF is the only paper under analysis. Ground every claim about it
in a section, equation, table or figure number. Say "not stated in the paper"
rather than guessing. When you name other papers, give title, first author,
year and a DOI or arXiv id; say "unsure of identifier" rather than invent one.
Be critical: praise is not useful here.
```

## P1: Structured read (blind)
```
From the attached paper, give:
1. The problem and the exact claims (numbered, with where each is supported).
2. The method, step by step, including every design choice and hyper-parameter
   the authors fixed without justification.
3. All assumptions the method needs to work — stated and unstated.
4. The evaluation: datasets, baselines, metrics, ablations. What is missing?
5. The limitations and future work the authors state.
```

## P2: Weakness hunt (blind, same chat)
```
Now act as the harshest competent reviewer. List the strongest reasons the
method or its evidence could be wrong, ranked by severity. For each:
- the weakness, and where in the paper it shows;
- a concrete scenario or input where the method would fail or the claim would not hold;
- how the authors could have tested it;
- whether it is fixable, and roughly how.
Cover at least: hidden assumptions, evaluation validity (leakage, weak or
missing baselines, cherry-picked settings, statistics), scalability/cost,
and generality beyond the tested setting.
```

## P3: Improvement directions (blind, same chat)
```
Propose 3–5 directions that would improve on this method in a way a top venue
would accept as a new method, not an incremental tweak. For each:
- which weakness from your previous answer it removes;
- the core mechanism, precisely enough to implement;
- why it should work (intuition or a short argument);
- the closest existing work you know, with identifiers, and how the direction differs;
- the smallest experiment that would show it beats the original.
```

## P4: Attack our candidates (needs user approval; new chat in the same project)
```
Below are candidate methods that build on the attached paper. For each:
1. Is it already published or obviously implied by existing work? Name the
   closest papers with identifiers, and say how close (identical / overlapping
   mechanism / same goal, different mechanism).
2. The strongest technical reason it would fail.
3. What a reviewer would call "incremental" about it, and what would make it
   clearly novel.
Do not be encouraging; if a candidate is not novel, say so.

{from candidates.md: name, weakness addressed, mechanism, minimal experiment}
```
A new chat is used for P4 so the model judges the candidates without its own P3 ideas in the same thread. The project files still give it the paper.

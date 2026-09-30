# Mathematical & Algorithmic Formalization Requirements

## Iron Rule

**No methodology proposal exits the Novelty Engine without at least one of:**
1. A mathematical theorem/proposition with proof sketch
2. An algorithm with pseudocode and complexity analysis

Prose-only methods are rejected. "Use technique X" without formal specification is rejected.

## Minimum Formalization Standards

### Track A: Mathematical Formalization

| Component | Required | Standard |
|-----------|----------|----------|
| Formal definitions | YES | Every object defined before use, using set-builder or constructive definitions |
| Assumption enumeration | YES | (A1), (A2), ... explicitly listed; no hidden prerequisites |
| Problem statement | YES | Given/Find/Subject-to/Objective format |
| Core theorem | YES | At least one non-trivial result with proof sketch |
| Bounds | YES | At least one upper or lower bound; complexity, approximation, or sample |
| Proof technique | YES | Named technique (induction, contradiction, reduction, coupling, etc.) |

### Track B: Algorithmic Specification

| Component | Required | Standard |
|-----------|----------|----------|
| I/O specification | YES | Formal input/output types with preconditions |
| Pseudocode | YES | Numbered lines, proper indentation, standard algorithmic notation |
| Time complexity | YES | Big-O with justification (not just stated) |
| Space complexity | YES | Big-O with justification |
| Correctness argument | YES | Loop invariants for iterative; structural induction for recursive |
| Termination proof | YES | For any loop or recursion, argue why it terminates |

### Track C: Both (Preferred)

When a method has both analytical and computational components:
- Mathematical framework governs the "what" (what the method optimizes, what it guarantees)
- Algorithmic specification governs the "how" (how to compute it efficiently)
- Complexity analysis bridges both (computational complexity of achieving the mathematical guarantee)

## Formalization Depth by Paper Section

| Section | Expected Depth |
|---------|---------------|
| Introduction | Informal problem statement; formal version deferred |
| Related Work | Formal comparison of complexity/guarantees across methods |
| Method | Full formal specification (definitions, theorems, algorithms) |
| Analysis | Proofs, bounds, convergence, impossibility results |
| Experiments | Formal metric definitions, statistical test specifications |
| Discussion | Limitations stated as formal conditions under which guarantees break |

## Common Formalization Failures

### Decorative Math
```
BAD:  "Let f(x) = something. This shows our method works."
GOOD: "Let f: X → Y be defined by f(x) = [formula]. Under assumptions
       (A1)-(A3), f satisfies ||f(x) - x*|| ≤ ε for all x ∈ B(x*, δ).
       Proof: By [technique], we bound..."
```

### Missing Definitions
```
BAD:  "We compute the similarity between nodes."
GOOD: "Definition 3.1. Let G = (V, E, w) be a weighted graph. The 
       similarity between nodes u, v ∈ V is defined as 
       sim(u,v) = Σ_{p ∈ P(u,v)} Π_{e ∈ p} w(e) / |p|
       where P(u,v) is the set of all simple paths from u to v."
```

### Vacuous Complexity
```
BAD:  "The algorithm runs in polynomial time."
GOOD: "The algorithm runs in O(n² log n) time, dominated by the sorting
       step in Line 7 (O(n log n)) executed for each of the n nodes."
```

### Hand-Waved Convergence
```
BAD:  "The algorithm converges to the optimal solution."
GOOD: "Theorem 4.1. Under assumptions (A1)-(A3), Algorithm 1 converges
       to an ε-approximate solution in O(1/ε²) iterations.
       Proof sketch: Define the potential function Φ(t) = [formula].
       By (A2), Φ(t+1) ≤ Φ(t) - γ||∇Φ(t)||². Since Φ is bounded
       below by (A3), the sequence converges by [monotone convergence]."
```

## Statistical Requirements for Experimental Design

Every proposed experiment MUST specify:

1. **Null hypothesis** (H₀) and **alternative** (H₁) — formally stated
2. **Test statistic** — named test with justification for choice
3. **Significance level** (α) — typically 0.05 unless justified otherwise
4. **Power analysis** — minimum sample size to detect effect of size d
5. **Multiple comparison correction** — if running >1 test (Bonferroni, Holm, FDR)

| Comparison Type | Recommended Test | When to Use |
|----------------|-----------------|-------------|
| Two methods, paired | Wilcoxon signed-rank | Non-parametric, robust |
| Two methods, independent | Mann-Whitney U | Non-parametric, different samples |
| Multiple methods | Friedman + Nemenyi post-hoc | Non-parametric, paired |
| Confidence intervals | Bootstrap (10K resamples) | Always provide alongside p-values |
| Effect size | Cohen's d or Cliff's delta | Always report; p-values alone are insufficient |

## Domain-Specific Standards

### Computer Science / ML
- Computational complexity must reference known complexity classes where relevant
- Learning-theoretic bounds (PAC, VC, Rademacher) for any generalization claim
- Differential privacy parameters (ε, δ) if privacy is claimed

### Social Science / HCI
- Effect sizes mandatory (not just significance)
- Causal identification strategy must be explicit (IV, RDD, DiD, matching)
- Pre-registration plan for any human subjects experiment

### Natural Science / Engineering
- Dimensional analysis for all physical quantities
- Uncertainty propagation through measurement chain
- Units stated for every numerical result

### Formal Methods / Security
- Adversary model formally defined (capabilities, knowledge, objectives)
- Security properties stated as formal games or trace properties
- Reduction to known hard problems for any hardness claim

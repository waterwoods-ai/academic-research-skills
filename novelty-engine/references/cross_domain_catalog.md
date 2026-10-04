# Cross-Domain Isomorphism Catalog

A discovery aid organized by **problem structure**, not by field. Entries and precedent labels are search leads, not verified novelty claims or proofs of transfer; retrieve the original work and check its assumptions before use. Use this to identify promising donor disciplines for any breaking point.

## Catalog Structure

Each entry describes:
- The **abstract problem structure** (field-agnostic)
- **Donor disciplines** that have mature solutions
- **Successful precedents** where this mapping produced published results
- **Formalization hooks** (what mathematical tools to use)

---

## 1. Coordination Without Central Control

**Abstract structure**: Multiple autonomous agents must achieve collective behavior without a central coordinator.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Statistical Mechanics | Ising model, spin glasses, phase transitions | Hamiltonian $H = -\sum_{ij} J_{ij} s_i s_j$, partition function $Z$ |
| Swarm Intelligence | Ant colony optimization, particle swarm | Pheromone update rules, velocity equations |
| Market Microstructure | Price discovery, order books, market makers | Equilibrium existence theorems, bid-ask dynamics |
| Evolutionary Biology | Evolutionary stable strategies, kin selection | Replicator dynamics $\dot{x}_i = x_i(f_i - \bar{f})$ |

**Successful precedents**: Flocking algorithms (Reynolds→robotics), ant-inspired routing (Dorigo→networking), market-based resource allocation (economics→distributed systems)

---

## 2. Information Extraction Under Noise

**Abstract structure**: Recovering a true signal from corrupted, incomplete, or adversarially modified observations.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Coding Theory | Error-correcting codes, channel capacity | Shannon capacity $C = \max_{p(x)} I(X;Y)$ |
| Compressed Sensing | Sparse recovery, RIP, basis pursuit | $\min ||x||_1$ s.t. $Ax = b$ |
| Robust Statistics | Breakdown point, influence functions | $\sup_F |T(F) - T(G)|$ over contamination neighborhoods |
| Quantum Error Correction | Stabilizer codes, syndrome measurement | Pauli group, stabilizer formalism |

**Successful precedents**: LDPC codes (information theory→storage), compressed sensing (functional analysis→MRI), robust PCA (robust statistics→computer vision)

---

## 3. Multi-Scale Structure

**Abstract structure**: A system exhibits qualitatively different behavior at different scales, and cross-scale interactions matter.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Renormalization Group | Scale-invariant physics, universality classes | RG flow equations, fixed points, critical exponents |
| Wavelet Theory | Multi-resolution analysis, time-frequency | $\psi_{a,b}(t) = a^{-1/2}\psi((t-b)/a)$ |
| Fractal Geometry | Self-similarity, Hausdorff dimension | $D_H = \lim_{\epsilon \to 0} \frac{\log N(\epsilon)}{\log(1/\epsilon)}$ |
| Ecological Hierarchy | Patch dynamics, landscape ecology | Metacommunity models, spatial Markov chains |

**Successful precedents**: Wavelets (harmonic analysis→signal processing), renormalization (physics→network analysis), fractal analysis (geometry→financial markets)

---

## 4. Strategic Interaction with Incomplete Information

**Abstract structure**: Agents make decisions that affect each other, but each agent has private information.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Mechanism Design | Incentive compatibility, revelation principle | VCG mechanisms, Myerson's theorem |
| Cryptographic Protocols | Zero-knowledge proofs, secure computation | Simulation-based security definitions |
| Signaling Theory | Cheap talk, costly signals, screening | Spence signaling game, separating/pooling equilibria |
| Auction Theory | Revenue-optimal auctions, combinatorial auctions | Myerson's optimal auction, VCG payments |

**Successful precedents**: Spectrum auctions (auction theory→telecom policy), differential privacy (cryptography→data science), mechanism design (game theory→platform economics)

---

## 5. System at a Phase Boundary

**Abstract structure**: A system operates near a critical point where small parameter changes cause qualitative behavior shifts.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Thermodynamics | Phase transitions, critical phenomena | Order parameter, Landau theory, mean-field |
| Catastrophe Theory | Bifurcation, structural stability | Thom's classification, gradient dynamics |
| Percolation Theory | Giant component, connectivity threshold | $p_c$ critical probability, cluster size distribution |
| Dynamical Systems | Bifurcation, strange attractors, chaos | Lyapunov exponents, Poincaré maps |

**Successful precedents**: Percolation (physics→epidemic modeling), catastrophe theory (math→engineering failure), phase transitions (physics→opinion dynamics)

---

## 6. Adversarial Robustness

**Abstract structure**: A system must perform well when an adversary actively tries to cause failure.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Cryptography | Indistinguishability, reductions | Security games, polynomial-time adversaries |
| Evolutionary Arms Races | Red Queen hypothesis, coevolution | Fitness landscapes, frequency-dependent selection |
| Robust Optimization | Worst-case optimization, uncertainty sets | $\min_x \max_{u \in \mathcal{U}} f(x, u)$ |
| Immune System | Clonal selection, affinity maturation | Hypermutation rates, affinity thresholds |

**Successful precedents**: Adversarial training (optimization→ML), GAN architecture (game theory→generative modeling), immune-inspired intrusion detection (immunology→cybersecurity)

---

## 7. Causal Discovery from Observational Data

**Abstract structure**: Determining cause-effect relationships without controlled experiments.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Do-Calculus | Interventional distributions, back-door | $P(y|do(x)) = \sum_z P(y|x,z)P(z)$ |
| Granger Causality | Temporal prediction, VAR models | $x$ Granger-causes $y$ if $P(y_t|y_{<t}, x_{<t}) \neq P(y_t|y_{<t})$ |
| Natural Experiments | Instrumental variables, regression discontinuity | LATE, Wald estimator, McCrary density test |
| Transfer Entropy | Information-theoretic causality | $T_{X \to Y} = H(Y_t|Y_{<t}) - H(Y_t|Y_{<t}, X_{<t})$ |

**Successful precedents**: IV estimation (econometrics→epidemiology), Granger causality (economics→neuroscience), do-calculus (philosophy→ML fairness)

---

## 8. Representation and Dimensionality

**Abstract structure**: Finding the right low-dimensional representation of high-dimensional data.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Differential Geometry | Manifold learning, Riemannian metrics | Geodesic distance, curvature, parallel transport |
| Topology | Persistent homology, Betti numbers | Simplicial complexes, filtration, barcode diagrams |
| Information Geometry | Fisher metric, natural gradient | $g_{ij} = E[\partial_i \log p \cdot \partial_j \log p]$ |
| Category Theory | Functors, natural transformations | $F: \mathcal{C} \to \mathcal{D}$ preserving structure |

**Successful precedents**: Manifold learning (geometry→ML), TDA (algebraic topology→data science), information geometry (differential geometry→neural networks), natural gradient (Riemannian→optimization)

---

## 9. Resource Allocation Under Constraints

**Abstract structure**: Distributing limited resources to maximize utility under hard constraints.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Linear Programming | Simplex, duality, complementary slackness | $\max c^Tx$ s.t. $Ax \leq b, x \geq 0$ |
| Queueing Theory | Scheduling, load balancing, priority | Little's law $L = \lambda W$, M/M/c models |
| Optimal Transport | Wasserstein distance, Kantorovich | $\inf_{\gamma \in \Pi(\mu,\nu)} \int c(x,y) d\gamma$ |
| Ecological Niche Theory | Competitive exclusion, niche partitioning | Lotka-Volterra dynamics, carrying capacity |

**Successful precedents**: Optimal transport (probability→generative models), queueing theory (telecom→cloud computing), niche theory (ecology→market positioning)

---

## 10. Learning with Limited Feedback

**Abstract structure**: Making good decisions when feedback is delayed, sparse, partial, or costly.

| Donor Discipline | Framework | Formalization |
|-----------------|-----------|---------------|
| Bandit Theory | Explore-exploit, UCB, Thompson sampling | Regret $R_T = \sum_t \mu^* - \mu_{a_t}$, UCB bound |
| Active Learning | Query strategies, version space | Reduction rate, disagreement coefficient |
| Experimental Design | Optimal design, D-optimality | $\max_{\xi} \det(M(\xi))$, Fisher information matrix |
| Reinforcement Learning | MDPs, temporal difference, policy gradient | Bellman equation $V(s) = \max_a [R(s,a) + \gamma \sum_{s'} P(s'|s,a)V(s')]$ |

**Successful precedents**: UCB (statistics→clinical trials), active learning (statistics→NLP annotation), optimal design (statistics→A/B testing)

---

## How to Use This Catalog

1. **Identify the abstract structure** of your breaking point (match to one of the 10 categories above)
2. **Select structurally suitable frameworks** from adjacent or distant fields; compare assumptions, adaptation costs and known uses rather than maximizing disciplinary distance
3. **Check the formalization column** — this tells you what mathematical tools to bring
4. **Check precedents** — if your exact mapping already exists, you need a new angle
5. **Compose structures** — many real problems combine 2-3 abstract structures (e.g., "adversarial robustness" + "multi-scale structure" = adversarial attacks that exploit cross-layer gaps)

## Composing Structures

The following combinations illustrate structures to search. They are established concepts, not newly generated contributions or evidence that more components improve novelty:

| Structure A | + Structure B | = Novel Composition |
|------------|---------------|---------------------|
| Coordination (1) | + Adversarial (6) | Byzantine fault-tolerant consensus |
| Phase boundary (5) | + Causal (7) | Tipping point identification in causal networks |
| Multi-scale (3) | + Representation (8) | Hierarchical disentangled representations |
| Information extraction (2) | + Strategic (4) | Private information retrieval |
| Resource allocation (9) | + Limited feedback (10) | Online resource allocation under uncertainty |

# Referee report — "Structure, invariants and obstructions in Collatz dynamics"

**Manuscript:** `paper/main.tex` (with the accompanying `collatz` package,
`REPORT.md`/`RELATORIO.md`, and `reproduce_paper_results.py`)
**Review type:** simulated academic peer review (expert in dynamical systems /
elementary and computational number theory)
**Date:** 2026-07-10

---

## 1. Summary of the submission

The manuscript studies the accelerated Collatz map T(n) = n/2 (n even),
(3n+1)/2 (n odd) and presents:

- **Contribution A (Theorem 3.2 + Corollary 3.5).** For every j ≥ 1 there is no
  "modular Lyapunov function" V(n) = log₂ n + w(n mod 2^j) that strictly
  decreases at every positive odd integer; the obstruction is the projection of
  the 2-adic fixed point −1, transported into ℤ₊ by the family
  n_m = 2^(j+1)m − 1. Robustness under finite exceptions, non-strict decrease,
  k-step blocks, and restricted domains is proved.
- **Contribution B (Theorems 4.3, 4.5).** The Syracuse Markov chain on ℤ₃
  (branches φ_a(x) = (3x+1)2^(−a) with probabilities 2^(−a)) has
  Dobrushin–Wasserstein coefficient ≤ 1/3; the dual inverse-branch chain on ℤ₂
  has coefficient exactly 1/2 and averages every level-k cylinder function to
  its Haar mean in exactly k steps.
- **Contribution C (Sections 5–7).** A pure-Python, exact-arithmetic laboratory:
  cycle enumeration via the closed form n = b(p)/(2^L − 3^k); Diophantine cycle
  exclusion with continued-fraction convergents of log₂ 3 certified by integer
  comparison of 2^p vs 3^q; Karp maximum-mean-cycle analysis of the residue
  graphs mod 2^j; exact rational transfer kernels mod 3^k and exact Wasserstein
  coefficients (τ₂ = 5/21, τ₃ = 455/1387, τ₄ = 7635497415/22906579627) via a
  closed form for W₁ on ultrametric quotients.

## 2. Verification performed by this referee

- Every proof in the manuscript was checked line by line: Theorem 3.2,
  Corollary 3.5, Lemma 2.3 (Dobrushin), Lemma 4.1 (geometric law of ν₂),
  Theorems 4.3 and 4.5, Propositions 5.1 (cycle equation), 5.2 (cycle
  inequality), 5.3 (Karp feasibility), and Lemma on W₁ over ℤ/p^kℤ.
  **No mathematical errors were found.**
- `python reproduce_paper_results.py` was executed in a clean environment:
  **all R1–R8 checks pass** (~4.5 s), confirming that every number quoted in
  the paper regenerates from scratch in exact arithmetic. The claimed arithmetic
  model (no floats in certified claims; certified rational upper bound for
  ε(N); symbolic acceptance condition for Karp runs) matches the code.
- Spot-checks against the literature: the cycle table (negative cycles −1,
  −5→−7→−10, cycle of −17; the 3n−1 and 3n+5 cycles), the stationary measure
  (1/3, 2/3) mod 3, the record stopping time / excursion values in R1, and the
  Eliahou-style exclusion figures under N = 2⁶⁸ are all consistent with known
  results.

## 3. Assessment

### 3.1 Soundness — high

The proofs are correct, the theorem/verification separation (Section 1.5) is
exemplary, and the reproducibility standard (single script, exact arithmetic,
CI) exceeds the norm for computational number theory submissions.

### 3.2 Novelty and relevance to the state of the art — modest

- **Theorem 3.2** is a clean formalization of a *folklore* phenomenon. That the
  residue class −1 mod 2^k rises for k consecutive accelerated steps (e.g.
  n = 2^k − 1) has been understood since Terras (1976) and Everett (1977), and
  it is standard intuition that descent arguments reading only a fixed finite
  dyadic residue cannot be uniform. The precise nonexistence statement for the
  class V = log₂ n + w(n mod 2^j) on ℤ₊ may well be unpublished — the authors
  properly disclaim priority — but experts will regard it as known-in-spirit.
  Importantly, the ruled-out class is narrow: serious descent arguments
  (Terras's stopping time, Tao 2019) use *variable-depth* stopping times, which
  the theorem does not touch (as the manuscript itself states in §1.4).
- **Theorems 4.3/4.5** follow in a few lines from |3|₃ = 1/3 and |2|₂ = 1/2:
  the inverse branches form a uniformly contractive iterated function system,
  and Banach's fixed point theorem does the rest. Unique ergodicity of the
  Syracuse model and its mod-3^k structure are anticipated by Matthews–Watts
  (Acta Arith. 43 (1984) 167–175; 45 (1985) 29–42) and implicit in Tao's
  construction of the Syracuse measure. The ℤ₂ statement is a functional-
  analytic re-reading of the classical Bernoulli-shift conjugacy
  (Terras; Bernstein–Lagarias 1996): finite-time averaging of cylinder
  observables is a textbook property of the shift's transfer operator. The
  *exact rational* finite-level coefficients τ_k appear to be new, but the
  manuscript itself proves (Remark 4.6) that Wasserstein contraction of global
  densities cannot constrain individual orbits, so their mathematical
  consequence is limited.
- **Contribution C is the genuinely valuable part**: a fully reproducible,
  dependency-free, exact-arithmetic laboratory whose certification scheme
  (integer certification of convergents, rational upper bound for the slack,
  symbolic acceptance of float-assisted runs) is a good model for
  computer-assisted number theory. The exclusion bounds themselves reproduce
  Eliahou/Simons–de Weger and are superseded by Hercher (J. Integer Seq. 26
  (2023), Art. 23.3.5: no m-cycles with m ≤ 91).

**Bottom line on state of the art:** the manuscript does not advance the
Collatz conjecture, improve any known bound, or introduce a method with clear
potential to do either. Its contributions are a rigorous no-go formalization,
a geometric repackaging of known mixing phenomena with exact constants, and a
high-quality reproducible laboratory.

### 3.3 Recommendation

Not suitable as a research contribution to a strong number theory or dynamics
journal. Suitable, after revision, as an **expository / experimental-mathematics
contribution** (e.g. Experimental Mathematics, Involve, the American
Mathematical Monthly for a distilled version, or an arXiv note), positioned
around the reproducible laboratory and the precise no-go statements rather
than around new theorems.

## 4. Itemized findings (all addressed in this revision)

| # | Severity | Finding | Resolution |
|---|----------|---------|------------|
| 1 | Factual error | README and two code docstrings attributed a verification limit of ≈2⁷¹ to Barina (2021); the published paper verifies 2⁶⁸ (the paper and reports were already correct). | Corrected to 2⁶⁸ in `README.md`, `collatz/cycles.py`, `collatz/__main__.py` (CLI default changed 71 → 68). |
| 2 | Factual error | `references.bib` credited "Marc Bernstein" for *The 3x+1 conjugacy map*; the author is **Daniel J. Bernstein**. | Fixed in `paper/references.bib`. |
| 3 | Overclaim | README implied uniqueness of the Karp optimal cycle ("relentlessly isolates"), contradicting the paper's own R4 caveat. | README aligned with the paper. |
| 4 | Overclaim | README's "τ₄ ≈ 0.33333206 ↗ 1/3" implied an established limit; the paper states the finite values prove no limit. | README reworded. |
| 5 | Overclaim | README presented the mod-3 stationary measure and rank collapse as discoveries of the code. | Attributed to Matthews–Watts (1984/85) and Tao (2019); reworded as exact reproduction. |
| 6 | Missing prior art | Matthews–Watts (mod-3^k Markov chains), Everett 1977 (independent of Terras), Hercher 2023 (current cycle-exclusion record) uncited; Bernstein–Lagarias 1996 in the .bib but never cited. | All added to `references.bib` and cited in the introduction, §2, Remark 3.6, §7.3, §7.6, and the Discussion. |
| 7 | Positioning | Remark 3.6 undersold the folklore status of the rising class −1 mod 2^j; the Discussion's claim that prior formulations "lack explicit constants" was unsupported. | Remark 3.6 broadened; Discussion softened and sourced. |
| 8 | Incompleteness (upgrade) | The rank collapse P_k^k = 𝟙π_k was only *verified* at k = 3, though it is provable for every k in three lines. | New Proposition (finite-time rank collapse) added to §5.4 with proof; R6 and both reports now present k = 3 as an implementation check. |
| 9 | Incompleteness (open point) | Whether τ(P) = 1/3 exactly on ℤ₃ was neither proved nor flagged. | Explicitly flagged as open in Remark 4.4. |

## 5. Minor comments (not blocking)

- Figure 1 is labeled "conceptual illustration, not an actual residue graph";
  a referee at a journal would ask for the true G₅ or for the figure's removal.
- The W₁ closed form on ultrametric quotients (Lemma 5.5) is likely known in
  the optimal-transport literature; a citation search before submission is
  advised.
- The R1 sieve limit has been raised to 10⁷ (pure CPython, few seconds; still
  dependency-free). The self-contained hypothesis now sits less far below the
  2⁷¹ record; the conditional Diophantine bound updates accordingly
  (k > 1,278 / > 2,019 elements).

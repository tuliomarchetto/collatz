# Collatz Lab — algorithmic search for invariants, symmetries and structure

[![CI](https://github.com/tuliomarchetto/Collatz/actions/workflows/ci.yml/badge.svg)](https://github.com/tuliomarchetto/Collatz/actions/workflows/ci.yml)

An exact-arithmetic computational laboratory (pure Python, no dependencies) to investigate the
**Collatz Conjecture** (3n+1) and affine sibling systems. The primary contribution of this project is a fully reproducible, dependency-free experimental framework for number theory, designed with strict certification: **no floating-point quantity participates in any certified claim**.

The laboratory investigates the problem from two complementary angles:

1. **Counterexample (Exact Search & Exclusion)** — systematic exact-arithmetic search for non-trivial cycles and divergent orbits, with detectors *validated on sibling systems that have real counterexamples* (3n−1 and 3n+5). It implements Diophantine cycle exclusion via certified integer convergents.
2. **Proof Constraints (Formalization of Folklore)** — explicit, rigorous formalization of structural properties that constrain where a counterexample could live.

Rather than proposing groundbreaking new theorems, the theoretical component provides an **obstruction map** of the problem based on precise formalizations of established phenomena: a formal no-go statement locating the 2-adic obstruction (the fixed point −1) that defeats every modular Lyapunov correction on the pointwise side — extended past the fixed-depth folklore to **every variable-depth adapted stopping-time scheme** (any rule that ever stops the all-ones parity word admits no bounded correction; the surviving rules must defer their decision beyond depth log₂ n, exactly where Terras's open coefficient stopping time conjecture lives) — paired with exactly computed Wasserstein contraction coefficients on the dual, measure-theoretic side (coefficient exactly 1/3 on ℤ₃ — with every finite-level coefficient in closed form — and exactly 1/2 on ℤ₂).

The laboratory uses **only the Python standard library** for its execution. You do not need to install anything to run the experiments.

```bash
python -m collatz all                     # full findings report
python -m collatz verify --limit 1000000  # counterexample sieve
python -m collatz cycles --d -1           # exact cycle enumeration (3n-1)
python -m collatz exclude --limit-bits 68 # Diophantine cycle exclusion
python -m collatz lyapunov --j 10         # Lyapunov function obstruction
python -m collatz stopping --rule coefficient --depth 6  # variable-depth no-go
python -m collatz spectral --k 4          # transfer operator mod 3^k
python -m collatz transfer --k3 3 --k2 6  # infinite transfer operator
python -m collatz tree --depth 120        # inverse-tree coverage
python -m collatz terras --k 18           # 2-adic structure
python reproduce_paper_results.py         # regenerate every number in the paper
```

If you want to run the test suite (which requires `pytest`), you should set up a virtual environment to avoid PEP 668 system-package errors:

```bash
make install                              # sets up a .venv and installs testing dependencies
make test                                 # runs the test suite
```

Equivalent `make` targets: `make install`, `make test`, `make reproduce`,
`make report`, `make paper`. The test suite and the reproduction script run
in CI (GitHub Actions) on Linux and macOS, CPython 3.9–3.13.

Notation: `T(n) = n/2` (n even), `(3n+d)/2` (n odd) — the accelerated map of
the `3n+d` system; `d = 1` is the Collatz problem, `d = −1` and `d = 5` are
the validation benches.

## The algorithms and what they find

### 1. `search` — direct counterexample search
Ascending sieve (only needs to iterate until the orbit drops below the
seed), O(1)-memory Brent cycle detection, and divergence probing. Collects
extremal records (stopping time ~ c·log n; excursion ~ n²).
**Validation:** applied to `3n−1`, it finds the non-trivial cycles
`{5,7,10}` and the cycle of 17 — the detector works; on `3n+1` nothing
turns up up to the swept limit.

### 2. `cycles.find_cycles` — **exact** cycle enumeration
Structural fact: a cycle of length L with k odd steps and parity vector p
satisfies `n = b(p)/(2^L − 3^k)` with `b(p)` a computable integer — finding
cycles is exact arithmetic, not simulation. The algorithm enumerates all
cycles of length ≤ L in **ℤ** and rediscovers on its own the three cycles
of negative integers (−1, −5, −17) and the cycles of `3n+5`. On positives,
for `d = 1`: only the trivial `{1,2}` — complete up to the swept length.

### 3. `cycles.cycle_exclusion_bound` — Diophantine cycle exclusion
From the multiplicative identity `2^L = Π(3 + 1/xᵢ)` around a cycle with
elements > N, it follows that `0 < L − k·log₂3 ≤ k·log₂(1 + 1/3N)`: the
ratio L/k approaches log₂3 *from above* with error ~ 1/(3N ln 2). The
theory of best rational approximations (convergents of the continued
fraction of log₂3, certified exactly by comparing `2^p` with `3^q`)
forbids this for small k. With N = 2⁷¹ (Barina's published computational
verification), **any non-trivial cycle has billions of odd steps** —
Eliahou/Simons–de Weger's method (the current state of the art, Hercher
2023, sharpens this further via constraints on the number of local
minima). This is the canonical example of a *structural invariant
(Diophantine approximation) that constrains counterexamples*.

### 4. `padic` — the fundamental symmetry: 2-adic conjugation with the shift
Exactly verifies Terras's theorem: the length-k parity vector is a
**bijection** on ℤ/2^k, and T is conjugate to the Bernoulli shift on the
2-adic integers. Consequences measured by the code: the parity census is
exactly Binomial(k, ½); the typical drift is `log₂3/2 − 1 < 0` (contraction
on average); the measure of the "still growing" set after k steps decays
exponentially at the large-deviations rate `1 − H(1/log₂3)`. This is the
formalization of why "almost every n descends" (Terras; Tao).

### 5. `invariants` — modular invariants and conserved partitions
* `induced_map_search`: searches for factorizations `T(n) mod m₂ = f(n mod
  m₁)`. Finding: **m₁ = 2m₂ always** — the only coordinate of the dynamics
  that factors is the 2-adic one; there is no hidden modular "clock".
* `conserved_partition`: bisimulation (partition refinement) over ℤ/m —
  any stable block would be a conserved discrete quantity. Finding: the
  partition refines completely (no discrete invariant beyond the 2-adic
  one).
* `transient_classes`: classes the dynamics abandons forever. Rediscovered
  classical fact: multiples of 3 are never re-entered; the inverse tree of
  1 lives in `n ≢ 0 (mod 3)`.

### 6. `invariants.karp_max_mean_cycle` — obstruction to a Lyapunov function
A natural strategy to prove global convergence would be to exhibit a
Lyapunov function of the form `f(n) = log n + w(n mod 2^j)` that decreases
strictly along orbits. It is a known mathematical fact that the existence
of cycles among the negative integers forbids the existence of such a
function over the whole line, but this algorithm recasts that
impossibility as an exact graph-optimization problem: the function `w`
exists **iff** the maximum mean cycle in the (non-deterministic) transition
graph on ℤ/2^j is strictly negative.

**The exact characterization of the obstruction:** the Karp algorithm not
only confirms the non-existence of `w` (maximum mean = `log₂3 − 1 > 0`), it
returns the self-loop at the residue `−1 mod 2^j` as an optimal cycle at
every tested level (uniqueness of the optimal cycle is not claimed).
Why `-1`? Under the accelerated map `T(n) = (3n+1)/2` (for odds), the
integer `-1` is a **fixed point** (`T(-1) = -1`). In the transition graph
modulo `2^j`, this shows up as a **self-loop** on node `2^j - 1`, whose
transitions are exclusively made up of odd steps. Since each odd step
carries an associated gain of `log₂(3/2) = log₂3 − 1`, this loop has a
strictly positive, uncompensable balance.

Mathematically, if we tried to build the compensating potential `w`, the
decrease condition along this self-loop would require:
`w(-1) - w(-1) + log₂3 - 1 < 0  ⟹  log₂3 - 1 < 0` (Contradiction!).
This rigorously shows that approaches based exclusively on finite residues
fail not because of a technical limitation, but because modular arithmetic
is "blind" to the difference between ℤ₊ (where we want to prove there is
no divergence) and the element `-1 ∈ ℤ₂` (where a genuine positive-growth
cycle exists). Any proof will need to break this 2-adic symmetry.

### 6b. `stopping` — variable-depth stopping-time potentials (strengthened no-go)
The fixed-depth obstruction above still leaves open the natural next
strategy: let both the number of steps between descent checkpoints and
the residue window read by the correction depend on `n` through an
**adapted stopping rule** (a prefix code of parity words — by Terras's
bijection, exactly a stopping time of the 2-adic filtration; examples:
"stop at the first even step", Terras's coefficient stopping time, any
truncation). The module `collatz/stopping.py` implements the theorem that
closes this class (paper, Theorem `thm:stopping`): **any rule that stops
the all-ones parity word — automatic for every bounded rule, by König's
lemma — admits no bounded correction `w(n)` whatsoever**, modular or not.
The module extends this impossibility to **any sublogarithmic envelope**
(checked exactly by the integer inequality `3^(q-p_) > 2^(q+p+)`) and 
**any monotone correction**. The proof replaces the single-step cancellation 
by a telescoping chain along `n = 2^ℓ·m − 1`, and the module makes it 
computational: it builds the **block graph** of any finite rule (validated 
by an exact Kraft sum), runs Karp on it, and certifies the obstruction cycle 
by the exact integer comparison `3^A > 2^L` — plus explicit Mersenne witnesses 
`n = 2^ℓ − 1` defeating any correction of prescribed oscillation or sublogarithmic 
bounds, verified in exact integer arithmetic. Ultimately, the unrestricted unbounded 
class is nonempty if and only if there are no nontrivial cycles. Rules escape 
only by never deciding on the all-ones word (`σ(n) > v₂(n+1)` for all n); the first 
open member of that boundary is Terras's coefficient stopping time conjecture, 
so the no-go is sharp.

### 7. `symmetries` — affine conjugations and rigidity
Exhaustive search for `φ(x) = ax + b` such that `φ∘T_d = T_{d'}∘φ`.
Findings: `φ(x) = −x` conjugates `3n+1` with `3n−1` (the cycles of `3n−1`
**are** the negative cycles of `3n+1` — the two "near-counterexample"
pieces of evidence are the same one, via symmetry); `φ(x) = d·x` embeds
`3n+1` into `3n+d` (self-similarity of the family). Affine automorphisms
of the mod-m transition graphs: only the identity — the projected dynamics
is rigid.

### 8. `spectral` — Syracuse transfer operator mod 3^k
Exact Markov chain (rational arithmetic, using that 2 is a primitive root
mod 3^k) of the Syracuse map projected onto (ℤ/3^k)*. **First exact
computation:** the uniform measure is *not* stationary — the exact
invariant measure mod 3 is π(1) = 1/3, π(2) = 2/3 (Syracuse iterates land
on 2 mod 3 twice as often as on 1, since `(3n+1)/2^a ≡ (−1)^a mod 3` with
`P(a odd) = 2/3`); `stationary_exact` computes the rational invariant
measure for every 3^k. These chains and their non-uniform stationary
vectors go back to Matthews–Watts (1984/85); the mod-3 measure is implicit
in Tao (2019) — the code reproduces them exactly rather than discovering
them. **Second result (proved for every k in the paper's rank-collapse
proposition):** the
spectrum beyond λ₁ = 1 is `{0}` — rows of P coincide for `r ≡ r'
(mod 3^{k-1})`, so P^k has rank 1 (`memory_loss_check` verifies this in
rational arithmetic at k = 3): the chain loses all memory mod 3^k in
exactly k steps. Structurally, the
nilpotency of this projection suggests that obstructions to convergence
cannot be detected by finite 3-adic arithmetic alone; the modular memory
dissipates, leaving the global/2-adic structure as the likely driver of the
asymptotic behavior (see Tao, 2019).

### 9. `tree` — inverse tree of 1
The conjecture ⇔ the pre-image tree `m → {2m, (2m−1)/3}` covers ℤ₊. The
algorithm measures coverage (→ 100% over the tested ranges), the growth
factor per level (≈ 4/3, as predicted by the branching heuristic;
Krasikov–Lagarias prove density ≥ X^0.84), and lists the smallest integers
still missing at each depth (candidates for further study).

### 10. `transfer` — the **infinite** transfer operator (replacing the mod 3^k projections)
The matrices of §8 are finite sections of the Koopman operator `U` of the
Syracuse chain `x ↦ (3x+1)·2^(−a)` acting on `C(ℤ₃)` — and its ℓ² gap is
trivial, so it says nothing in the limit. This module identifies the norm
in which the gap survives: each branch contracts the 3-adic metric by
**exactly 1/3** (exact check: the chain is a uniformly contractive IFS on
ℤ₃), and the **Wasserstein contraction coefficient has the proved closed
form τ_k = (1/3)(1−q²)/(1+q+q²), q = 2^(−2·3^(k−2))** — exact values
τ₂ = 5/21, τ₃ = 455/1387, τ₄ ≈ 0.33333206, strictly increasing to 1/3
with gap 1/3 − τ_k < 2^(−2·3^(k−2)), attained exactly on the pairs at
3-adic distance 3^(−(k−2)); hence **τ(P) = 1/3 exactly on ℤ₃** (the
coupling bound is sharp; no single pair attains the supremum). The
brute-force values certify the closed form independently
(`syracuse_tau_closed_form`, `syracuse_extremal_sphere_check`).
Hence `spec(U|Lip(ℤ₃)) ⊆ {1} ∪ {|z| ≤ 1/3}`: **global contraction** (Banach
in W₁) — a *unique* invariant measure on ℤ₃ (Tao's Syracuse measure; the
π_k form a projective family, exactly verified), equidistribution at rate
3^(−n), and `U^k f = π(f)` **exactly** in k steps (the rank collapse of §8
reread). Analogously on ℤ₂: `Lf(x) = ½f(2x) + ½f((2x−1)/3)` has
coefficient **exactly 1/2** and `L^k f =` the exact Haar average — maximal
mixing, the functional-analytic dual of Terras's conjugation (§4).
These results establish contraction in spaces of global densities.
However, in ℓ¹(ℤ₊) — where the conjecture actually lives —, every finite
section of the operator tested exhibits nilpotent behavior (spectrum {0})
and no elementary weight `n^θ` produces uniform contraction (due to the
same Karp obstruction, `n ≡ -1 mod 2^t`). This illustrates the conceptual
gap between C and D: contraction of global distributions (Wasserstein on
ℤ₃) does not rigorously imply the collapse of point masses on a Haar-null
set such as ℤ₊. Rigorous behavior in densities does not translate, in any
elementary way, into conclusions about individual orbits.

## Summary: what the findings say about proof vs. counterexample

* **Against a counterexample:** no cycle among positives up to the swept
  length (exact search, not sampling); any cycle has > 10⁹ odd steps
  (Diophantine); divergence requires forever avoiding a strictly negative
  average drift with binomial fluctuations (exponential cost, measured).
* **Against an elementary proof:** the Karp obstruction shows that no
  argument based on finite residues + log can close the problem — the
  negative/2-adic cycles are counterexamples *to the method*, not to the
  theorem.
* **Directions the toolkit leaves quantified:** the uniform spectral gap
  mod 3^k — **resolved** by the `transfer` module: in W₁/Lip(ℤ₃) it exists
  and equals exactly 2/3 (coefficient exactly 1/3, sharp, with the τ_k in
  closed form), with global contraction and a unique Syracuse measure; large-deviation rates for the "bad" set; inverse-tree
  density; and the exact frontier (cycle length, excursion height) where a
  counterexample could still hide. The limits of the spectral approach are
  also made explicit: finite projections (mod 3^k, 2-adic cylinders,
  finite-dimensional sections) have trivial spectrum {1} ∪ {0}, and the
  contraction guaranteed by the infinite limits occurs in weak topologies
  (such as the Wasserstein metric), which describe the evolution of
  distributions but do not impose a direct, unconditional constraint on
  individual points in ℤ₊.

## References
* R. Terras, *A stopping time problem on the positive integers*, Acta Arith. 30 (1976).
* C. J. Everett, *Iteration of the number-theoretic function f(2n)=n, f(2n+1)=3n+2*, Adv. Math. 25 (1977).
* K. R. Matthews, A. M. Watts, *A generalization of Hasse's generalization of the Syracuse algorithm*, Acta Arith. 43 (1984); *A Markov approach to the generalized Syracuse algorithm*, Acta Arith. 45 (1985).
* J. C. Lagarias, *The 3x+1 problem and its generalizations*, Amer. Math. Monthly 92 (1985).
* S. Eliahou, *The 3x+1 problem: new lower bounds on nontrivial cycle lengths*, Discrete Math. 118 (1993).
* J. Simons, B. de Weger, *Theoretical and computational bounds for m-cycles of the 3n+1 problem*, Acta Arith. (2005).
* I. Krasikov, J. C. Lagarias, *Bounds for the 3x+1 problem using difference inequalities*, Acta Arith. 109 (2003).
* T. Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi 10 (2022).
* D. Barina, *Convergence verification of the Collatz problem*, J. Supercomputing 77 (2021) — published verification of all n ≤ 2⁶⁸.
* D. Barina, *Improved verification limit for the convergence of the Collatz conjecture*, J. Supercomputing 81:810 (2025) — extends the verified limit to n ≤ 2⁷¹.
* C. Hercher, *There are no Collatz m-cycles with m ≤ 91*, J. Integer Seq. 26 (2023).

## Report and paper
The full mathematical report is available in [`RELATORIO.md`](RELATORIO.md)
(canonical, Brazilian Portuguese) and in [`REPORT.md`](REPORT.md) (English
translation). A formal manuscript (LaTeX, journal format, with complete
proofs and bibliography) lives in [`paper/main.tex`](paper/main.tex) — build
it with `make paper` (requires `latexmk`) or any TeX engine. Every number
quoted in the report and in the manuscript is regenerated and checked by
[`reproduce_paper_results.py`](reproduce_paper_results.py).

## Reproducibility
* No runtime dependencies (standard library only); `pytest` is the only
  development dependency (`requirements.txt` / `pyproject.toml`).
* `python reproduce_paper_results.py` recomputes results R1–R9 from scratch
  in exact arithmetic and exits nonzero if any value differs from the ones
  quoted in the paper (~3 s; `--quick` skips the slowest sections).
* CI runs the test suite and the reproduction script on every push.

## License
Code (`collatz/`) is released under the MIT License — see [LICENSE](LICENSE).
The written report (`RELATORIO.md` / `REPORT.md`) is released under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

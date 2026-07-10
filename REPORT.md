# Report: Structure, Invariants and Obstructions in Collatz Dynamics

*This is the English translation of [`RELATORIO.md`](RELATORIO.md), which remains the canonical Brazilian Portuguese version of this report. License: this document is distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (Creative Commons Attribution 4.0 International). The laboratory's source code (`collatz/`) is distributed separately under the MIT License — see `LICENSE`.*

This document formalizes the investigation of the Collatz Conjecture ($3n+1$ dynamics) and affine systems ($3n+d$). The report is divided into three strict parts:
1. **Part I: Mathematical Results**, containing theorems with purely analytic proofs (no dependence on computation). The central focus is the topological characterization of the failure of modular Lyapunov functions.
2. **Part II: Description of the Algorithms**, describing the exact computational methods designed to investigate the system (exact algebra, modular graphs, Wasserstein metric).
3. **Part III: Experimental Results and Verifications**, cataloguing the numerical limits, simulation findings, and computational certificates that instantiate the mathematical theories in practice.

**Separation of claims.** Part I contains only statements proved analytically; none of their proofs depends on a computation. Part III contains only computational verifications, each stated with its exact sweep limit. The empirical limits reported there (e.g. the convergence sieve at $200{,}000$) are deliberately modest and claim no novelty — the published verification record is $2^{68}$ (Barina 2021) — their role is to validate the detectors on systems with known counterexamples ($3n-1$, $3n+5$, the negative cycles of $3n+1$) and to instantiate the theorems of Part I at finite levels, not to extend numerical records.

**Formal manuscript and reproducibility.** A formal manuscript of this material (LaTeX, with complete proofs and pointed bibliography) is maintained in [`paper/main.tex`](paper/main.tex). Every number quoted in this report and in the manuscript is regenerated and checked by the script [`reproduce_paper_results.py`](reproduce_paper_results.py) (sections R1–R8), which exits with an error on any mismatch.

---

## Part I: Mathematical Results

*General notation.* Let $T$ be the accelerated Collatz map, $T(n) = n/2$ if $n$ is even, $(3n+1)/2$ if $n$ is odd. Let $S$ be the Syracuse map, $S(n) = (3n+1)/2^{\nu_2(3n+1)}$, defined on the odd integers. In $\mathbb{Z}_p$, $|x|_p$ denotes the $p$-adic norm.

### Main Theorem: The Modular Obstruction to a Lyapunov Function

**Hypotheses.** A natural strategy for proving global convergence would be to exhibit a Lyapunov function combining the macroscopic logarithmic trend with periodic local corrections. Specifically, fixing an arbitrary integer $j \ge 1$, we assume the existence of a function $V(n) = \log_2 n + w(n \bmod 2^j)$ that is strictly decreasing along any odd orbit in $\mathbb{Z}_+$. Here, the component $w : \mathbb{Z}/2^j\mathbb{Z} \to \mathbb{R}$ is an arbitrary function, acting strictly on the finite ring of residues. As an immediate corollary of its finite domain, $w$ is an inherently bounded function that, when evaluated on the integers, behaves as a periodic potential of period $2^j$.

**Statement.** No such function $V$ exists. More specifically, the existence of the potential $w$ runs into a structural, irreducible topological obstruction: the projection of the $2$-adic fixed point $-1$ onto $\mathbb{Z}/2^j\mathbb{Z}$ induces a strictly positive logarithmic-growth loop that no modular function can compensate for.

**Proof.**
Suppose, for contradiction, that there exists $w : \mathbb{Z}/2^j\mathbb{Z} \to \mathbb{R}$ such that for every odd integer $n > 0$, the accelerated step $T(n) = (3n+1)/2$ satisfies $V(T(n)) < V(n)$. This implies:
$$w(T(n) \bmod 2^j) - w(n \bmod 2^j) < - \log_2 \frac{T(n)}{n}.$$
To sidestep limiting arguments (which require justifying the preservation of strict inequalities) and to capture exactly the topology of $\mathbb{Z}_2$, consider the family $n_m = 2^{j+1}m - 1$, parametrized by any integer $m \geq 1$. Since $j \ge 1$, we have $n_m \ge 3$, which guarantees that every $n_m$ is a strictly positive odd integer. Therefore, this family is contained unconditionally and rigorously in the domain where the decrease hypothesis ($V(T(n)) < V(n)$) was assumed to hold.
Under the accelerated step, the exact image is:
$$T(n_m) = \frac{3(2^{j+1}m - 1) + 1}{2} = 3 \cdot 2^j m - 1.$$
Evaluating the residue classes modulo $2^j$, we obtain:
$n_m = 2^j(2m) - 1 \equiv -1 \pmod{2^j}$,
$T(n_m) = 2^j(3m) - 1 \equiv -1 \pmod{2^j}$.
Substituting $n_m$ into the Lyapunov inequality, the potential terms cancel identically on the left-hand side for any $m \ge 1$:
$$w(-1 \bmod 2^j) - w(-1 \bmod 2^j) < - \log_2 \frac{3 \cdot 2^j m - 1}{2^{j+1} m - 1}.$$
The inequality reduces to:
$$0 < - \log_2 \frac{3 \cdot 2^j m - 1}{2 \cdot 2^j m - 1}.$$
For this strict inequality to hold, the argument of the logarithm would need to be strictly less than $1$. Since the denominators are positive, this would require:
$$3 \cdot 2^j m - 1 < 2 \cdot 2^j m - 1 \implies 3 < 2,$$
which is a flagrant arithmetic contradiction over the integers.

The impossibility follows directly from a fundamental dynamical obstruction: in $\mathbb{Z}_2$, the integer $-1$ is an odd fixed point ($T(-1)=-1$). In finite projected arithmetic, the modular function assimilates this growth as an uncompensable stationary cycle (of non-zero logarithmic gain), forcing the local function to fail on the family $n_m$ that orbits it. Regardless of the existence of other global constraints, this mechanism acts as a self-sufficient, unavoidable structural failure for any function of this class. $\square$

**Note on the Literature:** To the best of our verification, this specific formulation does not seem to appear explicitly in the classical and contemporary literature on the problem (such as in works by Terras, Lagarias, Eliahou, Simons–de Weger, and Tao). While the non-existence of a modular Lyapunov function over all the integers is an expected corollary of the existence of cycles among the negatives, we argue that the fixed point $-1 \in \mathbb{Z}_2$ constitutes, on its own, a *structural* and *irreducible* topological obstruction to potentials of period $2^j$, which may constitute a novel formulation when restricted to $\mathbb{Z}_+$. It aims to establish in a logically consistent manner why approaches based strictly on finite residues face insurmountable barriers.

**Robustness Corollaries (Resilience of the Theorem):**
The topological-failure mechanism anchored at the fixed point $-1$ is robust to the usual relaxations of the definition of stability functions:
1. **Finite Exceptions:** If the decrease requirement is only required to hold "outside a finite set", the obstruction persists. The test family $n_m = 2^{j+1}m - 1$ has infinite cardinality; hence, for any finite set of exceptions, there exists a sufficiently large $m$ such that $n_m$ falls back into the decrease region, reactivating the contradiction.
2. **Non-Strict Decrease:** Allowing ties ($V(T(n)) \le V(n)$) transforms the final inequality into $3 \le 2$, preserving the arithmetic impossibility. The function fails not only to force convergence, but even to prove that the orbit does not escape to infinity.
3. **Condition on Multiple Iterations ($T^k$):** Evaluating feasibility over blocks of $k$ steps ($V(T^k(n)) < V(n)$) does not bypass the obstruction. Since the point $-1$ is invariant, parametrizing a deeper subfamily $n_m = 2^{j+k}m - 1$, all of the first $k$ steps over it will necessarily be odd. The image will be $T^k(n_m) = 3^k \cdot 2^j m - 1$. The modular cancellation $w(-1) - w(-1) = 0$ still holds, and the decrease constraint collapses to $3^k < 2^k$, which is false for every $k \ge 1$.
4. **Restricted Domain:** Restricting the decrease hypothesis to only a subset of the orbits is tautological with respect to the conjecture. If the domain of validity excludes the family $n_m$, the convergence theorem will not be global. If the domain includes it (or includes any family adjacent to the 2-adic fixed point), the logical time bomb is armed and the function fails.

---

### Theorems on Global Contraction and the Infinite Spectrum

These results formulate the stochastic contraction of the map on the $p$-adic closures.

**Theorem 1 (Wasserstein Contraction in $\mathbb{Z}_3$).** The Koopman operator $U$ of the Syracuse chain, acting on the space of Lipschitz functions on $\mathbb{Z}_3$, obeys a rigid uniform contraction. For any depth $k \ge 1$, the Dobrushin-Wasserstein coefficient of the kernel projected onto $\mathbb{Z}/3^k\mathbb{Z}$ is globally bounded by $\tau_k \leq 1/3$.
*Proof.* Each deterministic inverse branch $\varphi_a(x) = (3x+1)2^{-a}$ of the Syracuse tree produces, in the $\mathbb{Z}_3$ ultrametric, an exact scaled isometry: $|\varphi_a(x) - \varphi_a(y)|_3 = |3|_3 \cdot |x - y|_3 = \frac{1}{3} |x - y|_3$. By coupling the iterated distributions without crossing heterogeneous branches, the $W_1$ transition metric incurs the same $\frac{1}{3}$ penalty. This forces the restricted linear spectrum of $U$ to compact entirely into the region $|z| \leq 1/3$ and to collapse toward the attracting uniqueness of a Syracuse measure. $\square$

**Theorem 2 (2-Adic Dynamical Duality).** The Ruelle-Perron-Frobenius Transfer operator $L$ acting on the ring $\mathbb{Z}_2$ has a Wasserstein transport coefficient of exactly $1/2$.
*Proof.* The pairs of antecedent branches of the dynamics on $\mathbb{Z}_2$ are uniquely described by $\psi_0(x) = 2x$ (even branch) and $\psi_1(x) = (2x-1)/3$ (odd branch). Since $|2|_2 = 1/2$ and $|3|_2 = 1$, both operate isometrically with contraction $1/2$ under the 2-adic topology (i.e., $|\psi_i(x) - \psi_i(y)|_2 = \frac{1}{2}|x-y|_2$). The aggregate $W_1$ contraction of $L$ has no choice but to rigorously amount to $1/2$, revealing the latent symmetry that the process $L$ is nothing other than the isometric dual of Terras's metric conjugacy with the discrete shift, devoid of long-term memory. Integration against the Haar measure decays as $2^{-n}$. $\square$

---

## Part II: Description of the Algorithms

The foundation of our investigative laboratory rests on strict computational modeling free of precision drift. We avoid naive iterative simulation in favor of resolutive algebra (heavy use of the local `fractions` library and extended integers).

### 1. Algebraized Cycle Enumeration and Diophantine Exclusion
* **Exact Solution:** A basic premise of the project is that a hypothetical cycle of length $L$ generating $k$ odd transformations (following the local parity vector $p$) requires its elements to arise from the closed form $n = b(p)/(2^L - 3^k)$, where $b(p)$ comes from the base-2 expansions of the transition weights. The algorithm developed discovers attractors by systematically searching for exact factors of the Diophantine equation over all vectors $p$, rather than searching for loops via brute-force simulation. This allows sweeping $\mathbb{Z}$ (e.g., negative integers) at a fraction of the effort.
* **Diophantine Certificate:** Using continued fractions applied to the mechanical fact that $2^L = \prod (3+1/x_i)$, our algorithm mapped the minimal interval of $L/k$ against the infinite precision of $\log_2 3$ (raw arithmetic comparisons of prime-base powers $2^p$ versus $3^q$). This purges billions of trivial candidates.

### 2. Obstruction Identifier (Karp's Algorithm)
To physically certify the obstruction mechanism established in the Main Theorem locally (without taking a limit to infinity), the modular transition dynamics under $\mathbb{Z}/2^j\mathbb{Z}$ was encoded as a stochastic weighted graph.
* An odd step assigns the edge a logarithmic weight $\log_2 3 - 1$, while even edges inherit $-1$.
* The divergent classes in the mesh form the *Maximum Mean Cycle*. Running Richard Karp's algorithm over our $2^j$ topology, the laboratory exactly and inductively extracts the fatal mean and the vertices responsible for the disruption.

### 3. Spectra via Metric Arithmetic
The dynamics of the matrix $P_k$ and the Kolmogorov $W_1$ metric for $\tau_k$ (described in Theorems $1$ and $2$) were mechanized by formulating algorithms to extract the adjoint matrix of the chains over the finite ring.

### 4. Methodology: Exact Arithmetic
The rule governing the whole laboratory is: **no floating-point quantity participates in any certified claim.** Concretely:
* **Integers and rationals.** All integer arithmetic uses arbitrary-precision integers (no overflow is possible; quantities like $3^q$ with $q \approx 10^5$ are exact). All rational arithmetic — transfer matrices, stationary measures, Wasserstein distances, the coefficients $\tau_k$, the cycle equation $n = b(p)/(2^L - 3^k)$ — uses exact fractions (the `fractions` module). Values such as $\tau_3 = 455/1387$ are exact outputs; decimal expansions are display-only.
* **The constant $\log_2 3$.** The only irrational constant of the toolkit enters at two points, both handled without trusting floating point. (i) The convergents of its continued fraction are extracted from a 120-digit decimal approximation and then **certified exactly**: the predicted alternation $p/q \gtrless \log_2 3$ is equivalent to the integer comparison $2^p \gtrless 3^q$, checked in exact integer arithmetic for every denominator $q \le 10^5$ (covering the range our bounds use); a certification failure would raise an error. (ii) The slack $\varepsilon(N) = \log_2(1 + 1/(3N))$ of the Diophantine exclusion is replaced by a certified rational **upper** bound (the 120-digit value rounded up by one unit in the last place); any overestimate only weakens the resulting bound $K$, never its validity. Neither computation can suffer overflow or precision loss.
* **Where floats do appear.** Karp's algorithm runs its dynamic program on IEEE double weights for speed, but its verdict is certified symbolically: the maximum cycle mean is *proved* to equal $\log_2 3 - 1$ (no edge weight exceeds $\log_2 3 - 1$, and the self-loop at $-1 \bmod 2^j$ attains it), and a run is accepted only if the extracted optimal cycle consists solely of odd residues — an exact condition under which its mean is $\log_2 3 - 1$ by construction. The float value agrees to $< 2\cdot 10^{-15}$, as expected. Likewise, the power-iteration estimate of $|\lambda_2|$ is a numerical diagnostic only; the certified counterpart is the exact rank collapse $P_k^{\,k} = \mathbf{1}\pi_k$, verified in rational arithmetic.
* **Determinism.** There is no Monte Carlo component; all algorithms are deterministic and re-runs are bit-identical across platforms.

---

## Part III: Experimental Results and Verifications

Below we report the absolute quantifications obtained by applying the computational engines detailed in Part II. Everything in this part is a **verification with an explicit finite limit**, not a theorem; each number is regenerated by `reproduce_paper_results.py`.

### Global Computational Sieve and Inverse Tree
* **Initial Positive Bounds:** Closure to 1 was attested for all non-zero naturals below $200{,}000$ under ascending linear detection; no cyclic deviation was documented. (This is far below the published record $2^{68}$, Barina 2021; it is included solely as a self-contained, re-runnable hypothesis for the Diophantine exclusion below.)
* **Diffusion Balance (Inverse Tree):** The mechanical construction rigorously attested that depth $113$ is the minimum degree needed for the inverted Syracuse tree to encapsulate all naturals under the empirical threshold of $1000$. With $30$ levels mapped in absolute terms, the subset covers the entire internal spectrum in $[123, 2147483648]$.

### Analytical Discovery of Extended Cycles
* Applying the rational engine of section II.1 to the classical $3n+1$ dynamics, the system deterministically diagnosed the orbits of the negative-integer family: $\{-1\}$ and the isolated double loops at $\{-5\}$ and $\{-17\}$, confirming the topological completeness of the search.
* Reconfigured for the sibling maps $3n-1$ and $3n+5$, it verified the real, pointwise presence of the irregular cycles characteristic of these neighborhoods (e.g., the transitive loop of 19 and 49, proving that cyclic anomalies are not restricted but normative, depending on the operated delta).

### Exclusion via Diophantine Compression
* Operationalizing the attested boundary ($N = 200{,}000$), it was numerically proven that the occurrence of any non-trivial closed orbit would force a loop with a strict minimum base of 676 direct iterations (containing no fewer than 428 increments). If the limit were raised to the levels published contemporaneously ($2^{71}$), this cyclic path grows beyond $103$ billion items — ratifying the escaping character of the dynamics.

### Physical Evidence of the Topologies
* **Empirical Rank Collapse ($3^k$):** Evaluating the Syracuse operator at $k=3$ (ring $\mathbb{Z}/27\mathbb{Z}$), spectral convergence precisely zeroed out all supplementary eigenvalues. The measure converged irrefutably to the rational proportions $1/3$ and $2/3$, breaking trivial symmetries and instantiating, at a finite test dimension, the collapse predicted by Theorem 1.
* **Absolute Measures ($\tau_k$ Wasserstein):** For $k \in \{2, 3, 4\}$, the exact fractional values returned were $\tau_2 = 5/21$, $\tau_3 = 455/1387$, and $\tau_4 \approx 0.33333206$. The differential threshold error falls monotonically, proving the restricted ascent toward the global bound $\frac{1}{3}$.
* **Practical Identification of $-1 \bmod 2^j$:** Running the *Karp Mean Cycle* analysis for iterated moduli in the range $j = 5 \dots 10$, the returned mean settled, in a computationally unconditional way, at the constant peak of $0.584962$ — the value $\log_2 3 - 1$, certified symbolically per the methodology of Part II §4 (the float agrees to $< 2\cdot 10^{-15}$). In $100\%$ of the runs performed, the subgraph responsible for the disruption contained one and only one residue-class signature: the one generated strictly by the transient modulus of the integer $-1$.

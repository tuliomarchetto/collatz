"""
INFINITE transfer operator: from mod 3^k projections to operators on
p-adic function spaces.

Motivation. The `spectral` module builds the transfer matrices of the
Syracuse chain projected onto Z/3^k and finds that its spectrum is
trivial ({1} ∪ {0}: rank collapse in k steps). The ℓ² spectral gap of
the finite sections therefore carries NO information in the limit
k → ∞. This module replaces the projections with operators on the
infinite spaces of which they are sections, and identifies the norm in
which the spectral gap survives the limit — and is uniform in k.

1. Koopman operator of the Syracuse chain on C(Z_3). The chain
   x ↦ (3x+1)·2^{-a}, P(a) = 2^{-a}, makes sense on Z_3 (2 is invertible)
   and is an IFS with UNIFORM contraction: each branch
   phi_a(x) = (3x+1)·2^{-a} satisfies

       |phi_a(x) − phi_a(y)|_3 = (1/3)·|x − y|_3      (exact, since
       phi_a(x) − phi_a(y) = 3·2^{-a}(x−y) and |2|_3 = 1, |3|_3 = 1/3).

   Spectral consequences (verified exactly here at finite levels):
   * The Wasserstein (Dobrushin) contraction coefficient of the kernel
     is <= 1/3 at EVERY level 3^k — a bound uniform in k, unlike the
     ℓ² gap (exact values: 5/21, 455/1387, ... ↗ 1/3). Hence, on the
     space Lip(Z_3), U = Pi + R with Pi = rank-1 projection onto the
     invariant measure and spectral radius of R <= 1/3.
   * Global contraction (Banach fixed point in Wasserstein): there
     exists a UNIQUE invariant measure mu on Z_3 — the "Syracuse
     measure" (Tao 2019) — and every initial measure converges
     exponentially, at rate 3^{-n}. The finite stationary distributions
     pi_k form a consistent projective family (exact verification):
     they ARE the values of mu on the cylinders.
   * Finite-time equidistribution: U^k f = pi_k(f) EXACTLY for every f
     of level k (a re-reading of the rank collapse from `spectral`: it
     is the shadow of the 1/3 contraction — level-k functions have
     3-adic "frequency" k and each U step erases one digit).

2. Transfer operator of T on C(Z_2). Every x in Z_2 has exactly two
   T-preimages, 2x and (2x−1)/3 (3 is invertible in Z_2), each with Haar
   Jacobian 1/2:

       (Lf)(x) = (1/2)·f(2x) + (1/2)·f((2x−1)/3).

   Each inverse branch contracts the 2-adic metric by exactly 1/2; the
   Wasserstein coefficient is EXACTLY 1/2 at every level 2^k; L^k f =
   the exact Haar average. Spectrum in Lip(Z_2): {1} ∪ disk of radius
   1/2 — maximal mixing, invariant density = Haar (the functional-
   analytic dual of the Terras conjugacy with the shift, module `padic`).

3. Where the conjecture lives: ℓ¹(Z_+). The contractions above are
   global on spaces where Z_+ is invisible (Haar-null; point masses are
   not Lipschitz-dual). This module measures exactly what remains on
   Z_+:
   * Finite sections [1, N] of the pushforward of T are NILPOTENT
     outside the cycle {1,2} (the graph is a DAG — any cycle would be a
     counterexample): spectrum {0} again, with nilpotency index ~ c·log N.
   * NO pure weight w(n) = n^theta gives a uniform contraction in ℓ¹_w
     in t steps, for ANY t: exact witness n = 2^t − 1 ≡ −1 (mod 2^t)
     with t consecutive odd steps and ratio
     T^t(n)/n = (3^t−1)/(2^t−1) > 1. It is the SAME obstruction as
     Karp's cycle (`invariants`): the 2-adic point −1.
   * The contraction on Z_+ is only "in density": the mass not yet
     absorbed into {1,2} decays exponentially at a rate measured by
     absorption_profile (reference: large-deviations rate
     2^{-(1-H(1/log2 3))} per step).

Spectral synthesis: all compact/finite faces of the problem have
trivial spectrum {1} ∪ {0}, and the infinite operators have MAXIMAL
spectral gaps (radius 1/3 on Z_3, 1/2 on Z_2) with proved global
contraction. The conjecture is not a spectral question on any
homogeneous space: it lives exactly on the singular boundary
Z_+ ⊂ Z_2 (measure zero), where the dynamics moves point masses
isometrically and density contraction does not reach it.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

from .core import T, total_stopping_time
from .spectral import stationary_exact, syracuse_transfer_matrix

Measure = Dict[int, Fraction]


def _vp(n: int, p: int) -> int:
    """p-adic valuation of a nonzero integer."""
    if n == 0:
        raise ValueError("v_p(0) is infinite")
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def _vp_fraction(q: Fraction, p: int) -> int:
    """p-adic valuation of a nonzero rational."""
    return _vp(q.numerator, p) - _vp(q.denominator, p)


# ---------------------------------------------------------------------------
# Exact Wasserstein distance in p-adic ultrametrics
# ---------------------------------------------------------------------------

def wasserstein_padic(mu: Measure, nu: Measure, p: int, k: int) -> Fraction:
    """EXACT (rational) Wasserstein W1 distance between measures of equal
    mass on Z/p^k with the p-adic metric d(x, y) = p^{-v_p(x-y)}.

    In ultrametrics the optimal transport is the hierarchical greedy
    matching (cell by cell), which gives the closed form

        W1 = sum_{j=1}^{k-1} (p^{-(j-1)} - p^{-j})·m_j  +  p^{-(k-1)}·m_k,

    where m_j = (1/2)·sum_{c mod p^j} |mu(c) - nu(c)| is the mass that
    must cross level-j cell boundaries. (Lower bound: every coupling
    moves >= m_j across level j; the greedy matching attains every m_j
    simultaneously.)"""
    W = Fraction(0)
    for j in range(1, k + 1):
        pj = p ** j
        cells: Dict[int, Fraction] = {}
        for r, m in mu.items():
            cells[r % pj] = cells.get(r % pj, Fraction(0)) + m
        for r, m in nu.items():
            cells[r % pj] = cells.get(r % pj, Fraction(0)) - m
        m_j = sum(abs(v) for v in cells.values()) / 2
        if j < k:
            W += (Fraction(1, p ** (j - 1)) - Fraction(1, p ** j)) * m_j
        else:
            W += Fraction(1, p ** (k - 1)) * m_j
    return W


def w1_contraction_coefficient(P: Dict[int, Measure], p: int, k: int
                               ) -> Tuple[Fraction, Optional[Tuple[int, int]]]:
    """EXACT Wasserstein (Dobrushin) contraction coefficient of the
    kernel P at level p^k:

        tau = max_{x != y}  W1(P[x], P[y]) / d(x, y).

    tau < 1 implies global contraction: a unique invariant measure and
    W1 convergence at rate tau^n from ANY initial measure (Banach); the
    Koopman operator satisfies Lip(Uf) <= tau·Lip(f) (Kantorovich
    duality), hence spec(U|Lip) ⊆ {1} ∪ {|z| <= tau}. tau is computed
    exactly and, unlike the ℓ² gap of the finite sections, it is
    UNIFORM in k — it is the spectral property that survives to the
    infinite operator."""
    states = sorted(P)
    best = Fraction(0)
    arg: Optional[Tuple[int, int]] = None
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            d = Fraction(1, p ** _vp(x - y, p))
            ratio = wasserstein_padic(P[x], P[y], p, k) / d
            if ratio > best:
                best, arg = ratio, (x, y)
    return best, arg


# ---------------------------------------------------------------------------
# 1. The infinite operator on Z_3 (Syracuse chain)
# ---------------------------------------------------------------------------

def syracuse_branch_contraction_check(k: int, amax: int = 6) -> bool:
    """Verifies EXACTLY that each branch phi_a(x) = (3x+1)/2^a of the
    Syracuse chain contracts the 3-adic metric by exactly a factor 1/3:

        v_3(phi_a(x) - phi_a(y)) = v_3(x - y) + 1

    for all pairs of states x != y mod 3^k and every a <= amax. (The
    values phi_a(x) are 2-integral rationals, hence elements of Z_3; the
    check uses exact rational arithmetic.) This is the fact that makes
    the chain a uniformly contractive IFS on Z_3."""
    states = [r for r in range(3 ** k) if r % 3 != 0]
    for a in range(1, amax + 1):
        for i, x in enumerate(states):
            for y in states[i + 1:]:
                diff = Fraction(3 * x + 1, 2 ** a) - Fraction(3 * y + 1, 2 ** a)
                if _vp_fraction(diff, 3) != _vp(x - y, 3) + 1:
                    return False
    return True


def syracuse_w1_coefficient(k: int) -> Tuple[Fraction, Optional[Tuple[int, int]]]:
    """Exact Wasserstein coefficient of the Syracuse chain at level 3^k.

    FINDING: tau_k <= 1/3 for EVERY k (bound proved by coupling equal
    `a` + the 1/3 contraction of the branches; computed exactly here),
    with exact values tau_2 = 5/21, tau_3 = 455/1387,
    tau_4 = 7635497415/22906579627 ≈ 0.33333206 ↗ 1/3: in the finite
    sections, couplings between distinct branches still help, but in the
    limit the coefficient of the infinite operator is exactly 1/3. The
    uniform bound tau <= 1/3 is the spectral gap that survives as
    k → ∞: spec(U|Lip(Z_3)) ⊆ {1} ∪ {|z| <= 1/3}."""
    _, P = syracuse_transfer_matrix(k)
    return w1_contraction_coefficient(P, 3, k)


def stationary_projective_check(k: int) -> bool:
    """Verifies EXACTLY that the finite stationary measures form a
    projective family: the projection mod 3^{k-1} of pi_k is pi_{k-1}.

    Consequence (with the 1/3 contraction, via Banach/Kolmogorov): the
    pi_k are the cylinder values of the UNIQUE invariant measure mu on
    Z_3 — the Syracuse measure whose equidistribution feeds Tao 2019."""
    pi_k = stationary_exact(k)
    pi_prev = stationary_exact(k - 1)
    M = 3 ** (k - 1)
    proj: Dict[int, Fraction] = {}
    for r, m in pi_k.items():
        proj[r % M] = proj.get(r % M, Fraction(0)) + m
    return proj == pi_prev


def koopman_decay_profile(k: int, f: Optional[Dict[int, Fraction]] = None) -> Dict:
    """Iterates the Koopman operator U^n f at level 3^k, EXACTLY, and
    measures

        dev_n = max_x |U^n f(x) - pi(f)|.

    Spectral checks embedded in the result:
    * dev_n <= Lip_3(f)·(1/3)^n  (the 1/3 contraction in action: 'decay'
      returns True if the bound holds for every n);
    * dev_k = 0 EXACTLY ('finite_time' True): U^k f is constant = pi(f)
      — finite-time equidistribution on the cylinders, the spectral
      re-reading of the rank collapse from `spectral.memory_loss_check`."""
    states, P = syracuse_transfer_matrix(k)
    pi = stationary_exact(k)
    if f is None:  # "generic" test function (rational, not Lipschitz-tuned)
        f = {r: Fraction((r * r + 1) % 11, 11) for r in states}
    lip = Fraction(0)
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            lip = max(lip, abs(f[x] - f[y]) * 3 ** _vp(x - y, 3))
    mean = sum(pi[r] * f[r] for r in states)
    devs: List[Fraction] = []
    g = f
    for _ in range(k):
        g = {x: sum(w * g[y] for y, w in P[x].items()) for x in states}
        devs.append(max(abs(g[x] - mean) for x in states))
    decay = all(dev <= lip * Fraction(1, 3 ** (n + 1))
                for n, dev in enumerate(devs))
    return {"lipschitz": lip, "mean": mean, "devs": devs,
            "decay": decay, "finite_time": devs[-1] == 0}


# ---------------------------------------------------------------------------
# 2. The infinite operator on Z_2 (transfer operator of the accelerated map T)
# ---------------------------------------------------------------------------

def inverse_branches_check_2adic(k: int) -> bool:
    """Verifies EXACTLY, mod 2^k, that the two branches of the transfer
    operator are the T-preimages on Z_2 and that each contracts the
    2-adic metric by exactly a factor 1/2:

        T(2x) = x;   y = (2x-1)/3 is odd in Z_2 and T(y) = x;
        v_2(branch(x) - branch(y)) = v_2(x - y) + 1."""
    M2 = 1 << (k + 1)                       # work mod 2^{k+1} to see v+1
    inv3 = pow(3, -1, M2)
    for x in range(1 << k):
        y = ((2 * x - 1) * inv3) % M2
        if y % 2 == 0:                       # (2x-1)/3 must be odd in Z_2
            return False
        if (3 * y + 1) // 2 % (1 << k) != x:  # T(y) = x mod 2^k
            return False
    for x in range(1 << k):
        for y in range(x + 1, 1 << k):
            v = _vp(x - y, 2)
            b0 = (2 * x - 2 * y) % M2
            b1 = ((2 * x - 1) * inv3 - (2 * y - 1) * inv3) % M2
            for b in (b0, b1):
                if v + 1 < k + 1 and _vp(b if b else M2, 2) != v + 1:
                    return False
    return True


def transfer_2adic_matrix(k: int) -> Dict[int, Measure]:
    """Kernel of T's transfer operator at level 2^k:

        (Lf)(x) = (1/2)f(2x) + (1/2)f((2x-1)/3)   (mod 2^k, 3 invertible).

    This is the 'reverse' Markov chain (walk on the inverse branches
    with Haar weights). Doubly stochastic: Haar (uniform) is the
    invariant density — L1 = 1 and each y's column sums to 1."""
    M = 1 << k
    inv3 = pow(3, -1, M)
    half = Fraction(1, 2)
    P: Dict[int, Measure] = {}
    for x in range(M):
        row: Measure = {}
        for img in ((2 * x) % M, ((2 * x - 1) * inv3) % M):
            row[img] = row.get(img, Fraction(0)) + half
        P[x] = row
    return P


def transfer_2adic_w1_coefficient(k: int) -> Tuple[Fraction, Optional[Tuple[int, int]]]:
    """Exact Wasserstein coefficient of the 2-adic transfer operator.

    FINDING: tau = 1/2 EXACTLY for every k >= 2 — spec(L|Lip(Z_2)) ⊆
    {1} ∪ {|z| <= 1/2}, the maximal spectral gap of the 2-to-1 map: the
    functional-analytic analogue of the Terras conjugacy with the
    Bernoulli shift."""
    return w1_contraction_coefficient(transfer_2adic_matrix(k), 2, k)


def haar_mixing_check_2adic(k: int, f: Optional[Dict[int, Fraction]] = None) -> bool:
    """Verifies EXACTLY that L^k f = the Haar average of f, for an
    arbitrary rational f of level 2^k: complete finite-time mixing on
    the cylinders (L sends level-k functions to level-(k-1) functions —
    each step erases one 2-adic digit, an exact mirror of the Terras
    shift)."""
    M = 1 << k
    P = transfer_2adic_matrix(k)
    if f is None:
        f = {x: Fraction((x * x * x + x + 1) % 13, 13) for x in range(M)}
    mean = sum(f.values()) / M
    g = f
    for _ in range(k):
        g = {x: sum(w * g[y] for y, w in P[x].items()) for x in range(M)}
    return all(v == mean for v in g.values())


# ---------------------------------------------------------------------------
# 3. Where the conjecture lives: the pushforward on ℓ¹(Z_+)
# ---------------------------------------------------------------------------

def finite_section_nilpotency(N: int, d: int = 1) -> Dict:
    """Finite section [1, N] of T's pushforward operator (system 3n+d):
    the graph n -> T(n) restricted to [1, N], with 1's trivial cycle
    removed.

    The section is NILPOTENT iff the graph is acyclic — any cycle would
    be a genuine nontrivial cycle of T (a counterexample). Returns
    {'acyclic', 'index', 'witness', 'cycle'}: index = nilpotency index
    (smallest t with L^t = 0 on the section) = number of nodes on the
    longest path.

    FINDING: for d=1 the spectrum of EVERY finite section is {0}
    (outside {1,2}), with index ~ c·log N — the third finite face of the
    problem with trivial spectrum. Detector VALIDATION: for d=-1 the
    algorithm finds the cycle {5, 7, 10} (the section is NOT nilpotent —
    the spectrum flags the counterexample)."""
    # trivial cycle: orbit of 1
    triv = {1}
    x = T(1, d)
    while x not in triv:
        triv.add(x)
        x = T(x, d)
    depth = {}
    for start in range(1, N + 1):
        if start in triv or start in depth:
            continue
        stack = [start]
        onstack = {start}
        while stack:
            n = stack[-1]
            t = T(n, d)
            if t > N or t in triv:
                depth[n] = 1 + depth.get(t, 0) if t in depth else 1
                stack.pop()
                onstack.discard(n)
            elif t in onstack:                      # nontrivial cycle!
                cyc = []
                i = len(stack) - 1
                while stack[i] != t:
                    cyc.append(stack[i])
                    i -= 1
                cyc.append(t)
                return {"acyclic": False, "index": None,
                        "witness": None, "cycle": sorted(cyc)}
            elif t in depth:
                depth[n] = 1 + depth[t]
                stack.pop()
                onstack.discard(n)
            else:
                stack.append(t)
                onstack.add(t)
    if not depth:
        return {"acyclic": True, "index": 0, "witness": None, "cycle": None}
    witness = max(depth, key=depth.get)
    return {"acyclic": True, "index": depth[witness],
            "witness": witness, "cycle": None}


def power_weight_obstruction(t: int) -> Dict:
    """Computable proof that NO pure weight w(n) = n^theta makes the
    pushforward a uniform contraction of ℓ¹_w in t steps, for ANY theta
    and ANY fixed t.

    Exact witness: n = 2^t − 1 ≡ −1 (mod 2^t) has t consecutive odd
    steps (all-1 parity vector, Terras), hence

        T^t(n)/n = (3^t − 1)/(2^t − 1) > 1   (exact),

    and the family n = 2^t·m − 1 gives ratios → (3/2)^t with arbitrarily
    large witnesses: sup_n (T^t(n)/n)^theta > 1 for theta > 0. For
    theta <= 0 the pairs n = 2^t·m fail (ratio 2^{-t·theta} >= 1). It is
    the SAME obstruction as Karp's maximum mean cycle (`invariants`):
    the 2-adic periodic point −1. Contraction on Z_+ cannot be
    uniform — only 'in density' (absorption_profile)."""
    n = 2 ** t - 1
    x = n
    parities = []
    for _ in range(t):
        parities.append(x & 1)
        x = T(x)
    ratio = Fraction(x, n)
    return {"t": t, "n": n, "all_odd": all(p == 1 for p in parities),
            "endpoint": x, "ratio": ratio,
            "ratio_matches_formula": ratio == Fraction(3 ** t - 1, 2 ** t - 1),
            "limit_ratio": (1.5) ** t}


def absorption_profile(N: int, stride: int = 20) -> Dict:
    """Measured contraction 'in density' on Z_+: evolves the uniform mass
    on [1, N] under T's exact pushforward (full orbits, no truncation)
    and measures m(t) = fraction not yet absorbed into the cycle {1, 2}
    after t steps.

    Returns the profile {t: m(t)} and the effective per-step rate in the
    exponential regime (between the 90% and 99.9% quantiles), with the
    large-deviations reference 2^{-(1-H(1/log2 3))} ≈ 0.9661 per step
    (`padic`). This rate is what remains of the 'spectral gap' on the
    Z_+ face of the problem: contraction of MASS, not of individual
    points — exactly the strength of a density theorem (Terras, Tao)
    and nothing more."""
    times = [total_stopping_time(n) for n in range(2, N + 1)]
    assert all(s >= 0 for s in times)
    tmax = max(times)
    counts = [0] * (tmax + 1)
    for s in times:
        counts[s] += 1
    total = len(times)
    m: List[float] = []
    rem = total
    for t in range(tmax + 1):
        rem -= counts[t]
        m.append(rem / total)
    profile = {t: m[t] for t in range(0, tmax + 1, stride)}
    t1 = next(t for t, v in enumerate(m) if v <= 0.10)
    t2 = next((t for t, v in enumerate(m) if v <= 0.001), tmax)
    rate = (m[t2] / m[t1]) ** (1.0 / (t2 - t1)) if t2 > t1 and m[t2] > 0 else None
    theta = 1 / math.log2(3)
    H = -theta * math.log2(theta) - (1 - theta) * math.log2(1 - theta)
    return {"tmax": tmax, "profile": profile, "rate": rate,
            "t_10pct": t1, "t_01pct": t2,
            "reference_rate": 2 ** (-(1 - H))}

"""
Syracuse transfer operator modulo 3^k.

Model (the same used by Tao, 2019, "Almost all orbits..."): for a
"typical" odd n, the Syracuse map S(n) = (3n+1)/2^a has a ~ Geometric(1/2)
(an exact consequence of the Terras bijection). Projecting onto Z/3^k
gives a Markov chain on residues r with 3 ∤ r:

    r  ->  (3r + 1) · inv(2^a)  (mod 3^k),   P(a) = 2^{-a}.

Since 2 is a primitive root mod 3^k, inv(2^a) is periodic in a with
period ord = φ(3^k) = 2·3^{k-1}; summing the geometric series, the
transition matrix is EXACT in rational arithmetic:

    P[r][r'] = (sum over a<=ord with transition r->r' of 2^{-a}) / (1 - 2^{-ord}).

Algorithms:
* syracuse_transfer_matrix(k) — exact matrix (Fraction).
* stationary_uniform_check(k) — tests whether the uniform distribution
  is stationary. FINDING: it is not! Mod 3 the invariant measure is
  (1/3, 2/3) — the bias (3n+1)/2^a ≡ (-1)^a (mod 3), P(a odd) = 2/3,
  propagates to every 3^k. An explicit and exact measure invariant of
  the projected dynamics.
* stationary_exact(k) — the exact (rational) invariant measure, via
  Gaussian elimination.
* spectral_gap(k) — modulus of the second eigenvalue via power iteration
  on the spectral complement of the stationary distribution; a large
  spectral gap = fast mixing = orbits forget the initial residue
  exponentially fast. Structure to pursue: a gap uniform in k would give
  quantitative equidistribution (in the invariant measure) — the kind of
  ingredient that feeds "for almost every n" results (Tao 2019).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Tuple


def _states(k: int) -> List[int]:
    return [r for r in range(3**k) if r % 3 != 0]


def syracuse_transfer_matrix(
    k: int,
) -> Tuple[List[int], Dict[int, Dict[int, Fraction]]]:
    """Exact transition matrix of the Syracuse chain on {r mod 3^k, 3∤r}.

    Returns (states, P) with P[r][r'] an exact rational."""
    M = 3**k
    states = _states(k)
    ord_ = 2 * 3 ** (k - 1)  # order of 2 mod 3^k (2 is a primitive root)
    assert pow(2, ord_, M) == 1
    inv2 = pow(2, -1, M)
    norm = Fraction(1) - Fraction(1, 2**ord_)
    P: Dict[int, Dict[int, Fraction]] = {r: {} for r in states}
    for r in states:
        target = (3 * r + 1) % M
        t = target
        for a in range(1, ord_ + 1):
            t = (t * inv2) % M  # t = (3r+1)·inv(2^a)
            if t % 3 != 0:  # always true: (3r+1)/2^a ≢ 0 mod 3
                w = Fraction(1, 2**a) / norm
                P[r][t] = P[r].get(t, Fraction(0)) + w
    return states, P


def stationary_uniform_check(k: int) -> bool:
    """Checks EXACTLY whether the uniform distribution over the states is
    stationary (doubly stochastic matrix).

    FINDING (discovered by this code): it is NOT — e.g. mod 3 the exact
    invariant measure is pi(1) = 1/3, pi(2) = 2/3: the Syracuse iterates
    visit 2 (mod 3) twice as often as 1 (mod 3), because
    (3n+1)/2^a ≡ 2^{-a} ≡ (-1)^a (mod 3) and a is odd with probability
    2/3. The correct invariant measure is computed by stationary_exact."""
    states, P = syracuse_transfer_matrix(k)
    col: Dict[int, Fraction] = {r: Fraction(0) for r in states}
    for r in states:
        row_sum = sum(P[r].values())
        if row_sum != 1:
            return False
        for s, w in P[r].items():
            col[s] += w
    return all(c == 1 for c in col.values())


def stationary_exact(k: int) -> Dict[int, Fraction]:
    """EXACT (rational) invariant measure of the Syracuse chain mod 3^k:
    solves pi·P = pi, sum(pi) = 1 via Gaussian elimination over Fraction.

    This is a genuine structural invariant of the projected dynamics: the
    unique probability measure preserved by the transfer operator."""
    states, P = syracuse_transfer_matrix(k)
    n = len(states)
    idx = {r: i for i, r in enumerate(states)}
    # system (P^T - I) pi = 0, with the last row replaced by sum = 1
    A: List[List[Fraction]] = [[Fraction(0)] * (n + 1) for _ in range(n)]
    for r in states:
        for s, w in P[r].items():
            A[idx[s]][idx[r]] += w
    for i in range(n):
        A[i][i] -= 1
    A[n - 1] = [Fraction(1)] * n + [Fraction(1)]
    # Gaussian elimination with partial pivoting
    for col_i in range(n):
        piv = next(row for row in range(col_i, n) if A[row][col_i] != 0)
        A[col_i], A[piv] = A[piv], A[col_i]
        inv = 1 / A[col_i][col_i]
        A[col_i] = [v * inv for v in A[col_i]]
        for row in range(n):
            if row != col_i and A[row][col_i] != 0:
                f = A[row][col_i]
                A[row] = [a - f * b for a, b in zip(A[row], A[col_i])]
    return {r: A[idx[r]][n] for r in states}


def stationary_distribution(
    k: int, iters: int = 2000, tol: float = 1e-13
) -> Dict[int, float]:
    """Stationary distribution via power iteration (float)."""
    states, P = syracuse_transfer_matrix(k)
    Pf = {r: {s: float(w) for s, w in row.items()} for r, row in P.items()}
    pi = {r: 1.0 / len(states) for r in states}
    for _ in range(iters):
        new = {r: 0.0 for r in states}
        for r in states:
            pr = pi[r]
            for s, w in Pf[r].items():
                new[s] += pr * w
        delta = max(abs(new[r] - pi[r]) for r in states)
        pi = new
        if delta < tol:
            break
    return pi


def memory_loss_check(k: int) -> bool:
    """Checks EXACTLY the rank collapse of the transfer operator: states
    r ≡ r' (mod 3^{k-1}) have IDENTICAL rows, because the row depends
    only on 3r+1 (mod 3^k), which depends only on r (mod 3^{k-1}).

    Consequence (by induction): P^k has rank 1 — the chain reaches the
    invariant measure in EXACTLY k steps and the spectrum beyond
    lambda_1 = 1 is {0}. STRUCTURAL FINDING: the mod 3^k projection
    retains no long-term memory; no obstruction to convergence can live
    in finite 3-adic arithmetic — only the 2-adic/global structure
    remains."""
    M = 3**k
    states, P = syracuse_transfer_matrix(k)
    if k == 1:
        pairs = [(1, 2)]
    else:
        step = 3 ** (k - 1)
        pairs = [(r, r + step) for r in states if r + step < M and (r + step) % 3 != 0]
    return all(P[a] == P[b] for a, b in pairs)


def spectral_gap(k: int, iters: int = 400) -> float:
    """Estimate of |lambda_2| of the chain mod 3^k via power iteration on
    the right action f -> P f, removing the spectral component of
    eigenvalue 1 (constant right eigenvector, left eigenvector pi):
    f -> f - (pi·f)·1. Spectral gap = 1 - |lambda_2|."""
    states, P = syracuse_transfer_matrix(k)
    Pf = {r: {s: float(w) for s, w in row.items()} for r, row in P.items()}
    pi = {r: float(v) for r, v in stationary_exact(k).items()}
    import math

    def project(v):
        c = sum(pi[r] * v[r] for r in states)
        return {r: v[r] - c for r in states}

    f = project({r: math.sin(1.0 + 2.7 * i) for i, r in enumerate(states)})
    norm = math.sqrt(sum(v * v for v in f.values()))
    f = {r: v / norm for r, v in f.items()}
    lam = 0.0
    for _ in range(iters):
        g = project({r: sum(w * f[s] for s, w in Pf[r].items()) for r in states})
        norm = math.sqrt(sum(v * v for v in g.values()))
        if norm == 0.0:
            return 0.0
        lam = norm  # ||P f|| with ||f|| = 1
        f = {r: v / norm for r, v in g.items()}
    return lam

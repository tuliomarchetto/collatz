"""
2-adic structure: the fundamental symmetry of the accelerated map.

Terras's theorem (1976) / Lagarias (1985). The map

    Q_k : Z/2^k -> {0,1}^k,   n |-> length-k parity vector

is a BIJECTION, and the accelerated map T is conjugate to the Bernoulli
shift: the parity vector of T(n) is the shift of the parity vector of n.
In other words, extended to the 2-adic integers Z_2, T is measurably
isomorphic to the shift (sigma-algebra and Haar measure), and the parity
of the iterates of a "random" n is an i.i.d. sequence of fair coin
flips. This is the strongest known structural symmetry of the system —
and the reason probabilistic heuristics predict convergence (mean drift
log(3)/2 - log 2 < 0 per step).

Algorithms:

* terras_bijection_check(k)  — exactly verifies the bijectivity of Q_k.
* shift_conjugacy_check(k)   — verifies Q_{k-1}(T(n)) = shift(Q_k(n)).
* parity_census(k)           — EXACT distribution of the number of odd
                               steps among the first k steps, over
                               n mod 2^k: should be Binomial(k, 1/2).
                               From this follows the exact measure of the
                               "bad set" (classes that still grow after k
                               steps) and its decay rate — compared with
                               the large-deviations rate
                               1 - H(1/log2(3)) (H = binary entropy).
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from .core import parity_vector


def terras_bijection_check(k: int) -> bool:
    """True iff n |-> parity_vector(n, k) is bijective on Z/2^k."""
    seen = set()
    for n in range(1 << k):
        seen.add(parity_vector(n, k))
    return len(seen) == (1 << k)


def shift_conjugacy_check(k: int) -> bool:
    """Verifies the conjugacy with the shift: for every n mod 2^k, the
    parity vector of T(n) (length k-1) is the shift of the vector of n."""
    from .core import T
    for n in range(1 << k):
        pv = parity_vector(n, k)
        pv_shift = parity_vector(T(n), k - 1)
        if pv[1:] != pv_shift:
            return False
    return True


def parity_census(k: int) -> Dict[int, int]:
    """Counts, for n ranging over Z/2^k, how many have exactly j odd
    steps in the first k steps of T. Expected result (implied by the
    Terras bijection): the binomial coefficient C(k, j)."""
    census: Dict[int, int] = {}
    for n in range(1 << k):
        j = sum(parity_vector(n, k))
        census[j] = census.get(j, 0) + 1
    return census


def census_is_binomial(census: Dict[int, int], k: int) -> bool:
    return all(census.get(j, 0) == math.comb(k, j) for j in range(k + 1))


def bad_set_measure(k: int) -> Tuple[float, float]:
    """Measure (fraction of residues mod 2^k) of the 'bad' set: classes
    whose growth factor after k steps is >= 1, i.e. 3^j >= 2^k, i.e.
    j > k/log2(3).

    Returns (exact_measure, theoretical_rate) where the theoretical
    large-deviations decay rate is 2^{-k(1-H(theta))}, theta = 1/log2 3
    ~ 0.6309. The conjecture 'almost every n has finite stopping time'
    (Terras) is exactly the statement that this measure -> 0; the rate
    quantifies it.
    """
    alpha = math.log2(3)
    theta = 1 / alpha
    census = parity_census(k)
    bad = sum(c for j, c in census.items() if j * alpha >= k)
    measure = bad / (1 << k)

    def H(p: float) -> float:
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    rate = 2 ** (-k * (1 - H(theta)))
    return measure, rate

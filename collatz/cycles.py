"""
Exact cycle theory: enumeration via parity vectors and exclusion via
continued fractions.

CENTRAL STRUCTURAL FACT. For the accelerated map T of the system 3n+d,
after L steps with parity vector p = (p_0,...,p_{L-1}) containing k ones:

    T^L(n) = (3^k · n + b(p)) / 2^L,

where b(p) is the integer given by the recurrence
    b_0 = 0;  b_{i+1} = 3·b_i + d·2^i  if p_i = 1,  else  b_{i+1} = b_i.

A cycle of length L is exactly a fixed point T^L(n) = n, i.e.

    n = b(p) / (2^L - 3^k).                                   (*)

This reduces the search for cycles to an exact ARITHMETIC problem:

* find_cycles          — enumerates all cycles of length <= L_max of the
                         system 3n+d in Z (positive and negative), testing
                         the integrality of (*) for each parity vector.
                         Finds the famous negative cycles (-1, -5, -17)
                         and the nontrivial cycles of 3n-1 and 3n+5.
* cycle_exclusion_bound — given that every n <= N converges (verified),
                         derives a RIGOROUS LOWER BOUND on the number of
                         odd steps k of any nontrivial cycle, using the
                         continued-fraction convergents of alpha = log2(3).

The exclusion uses the multiplicative identity around the cycle:
    2^L = prod_{odd steps} (3 + d/x_i)                    (**)
with all x_i > N, which forces
    0 < L - k·alpha <= k·eps,   eps = log2(1 + 1/(3N)),
i.e. L/k approximates alpha from ABOVE with error ~ 1/(3N·ln2). By the
theory of best rational approximations, for q_i <= k < q_{i+1}
(denominators of the convergents of alpha) we have
||k·alpha|| >= ||q_i·alpha|| > 1/(q_i + q_{i+1}); hence a cycle requires
k > 1/(eps·(q_i + q_{i+1})). We sweep the intervals between consecutive
denominators and return the largest K such that EVERY k <= K is
impossible. (Method along the lines of Eliahou 1993 / Simons-de Weger.)
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Dict, List, Optional, Set, Tuple

from .core import T

# ----------------------------------------------------------------------
# Exact enumeration of cycles
# ----------------------------------------------------------------------


def _fixed_point(parity: Tuple[int, ...], d: int) -> Optional[int]:
    """Solve (*) for the given parity vector; return integer n or None."""
    L = len(parity)
    k = sum(parity)
    b = 0
    pw = 1  # 2^i
    for p in parity:
        if p:
            b = 3 * b + d * pw
        pw <<= 1
    den = (1 << L) - 3**k
    if den == 0 or b % den != 0:
        return None
    return b // den


def _realizes(n: int, parity: Tuple[int, ...], d: int) -> bool:
    """Check that the actual orbit of n has exactly this parity vector
    and returns to n (a genuine cycle, not just an algebraic solution)."""
    x = n
    for p in parity:
        if (x & 1) != p:
            return False
        x = T(x, d)
    return x == n


def find_cycles(
    d: int = 1, max_len: int = 20, include_negative: bool = True
) -> List[Tuple[int, ...]]:
    """Enumerates ALL cycles of the accelerated map T (system 3n+d) with
    length <= max_len, over the integers (positive and, optionally,
    negative and zero).

    Correctness: every cycle contains at least one odd step (except the
    fixed point 0), so it can be rotated to start at p_0 = 1; we enumerate
    only vectors with p_0 = 1 and deduplicate by the set of elements.

    For d=1 the expected result (and conjectured to be complete over the
    positives) is just the trivial cycle {1,2}; among the negatives the
    cycles of -1, -5, and -17 appear — proof that the detector works.
    """
    seen: Set[frozenset] = set()
    cycles: List[Tuple[int, ...]] = []
    for L in range(1, max_len + 1):
        for mask in range(1 << (L - 1)):
            parity = (1,) + tuple((mask >> i) & 1 for i in range(L - 1))
            n = _fixed_point(parity, d)
            if n is None or n == 0:
                continue
            if n < 0 and not include_negative:
                continue
            if not _realizes(n, parity, d):
                continue
            orb = [n]
            x = T(n, d)
            while x != n:
                orb.append(x)
                x = T(x, d)
            key = frozenset(orb)
            if key not in seen:
                seen.add(key)
                m = min(orb, key=abs)
                i = orb.index(m)
                cycles.append(tuple(orb[i:] + orb[:i]))
    cycles.sort(key=lambda c: (len(c), min(c)))
    return cycles


# ----------------------------------------------------------------------
# Continued fractions of log2(3) and cycle exclusion
# ----------------------------------------------------------------------


def log2_3_convergents(
    max_den: int = 10**30, exact_certificate_upto: int = 10**5
) -> List[Tuple[int, int]]:
    """Convergents p/q of alpha = log2(3), with denominator <= max_den.

    The partial quotients are extracted from a 120-digit decimal
    approximation. Certification:
    * for q <= exact_certificate_upto, each convergent is verified
      EXACTLY by comparing the integers 2^p and 3^q (above/below
      alternation of alpha) — pure integer arithmetic;
    * for larger q, the expansion remains correct as long as q^2 stays
      much smaller than 10^prec (the decimal approximation error,
      ~10^-120, is smaller than 1/(2·q_i·q_{i+1}), the classical
      condition for the CF of an approximation to match that of the
      number); the loop stops before that limit."""
    getcontext().prec = 120
    alpha = Decimal(3).ln() / Decimal(2).ln()
    x = alpha
    p0, q0, p1, q1 = 1, 0, 0, 1  # previous convergents
    out: List[Tuple[int, int]] = []
    for _ in range(200):
        a = int(x)
        p0, q0, p1, q1 = a * p0 + p1, a * q0 + q1, p0, q0
        if q0 > max_den or q0 * q0 > 10**100:
            break
        expected_above = len(out) % 2 == 1  # 1/1 below, 2/1 above, 3/2 below...
        if q0 <= exact_certificate_upto:
            # exact certificate: p0/q0 > alpha  <=>  2^p0 > 3^q0
            above = (1 << p0) > 3**q0
            if above != expected_above:
                raise ArithmeticError(
                    "inconsistent continued-fraction expansion (exact certificate)"
                )
        else:
            above = Fraction(p0, q0) > Fraction(str(alpha))
            if above != expected_above:
                raise ArithmeticError(
                    "insufficient decimal precision for the convergents"
                )
        out.append((p0, q0))
        frac = x - a
        if frac == 0:
            break
        x = 1 / frac
    return out


def cycle_exclusion_bound(verified_limit: int) -> Dict[str, int]:
    """Rigorous lower bound for nontrivial cycles of 3n+1.

    Hypothesis: every 2 <= n <= verified_limit converges (e.g. the result
    of verify_range, or the published computational limit 2^71, Barina 2025).

    Returns {'min_odd_steps': K, 'min_length': L, 'min_elements': ...}:
    any nontrivial cycle over the positives has MORE than K odd steps and
    length (in T steps) greater than L.

    Derivation (see the module docstring): a cycle with k odd steps and
    all elements > N satisfies 0 < L - k·alpha <= k·eps with
    eps = log2(1 + 1/(3N)); for q_i <= k < q_{i+1} we have
    dist(k·alpha, Z) > 1/(q_i + q_{i+1}); hence k > 1/(eps·(q_i+q_{i+1})).
    """
    N = verified_limit
    getcontext().prec = 120
    ln2 = Decimal(2).ln()
    eps_dec = (1 + Decimal(1) / (3 * N)).ln() / ln2
    # eps as a safe upper-bound fraction
    eps = Fraction(int(eps_dec * 10**60) + 1, 10**60)

    convs = log2_3_convergents()
    K = 0  # every k <= K is excluded
    for i in range(len(convs) - 1):
        _, qi = convs[i]
        _, qi1 = convs[i + 1]
        # within [qi, qi1): excludes k <= 1/(eps*(qi+qi1))
        cap = int(Fraction(1, 1) / (eps * (qi + qi1)))
        if cap >= qi1 - 1:
            K = max(K, qi1 - 1)  # whole interval excluded; continue
        else:
            K = max(K, min(cap, qi1 - 1))
            break
    # length L > k*alpha > K*1.58; cycle elements = L (all distinct)
    min_len = int(K * Fraction(158, 100))
    return {
        "verified_limit": N,
        "min_odd_steps": K,
        "min_length_T_steps": min_len,
        "min_elements": min_len,
    }

"""
Core: Collatz maps and trajectory tools.

Three forms of the map are used in the literature and here:

* Original map       C(n) = n/2 if n even;  3n+d if n odd.
* Accelerated map    T(n) = n/2 if n even;  (3n+d)/2 if n odd.
  (each step divides by 2 exactly once; this is the canonical form for
  2-adic analysis and for cycle theory)
* Syracuse map       S(n) = (3n+d) / 2^v2(3n+d), defined from odd to
  odd (used in the mod 3^k transfer operator).

The parameter d (odd, default +1) allows studying the sibling systems 3n-1
and 3n+5, which DO have nontrivial cycles — serving as a validation bench
for the counterexample-search algorithms.
"""

from __future__ import annotations

from typing import Iterator, List, Tuple


def v2(n: int) -> int:
    """2-adic valuation: largest a with 2^a | n (n != 0)."""
    if n == 0:
        raise ValueError("v2(0) is infinite")
    return (n & -n).bit_length() - 1


def collatz_step(n: int, d: int = 1) -> int:
    """Original map C(n) for the system 3n+d."""
    return n // 2 if n % 2 == 0 else 3 * n + d


def T(n: int, d: int = 1) -> int:
    """Accelerated map T(n) for the system 3n+d."""
    return n // 2 if n % 2 == 0 else (3 * n + d) // 2


def syracuse(n: int, d: int = 1) -> int:
    """Syracuse map (odd -> odd): removes ALL powers of 2."""
    if n % 2 == 0:
        raise ValueError("syracuse is only defined for odd numbers")
    m = 3 * n + d
    return m >> v2(m)


def trajectory(n: int, d: int = 1, max_steps: int = 10_000,
               accelerated: bool = True) -> List[int]:
    """Trajectory of n under T (or C), until reaching 1, a locally
    repeated value (short cycle), or max_steps."""
    step = T if accelerated else collatz_step
    out = [n]
    x = n
    for _ in range(max_steps):
        if x == 1 and d == 1:
            break
        x = step(x, d)
        out.append(x)
        if x == n:  # cycle closed
            break
    return out


def orbit(n: int, d: int = 1, accelerated: bool = True) -> Iterator[int]:
    """Infinite iterator over the orbit of n."""
    step = T if accelerated else collatz_step
    x = n
    while True:
        yield x
        x = step(x, d)


def parity_vector(n: int, k: int, d: int = 1) -> Tuple[int, ...]:
    """Parity vector (p_0,...,p_{k-1}) with p_i = parity of T^i(n).

    Terras's theorem (1976): for the accelerated map, n mod 2^k determines
    and is determined by the length-k parity vector — a bijection
    Z/2^k <-> {0,1}^k. Verified computationally in `padic`.
    """
    ps = []
    x = n
    for _ in range(k):
        p = x & 1
        ps.append(p)
        x = (3 * x + d) // 2 if p else x // 2
    return tuple(ps)


def stopping_time(n: int, d: int = 1, max_steps: int = 10_000) -> int:
    """Smallest i >= 1 with T^i(n) < n (the "stopping time"); -1 if it does
    not occur within max_steps. The conjecture is equivalent to: every
    n >= 2 has a finite stopping time."""
    x = n
    for i in range(1, max_steps + 1):
        x = T(x, d)
        if x < n:
            return i
    return -1


def total_stopping_time(n: int, d: int = 1, max_steps: int = 10_000_000) -> int:
    """Number of T steps until reaching 1; -1 if not reached within max_steps."""
    x = n
    for i in range(max_steps):
        if x == 1:
            return i
        x = T(x, d)
    return -1


def max_excursion(n: int, d: int = 1, max_steps: int = 10_000_000) -> int:
    """Largest value reached by the orbit of n before reaching 1."""
    x = n
    hi = n
    for _ in range(max_steps):
        if x == 1:
            return hi
        x = T(x, d)
        if x > hi:
            hi = x
    return hi

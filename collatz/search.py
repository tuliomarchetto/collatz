"""
Direct search for counterexamples.

A counterexample to the Collatz Conjecture would be:
  (a) a nontrivial cycle over the positive integers, or
  (b) a divergent orbit.

Algorithms in this module:

* verify_range(N)      — ascending sieve: computationally proves that
                         every n <= N converges to 1 (or returns the
                         counterexample). While verifying, it collects
                         RECORDS of stopping time and maximum excursion —
                         the extremal statistics are themselves a
                         structural property (growth ~ c·log n and ~ n^2
                         respectively).
* brent_cycle_detect   — cycle detection on an orbit (Brent's algorithm,
                         O(1) memory): finds the cycle if the orbit is
                         eventually periodic.
* divergence_probe     — probes candidates for a divergent orbit.

Validation: applied to the sibling system 3n-1 (d=-1), these algorithms
FIND the nontrivial cycles {5,7,10} and {17,25,37,...} — evidence that,
if an analogous counterexample existed for 3n+1, it would be detected.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple

from .core import T


@dataclass
class VerifyResult:
    limit: int
    d: int
    all_converge: bool
    counterexample: Optional[int] = None       # seed that does not converge
    cycle: Optional[Tuple[int, ...]] = None    # nontrivial cycle found
    stopping_records: List[Tuple[int, int]] = field(default_factory=list)
    excursion_records: List[Tuple[int, int]] = field(default_factory=list)


def verify_range(limit: int, d: int = 1, max_steps: int = 100_000) -> VerifyResult:
    """Verifies convergence of every 2 <= n <= limit under T (system 3n+d).

    Classic ascending sieve strategy: when processing n in increasing
    order, it suffices to iterate until the orbit drops below n (everything
    below is already verified). Even numbers drop immediately (n/2 < n),
    so only odd numbers are iterated.

    If an orbit returns to its own seed, a CYCLE has been found and is
    returned. If it exceeds max_steps without dropping, it is returned as
    a candidate counterexample (divergence or a very long cycle).
    """
    res = VerifyResult(limit=limit, d=d, all_converge=True)
    best_stop = 0
    best_exc = 0
    for n in range(3, limit + 1, 2):
        x = n
        steps = 0
        peak = n
        while x >= n:
            x = T(x, d)
            steps += 1
            if x > peak:
                peak = x
            if x == n:  # orbit closed: cycle with minimal element n
                cyc = [n]
                y = T(n, d)
                while y != n:
                    cyc.append(y)
                    y = T(y, d)
                res.all_converge = False
                res.counterexample = n
                res.cycle = tuple(cyc)
                return res
            if steps > max_steps:
                res.all_converge = False
                res.counterexample = n
                return res
        if steps > best_stop:
            best_stop = steps
            res.stopping_records.append((n, steps))
        if peak > best_exc:
            best_exc = peak
            res.excursion_records.append((n, peak))
    return res


def brent_cycle_detect(n: int, d: int = 1,
                       max_power: int = 60) -> Optional[Tuple[int, int, int]]:
    """Brent's algorithm for cycle detection on the orbit of n under T.

    Returns (mu, lam, cycle_min_element) — entry index into the cycle,
    cycle length, and its smallest element — or None if no cycle closes
    within 2^max_power steps (orbit possibly divergent).
    """
    f: Callable[[int], int] = lambda x: T(x, d)
    power = lam = 1
    tortoise = n
    hare = f(n)
    while tortoise != hare:
        if power > (1 << max_power):
            return None
        if lam == power:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1
    # length lam known; find mu
    tortoise = hare = n
    for _ in range(lam):
        hare = f(hare)
    mu = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
    # smallest element of the cycle
    x = tortoise
    lo = x
    for _ in range(lam):
        x = f(x)
        if x < lo:
            lo = x
    return mu, lam, lo


def divergence_probe(n: int, d: int = 1, ceiling_bits: int = 4096,
                     max_steps: int = 1_000_000) -> dict:
    """Divergence probe: follows the orbit of n and reports whether it
    exceeds 2^ceiling_bits (STRONG candidate for divergence) or whether it
    converges / enters a cycle. No algorithm can PROVE divergence by
    finite simulation; this classifies candidates for later analysis."""
    x = n
    peak = n
    for i in range(max_steps):
        if x == 1:
            return {"n": n, "verdict": "converge", "steps": i, "peak": peak}
        if x.bit_length() > ceiling_bits:
            return {"n": n, "verdict": "explode", "steps": i, "peak_bits": x.bit_length()}
        x = T(x, d)
        if x > peak:
            peak = x
        if x == n:
            return {"n": n, "verdict": "ciclo", "steps": i + 1, "peak": peak}
    return {"n": n, "verdict": "indeterminado", "steps": max_steps, "peak": peak}

"""
Symmetry search: conjugacies between 3n+d systems and automorphisms of
the modular transition graphs.

1. EXACT AFFINE CONJUGACIES — affine_conjugacy_search(d, d'):
   searches for maps φ(x) = a·x + b (a, b integers) with

       φ(T_d(x)) = T_{d'}(φ(x))   for all x,

   i.e. φ carries the dynamics of the system 3n+d to that of 3n+d'.
   Structural findings the algorithm rediscovers on its own:
     * φ(x) = -x  conjugates 3n+1 with 3n-1: the problem "3n-1 over the
       positives" (which DOES have nontrivial cycles) is exactly "3n+1
       over the negatives". Every reflection symmetry of the problem is
       there.
     * φ(x) = d·x conjugates 3n+1 with the restriction of 3n+d to the
       multiples of d (self-similarity of the family).
   Methodological consequence: counterexamples of the sibling systems
   are images of symmetries — the search for a 3n+1 counterexample
   should look for structures that BREAK these symmetries, not repeat
   them.

2. AFFINE AUTOMORPHISMS OF THE MODULAR GRAPH — modular_affine_automorphisms(m):
   affine permutations x -> ax+b of Z/m that preserve T's transition
   relation. A trivial group means the projected dynamics is "rigid"
   modulo m.

The conjugacy test is exact: T is affine per parity with period 2 in n,
and φ is affine; the identity holds for all x iff it holds on an
interval of length > 2·|a|·2 (verified with margin)."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from .core import T


def _is_conjugacy(a: int, b: int, d1: int, d2: int, test_range: int = 200) -> bool:
    """Verifies φ(T_{d1}(x)) == T_{d2}(φ(x)) for x in [-R, R]. Since both
    sides are affine functions per class of x mod 2 (and φ affects parity
    with period 2), equality on 4·|a|+8 consecutive points per class
    implies global equality; test_range=200 gives margin for |a| <= 20."""
    for x in range(-test_range, test_range + 1):
        lhs = a * T(x, d1) + b
        rhs = T(a * x + b, d2)
        if lhs != rhs:
            return False
    return True


def affine_conjugacy_search(d1: int, d2: int, max_a: int = 20,
                            max_b: int = 40) -> List[Tuple[int, int]]:
    """All affine conjugacies φ(x)=ax+b (0<|a|<=max_a, |b|<=max_b) from
    the system 3n+d1 to 3n+d2."""
    found = []
    for a in [i for i in range(-max_a, max_a + 1) if i != 0]:
        for b in range(-max_b, max_b + 1):
            if _is_conjugacy(a, b, d1, d2):
                found.append((a, b))
    return found


def semiconjugacy_multiples(d: int) -> bool:
    """Verifies the self-similarity x -> d·x: T_d(d·x) == d·T_1(x)?"""
    return all(T(d * x, d) == d * T(x, 1) for x in range(-100, 101))


def _edges_mod(m: int, d: int = 1) -> Set[Tuple[int, int]]:
    edges = set()
    for n in range(2 * m):
        edges.add((n % m, T(n, d) % m))
    return edges


def modular_affine_automorphisms(m: int, d: int = 1) -> List[Tuple[int, int]]:
    """Affine automorphisms x -> ax+b of Z/m that preserve the edge set
    of T's transition graph mod m. Returns the list of (a, b);
    (1, 0) — the identity — is always present."""
    edges = _edges_mod(m, d)
    from math import gcd
    autos = []
    for a in range(1, m):
        if gcd(a, m) != 1:
            continue
        for b in range(m):
            ok = all(((a * u + b) % m, (a * v + b) % m) in edges for (u, v) in edges)
            if ok:
                autos.append((a, b))
    return autos

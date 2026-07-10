"""
Inverse tree (preimage graph of 1).

The conjecture is equivalent to: the inverse tree of the accelerated map
T, rooted at 1 (excluding the loop 1->2->1), covers ALL positive
integers. Preimages of m under T:

    2m               (always — undoes an even step),
    (2m - 1)/3       (when it is an integer and odd — undoes an odd step).

A counterexample would be exactly an integer outside the tree.

Algorithms:
* inverse_tree(depth)      — exact BFS up to the given depth.
* coverage_density(X, ..)  — fraction of n <= X reached; should tend to 1
                             (Krasikov-Lagarias prove density >= X^0.84
                             for the reached set).
* growth_rate(depth)       — number of nodes per level; the asymptotic
                             factor predicted by the branching heuristic
                             is (1 + 1/3)·... ~ 4/3 per level for nodes
                             that admit the odd branch (2m-1 ≡ 0 mod 3
                             occurs for 1/3 of the m; the algorithm
                             measures the actual factor).
* missing_below(X, depth)  — the smallest integers STILL not reached at
                             the given depth (structural candidates
                             worth studying; all disappear when going
                             deeper iff the conjecture holds).
"""

from __future__ import annotations

from typing import List, Set, Tuple


def inverse_children(m: int) -> List[int]:
    """Preimages of m under T over the positive integers."""
    kids = [2 * m]
    q, r = divmod(2 * m - 1, 3)
    if r == 0 and q % 2 == 1 and q > 0:
        kids.append(q)
    return kids


def inverse_tree(depth: int, cap: int | None = None) -> Tuple[Set[int], List[int]]:
    """BFS of the inverse tree starting from 1. Returns (reached nodes,
    number of new nodes per level).

    `cap`: nodes larger than the cap are recorded but NOT expanded —
    pruning that keeps the cost O(cap) and allows large depths. The
    reported coverage is then a LOWER BOUND on the true coverage."""
    reached: Set[int] = {1, 2}
    frontier = [2]
    levels = [1]
    for _ in range(depth):
        nxt: List[int] = []
        for m in frontier:
            for c in inverse_children(m):
                if c not in reached:
                    reached.add(c)
                    if cap is None or c <= cap:
                        nxt.append(c)
        levels.append(len(nxt))
        frontier = nxt
        if not frontier:
            break
    return reached, levels


def coverage_density(X: int, depth: int, cap: int | None = None) -> float:
    """Fraction of the integers 1..X reached by the inverse tree up to
    the given depth. Convergence to 1 as depth grows <=> conjecture
    (restricted to n <= X). Default cap: 1000·X (the maximum excursion
    of small orbits far exceeds X — e.g. 703 rises to 125252 under T)."""
    if cap is None:
        cap = max(1_000_000, 1000 * X)
    reached, _ = inverse_tree(depth, cap=cap)
    hit = sum(1 for n in range(1, X + 1) if n in reached)
    return hit / X


def growth_rate(depth: int) -> List[float]:
    """Level-by-level growth factor of the number of new nodes (no
    pruning). The branching heuristic predicts a factor ~ 4/3 per level."""
    _, levels = inverse_tree(depth)
    return [levels[i + 1] / levels[i] for i in range(1, len(levels) - 1) if levels[i]]


def missing_below(X: int, depth: int, cap: int | None = None) -> List[int]:
    """Smallest integers <= X still outside the tree at the given depth."""
    if cap is None:
        cap = max(1_000_000, 1000 * X)
    reached, _ = inverse_tree(depth, cap=cap)
    return [n for n in range(1, X + 1) if n not in reached][:20]


def required_depth(X: int) -> int:
    """EXACT minimum depth of the inverse tree needed to cover all
    integers from 1 to X. Equivalent to the maximum total stopping time
    (under the accelerated map T) among all n in 1..X.

    The conjecture is equivalent to: required_depth(X) is finite for
    every X."""
    from .core import total_stopping_time

    return max(total_stopping_time(n) for n in range(1, X + 1))


def empirical_bounds(depth: int) -> List[Tuple[int, int]]:
    """For each level 0..depth of the inverse tree, returns (min_node,
    max_node) among the NEW nodes at that level.

    Level 0 contains {1, 2} (root + trivial cycle). The max at each level
    is exactly 2^k (the even branch doubles the previous max); the min
    gradually decreases as the odd branch (2m-1)/3 produces smaller
    nodes — the backward diffusion of the inverse tree capturing small
    integers."""
    reached: Set[int] = {1, 2}
    frontier = [2]
    bounds: List[Tuple[int, int]] = [(1, 2)]
    for _ in range(depth):
        nxt: List[int] = []
        for m in frontier:
            for c in inverse_children(m):
                if c not in reached:
                    reached.add(c)
                    nxt.append(c)
        if nxt:
            bounds.append((min(nxt), max(nxt)))
        else:
            bounds.append((0, 0))
            break
        frontier = nxt
    return bounds

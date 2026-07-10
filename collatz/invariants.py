"""
Automatic search for invariants.

Three families of algorithms:

1. EXACT MODULAR INVARIANTS — induced_map_search(M):
   searches for pairs (m1, m2) such that T(n) mod m2 is a FUNCTION of
   n mod m1. Structural finding: T(n) mod m is determined by n mod 2m
   (and nothing less, for m a power of 2) — the tower Z/2^{k+1} -> Z/2^k
   whose inverse limit is Z_2, confirming that the only factorable
   "coordinate" of the dynamics is the 2-adic one.

2. CONSERVED PARTITIONS — conserved_partition(m):
   computes the coarsest stable partition of Z/m under the transition
   relation (bisimulation / partition refinement, as in DFA
   minimization). Any function that is constant on the blocks is a
   "discrete quantity conserved by the projected dynamics". Also detects
   TRANSIENT classes (which the dynamics abandons and never re-enters) —
   e.g. multiples of 3: T never produces a multiple of 3 from an odd
   step, so the long-term dynamics lives on n coprime to 3.

3. LYAPUNOV FUNCTION / MAXIMUM MEAN CYCLE — karp_max_mean_cycle(j):
   If there existed f(n) = log n + w(n mod 2^j) strictly decreasing
   along every orbit, the conjecture (the divergence part) would be
   proved. Such a w exists iff the MAXIMUM MEAN CYCLE of the transition
   graph on Z/2^j (weights = log2 of the step's multiplicative factor)
   is negative. Karp's algorithm computes that value exactly.
   STRUCTURAL FINDING: the maximum is log2(3) - 1 > 0, attained at the
   loop on residue -1 mod 2^j — and every cycle with positive mean
   corresponds to 2-adic periodic points that are the cycles of
   NEGATIVE INTEGERS (-1, -5, -17). In other words: the obstruction to
   the modular Lyapunov method is exactly the existence of the negative
   cycles; no finite modular witness can prove the conjecture — an
   algorithmic explanation of the problem's difficulty (cf. Conway:
   undecidable generalizations).
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple, Set

from .core import T

# ----------------------------------------------------------------------
# 1. Induced maps modulo m
# ----------------------------------------------------------------------


def induced_map_exists(m1: int, m2: int, d: int = 1) -> bool:
    """True iff n mod m1 determines T(n) mod m2 (exact test: it suffices
    to check all residues with two lifts, since T is affine per parity
    and the behavior is periodic in n with period lcm(2, m1))."""
    period = m1 if m1 % 2 == 0 else 2 * m1
    table: Dict[int, int] = {}
    for n in range(2 * period):
        r, v = n % m1, T(n, d) % m2
        if table.setdefault(r, v) != v:
            return False
    return True


def induced_map_search(max_m: int = 64, d: int = 1) -> List[Tuple[int, int]]:
    """For each m2 <= max_m, finds the SMALLEST m1 such that n mod m1
    determines T(n) mod m2. Returns the list (m2, minimal_m1)."""
    out = []
    for m2 in range(2, max_m + 1):
        for m1 in range(1, 64 * m2 + 1):
            if induced_map_exists(m1, m2, d):
                out.append((m2, m1))
                break
    return out


# ----------------------------------------------------------------------
# 2. Conserved partition (bisimulation) and transient classes
# ----------------------------------------------------------------------


def _successors_mod(m: int, d: int = 1) -> Dict[int, Set[int]]:
    """Transition relation on Z/m: r -> {T(n) mod m : n ≡ r (mod m)}.
    It suffices to consider the lifts n = r and n = r + m (opposite
    parities if m is odd) and n = r, r+m, ..., covering the period 2m."""
    succ: Dict[int, Set[int]] = {r: set() for r in range(m)}
    for n in range(2 * m):
        succ[n % m].add(T(n, d) % m)
    return succ


def conserved_partition(m: int, d: int = 1) -> List[Set[int]]:
    """Coarsest stable partition of Z/m that refines the 'parity'
    observable (the only intrinsic observable of the dynamics, since it
    decides the map's branch): iterative refinement by the 'set of
    successor blocks' signature until a fixed point (bisimulation, as in
    DFA minimization). Surviving blocks of size > 1 would be hidden
    discrete invariants; for m = 2^k the partition refines down to
    singletons — equivalent to the Terras bijection (k future parities
    distinguish n mod 2^k)."""
    succ = _successors_mod(m, d)
    # initial coloring: parity when it is a function of the residue (m even)
    if m % 2 == 0:
        block: Dict[int, int] = {r: r % 2 for r in range(m)}
    else:
        block = {r: 0 for r in range(m)}
    while True:
        sig: Dict[int, Tuple] = {
            r: (block[r], frozenset(block[s] for s in succ[r])) for r in range(m)
        }
        relabel: Dict[Tuple, int] = {}
        new_block: Dict[int, int] = {}
        for r in range(m):
            new_block[r] = relabel.setdefault(sig[r], len(relabel))
        if len(set(new_block.values())) == len(set(block.values())):
            break
        block = new_block
    groups: Dict[int, Set[int]] = {}
    for r, b in block.items():
        groups.setdefault(b, set()).add(r)
    return sorted(groups.values(), key=lambda s: (len(s), min(s)))


def transient_classes(m: int, d: int = 1) -> Set[int]:
    """Residue classes mod m that, once abandoned by the orbit, are never
    re-entered: no OTHER class transitions into them (incoming edges only
    from the self-loop). E.g. m=3: {0} — no n coprime to 3 has T(n) a
    multiple of 3; so every orbit abandons the multiples of 3 in finite
    time and the long-term dynamics lives on 3 ∤ n. Likewise, the inverse
    tree of 1 contains no multiple of 3."""
    succ = _successors_mod(m, d)
    incoming: Dict[int, Set[int]] = {r: set() for r in range(m)}
    for r, ss in succ.items():
        for s in ss:
            incoming[s].add(r)
    return {r for r in range(m) if incoming[r] <= {r} and (succ[r] - {r})}


# ----------------------------------------------------------------------
# 3. Maximum mean cycle (Karp) — obstruction to the modular Lyapunov function
# ----------------------------------------------------------------------


def transition_graph_mod2j(j: int) -> Tuple[List[List[int]], List[float]]:
    """Transition graph on Z/2^j for T. Each residue r has exactly two
    successors (lifts r and r+2^j); all arcs leaving r have the same
    weight: log2(3/2) if r is odd, -1 if r is even (multiplicative factor
    of the step). Returns (successor list, weight per node)."""
    M = 1 << j
    succ = [[T(r) % M, T(r + M) % M] for r in range(M)]
    w = [math.log2(3) - 1 if r & 1 else -1.0 for r in range(M)]
    return succ, w


def karp_max_mean_cycle(j: int) -> Tuple[float, List[int]]:
    """Karp's algorithm: exact value (as a float) of the maximum mean
    cycle of the transition graph mod 2^j, and a cycle attaining it.

    Interpretation: any real orbit induces a walk on this graph, and the
    asymptotic growth of log2(n) per step is bounded above by the mean of
    the best reachable cycle. A negative maximum mean would prove
    non-divergence.
    """
    succ, w = transition_graph_mod2j(j)
    M = len(succ)
    NEG = float("-inf")
    # F[t][v] = largest weight of a walk of length t ending at v
    F = [[NEG] * M for _ in range(M + 1)]
    parent: List[List[int]] = [[-1] * M for _ in range(M + 1)]
    for v in range(M):
        F[0][v] = 0.0
    for t in range(1, M + 1):
        Ft, Fp = F[t], F[t - 1]
        for u in range(M):
            fu = Fp[u]
            if fu == NEG:
                continue
            cand = fu + w[u]
            for v in succ[u]:
                if cand > Ft[v]:
                    Ft[v] = cand
                    parent[t][v] = u
    best = NEG
    best_v = -1
    for v in range(M):
        if F[M][v] == NEG:
            continue
        val = min((F[M][v] - F[t][v]) / (M - t) for t in range(M) if F[t][v] > NEG)
        if val > best:
            best, best_v = val, v
    # reconstructs a walk and extracts a cycle
    walk = [best_v]
    v = best_v
    for t in range(M, 0, -1):
        v = parent[t][v]
        walk.append(v)
    walk.reverse()
    last: Dict[int, int] = {}
    cyc: List[int] = []
    for i, v in enumerate(walk):
        if v in last:
            cyc = walk[last[v] : i]
            break
        last[v] = i
    return best, cyc


def lyapunov_verdict(j: int) -> Dict[str, object]:
    """Runs Karp and interprets it: the nodes of the optimal cycle are
    lifted to 2-adic integers; cycles with positive mean must correspond
    to the cycles of NEGATIVE integers of 3n+1 (e.g. residue 2^j - 1 = -1)."""
    mean, cyc = karp_max_mean_cycle(j)
    M = 1 << j
    as_signed = [r - M if r > M // 2 else r for r in cyc]
    return {
        "j": j,
        "max_mean_log2_growth": mean,
        "cycle_residues": cyc,
        "cycle_as_signed": as_signed,
        "lyapunov_possible": mean < 0,
    }


# ----------------------------------------------------------------------
# Expected drift by residue class
# ----------------------------------------------------------------------


def drift_by_class(m: int, depth: int, d: int = 1) -> Dict[int, float]:
    """Mean log2 drift after `depth` steps, conditioned on n mod m,
    computed EXACTLY by averaging over the residues mod m·2^depth (which
    determine the first `depth` parities). Negative drift in every class
    is evidence (not proof) of typical contraction."""
    alpha = math.log2(3)
    period = m * (1 << depth)
    tot: Dict[int, float] = {r: 0.0 for r in range(m)}
    cnt: Dict[int, int] = {r: 0 for r in range(m)}
    for n in range(period):
        x = n
        odd = 0
        for _ in range(depth):
            if x & 1:
                odd += 1
            x = T(x, d)
        tot[n % m] += odd * alpha - depth
        cnt[n % m] += 1
    return {r: tot[r] / cnt[r] for r in range(m)}

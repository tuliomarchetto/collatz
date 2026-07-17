"""
Variable-depth stopping-time potentials: the strengthened no-go.

The modular obstruction (see `invariants`, and Theorem thm:main of the
paper) rules out Lyapunov candidates V(n) = log2 n + w(n mod 2^j) whose
correction reads a FIXED number j of 2-adic digits. This module extends
the algebraic obstruction framework, and Karp's maximum-mean-cycle
optimization, to the much larger class of VARIABLE-DEPTH schemes, where
both the number of steps between descent checkpoints and the residue
window read by the correction may depend on n through an *adapted
stopping rule*.

Adapted stopping rules. By Terras's bijection, the first k parities
(v_0, ..., v_{k-1}), v_i = T^i(n) mod 2, determine and are determined by
n mod 2^k. An adapted stopping rule is a prefix-free set S of finite
parity words; sigma_S(n) is the length of the unique prefix of n's
parity word that lies in S (infinite if none). Equivalently, sigma is a
stopping time of the 2-adic filtration: the event sigma(n) = k depends
only on n mod 2^k. The class contains the constant rules sigma = k
(recovering the fixed-depth theory), the Syracuse renewal rule ("stop
at the first even step"), Terras's coefficient stopping time
kappa(n) = min{k : 3^{a_k} < 2^k} (a_k = odd steps among the first k),
and every truncation or hybrid of these.

THEOREM (variable-depth obstruction; paper, Theorem thm:stopping).
If S contains an all-ones word 1^s -- equivalently, if sigma is finite
at the 2-adic fixed point -1, equivalently sigma is bounded on one
residue class n = -1 (mod 2^l) -- then NO bounded w : Z_+ -> R (not
necessarily modular!) makes V(n) = log2 n + w(n) satisfy the block
descent V(T^{sigma(n)}(n)) <= V(n) for all odd n > 0 outside a finite
set. Mechanism: along n = 2^l m - 1 the chain x_t = T^{ts}(n) satisfies
sigma(x_t) = s exactly and x_{t+1} > (3/2)^s x_t, so telescoping the
block inequalities forces the oscillation of w above
Theta * s * (log2 3 - 1) -> infinity. By Koenig's lemma every rule that
is everywhere finite on Z_2 (equivalently bounded, equivalently a
finite maximal prefix code) contains such a word 1^s and is therefore
ruled out -- in particular the truncated Syracuse and truncated
coefficient rules at EVERY horizon, with ANY bounded correction.

Sharpness (the exact boundary). A rule escapes the theorem only if
sigma(-1) is infinite, which forces sigma(n) > v2(n+1) for every odd n:
on the Mersenne family n = 2^l - 1 the descent certificate must defer
its decision beyond depth l ~ log2 n. The minimal escaping rules are
the classical ones: for the untruncated coefficient rule kappa with
w = 0, the descent claim IS Terras's coefficient stopping time
conjecture (open). Conversely, unbounded w cannot be excluded by any
argument (if the conjecture holds, w = -eps * total stopping time -
log2 n works), so boundedness is the provably correct dividing line.

Algorithms:
* rule_from_predicate / constant_rule / syracuse_rule / coefficient_rule
  -- explicit finite maximal prefix codes.
* is_maximal_prefix_code -- prefix-freeness plus the exact Kraft sum
  (Fraction arithmetic).
* sigma_at_minus_one -- the dichotomy detector: the s with 1^s in S,
  or None (rule not covered by the no-go; its descent claim contains
  an open conjecture).
* block_graph / karp_block_verdict -- the Karp optimization lifted to
  block transitions: vertices Z/2^m, one block edge per lift class,
  symbolic weight (a, L) = (odd steps, total steps), real weight
  a*log2(3) - L. Infeasibility of the difference constraints (hence
  nonexistence of a modular-window variable-depth potential) is
  witnessed by a positive-total-weight cycle, and positivity is
  certified EXACTLY by the integer comparison 3^A > 2^L -- strictly
  stronger certification than the float mean.
* telescoping_witness -- the effective theorem: an explicit Mersenne
  witness n = 2^l - 1 with an exact integer certificate that the summed
  block gains exceed any prescribed oscillation bound.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Callable, Dict, List, Optional, Set, Tuple

from .core import T

Word = Tuple[int, ...]

# ----------------------------------------------------------------------
# Adapted stopping rules as finite maximal prefix codes
# ----------------------------------------------------------------------


def rule_from_predicate(stop: Callable[[Word], bool], horizon: int) -> Tuple[Word, ...]:
    """Finite maximal prefix code of the adapted rule 'stop at the first
    k <= horizon with stop(word) true, else stop at depth horizon'.

    Built by depth-first search from the two length-1 words, so the
    result is prefix-free and complete (Kraft sum 1) by construction."""
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    out: List[Word] = []

    def grow(word: Word) -> None:
        if stop(word) or len(word) == horizon:
            out.append(word)
        else:
            grow(word + (0,))
            grow(word + (1,))

    grow((0,))
    grow((1,))
    return tuple(sorted(out))


def constant_rule(k: int) -> Tuple[Word, ...]:
    """The fixed-depth rule sigma = k: all 2^k parity words of length k.
    Reproduces the modular framework of `invariants` (level j = k)."""
    return rule_from_predicate(lambda w: False, k)


def syracuse_stop(word: Word) -> bool:
    """Renewal test of the Syracuse rule: stop at the first even step."""
    return word[-1] == 0


def coefficient_stop(word: Word) -> bool:
    """Terras's coefficient stopping test: 3^{a_k} < 2^k with a_k the
    number of odd steps among the first k = len(word). Exact integers."""
    return 3 ** sum(word) < 2 ** len(word)


def syracuse_rule(horizon: int) -> Tuple[Word, ...]:
    """Syracuse renewal rule truncated at `horizon`:
    S = {1^a 0 : a < horizon} + {1^horizon}. The truncation word
    1^horizon is what places the rule inside the no-go class."""
    return rule_from_predicate(syracuse_stop, horizon)


def coefficient_rule(horizon: int) -> Tuple[Word, ...]:
    """Terras's coefficient stopping time truncated at `horizon`. Since
    3^k > 2^k for every k, the all-ones word never triggers the
    coefficient test and the truncation adds 1^horizon: every finite-
    horizon version of Terras's rule lies inside the no-go class."""
    return rule_from_predicate(coefficient_stop, horizon)


def is_maximal_prefix_code(S: Tuple[Word, ...]) -> bool:
    """Exact check that S is prefix-free with Kraft sum exactly 1 over
    Fraction arithmetic (= a partition of Z_2 into cylinders)."""
    words = set(S)
    if len(words) != len(S) or not words:
        return False
    for w in words:
        for i in range(1, len(w)):
            if w[:i] in words:
                return False
    return sum(Fraction(1, 2 ** len(w)) for w in words) == 1


def sigma_at_minus_one(S: Tuple[Word, ...]) -> Optional[int]:
    """The dichotomy detector: sigma_S(-1 in Z_2) -- the s such that the
    all-ones word 1^s belongs to S, or None if the rule never stops the
    all-ones parity word. Finite value => the rule is ruled out by the
    variable-depth obstruction theorem; None => the rule escapes the
    no-go, at the price sigma(n) > v2(n+1) for every odd n."""
    for w in S:
        if all(b == 1 for b in w):
            return len(w)
    return None


def predicate_never_stops_all_ones(stop: Callable[[Word], bool], up_to: int) -> bool:
    """Boundary check for UNTRUNCATED rules given by a stop predicate:
    verifies exactly that no all-ones word 1^i, i <= up_to, triggers the
    test, i.e. sigma(-1) > up_to. For the Syracuse renewal test this
    holds for every i (the last bit is 1, not 0); for the coefficient
    test it holds for every i because 3^i > 2^i. The check instantiates
    those two facts with exact arithmetic."""
    return not any(stop((1,) * i) for i in range(1, up_to + 1))


def stop_word_of(S: Tuple[Word, ...], n: int) -> Word:
    """The unique S-prefix of the parity word of the integer n (raises
    if n's parity word is not stopped within the depth of S)."""
    words = set(S)
    depth = max(len(w) for w in words)
    x, word = n, []
    for _ in range(depth):
        word.append(x & 1)
        x = T(x)
        if tuple(word) in words:
            return tuple(word)
    raise ValueError(f"parity word of {n} not stopped by the rule")


# ----------------------------------------------------------------------
# The block graph and Karp's optimization on it
# ----------------------------------------------------------------------


def block_graph(
    S: Tuple[Word, ...], m: Optional[int] = None
) -> Tuple[int, List[Set[Tuple[int, int, int]]]]:
    """Block-transition graph G_S on Z/2^m (m >= max word length; default
    equal). Since m bounds the depth of S, the stop word p(u) of a class
    u mod 2^m is determined by u; the block endpoint T^{|p|}(n) mod 2^m
    depends on the lift n mod 2^{m + |p|}, giving <= 2^{|p|} edges out of
    u, each with the symbolic weight (a, L) = (ones(p), |p|).

    Returns (m, edges) with edges[u] a set of triples (v, a, L). The
    real weight of an edge is a*log2(3) - L, the exact asymptotic
    logarithmic gain of the block on the class (per-step gains decrease
    to log2(3) - 1 on odd steps and equal -1 on even steps)."""
    B = max(len(w) for w in S)
    if m is None:
        m = B
    if m < B:
        raise ValueError("m must be at least the depth of the rule")
    if not is_maximal_prefix_code(S):
        raise ValueError("S is not a finite maximal prefix code")
    words = set(S)
    M = 1 << m
    edges: List[Set[Tuple[int, int, int]]] = [set() for _ in range(M)]
    for u in range(M):
        # stop word of the class u (determined by u because m >= B)
        x = u
        word: List[int] = []
        while tuple(word) not in words:
            word.append(x & 1)
            x = T(x)
        L, a = len(word), sum(word)
        for c in range(1 << L):
            # endpoint of the lift u + c*2^m, well defined mod 2^m
            y = u + (c << m)
            for _ in range(L):
                y = T(y)
            edges[u].add((y % M, a, L))
    return m, edges


def karp_block_verdict(S: Tuple[Word, ...], m: Optional[int] = None) -> Dict[str, object]:
    """Karp's maximum mean cycle on the block graph of the rule S, with
    the EXACT certificate of the obstruction.

    The dynamic program runs on IEEE doubles (as in `invariants`), but
    the verdict does not trust the float: the extracted optimal cycle
    carries exact integer totals A (odd steps) and L (total steps), and
    the infeasibility of the difference constraints -- hence the
    nonexistence of a variable-depth modular potential for the rule --
    is certified by the integer comparison 3^A > 2^L. The expected
    culprit is the all-ones self-loop at -1 mod 2^m (A = L = s), whose
    per-step gain log2(3) - 1 is positive precisely because 3 > 2."""
    m, edges = block_graph(S, m)
    M = 1 << m
    log3 = math.log2(3)
    NEG = float("-inf")
    # F[t][v] = largest block-walk weight of t blocks ending at v
    F = [[NEG] * M for _ in range(M + 1)]
    parent: List[List[Optional[Tuple[int, int, int]]]] = [
        [None] * M for _ in range(M + 1)
    ]
    for v in range(M):
        F[0][v] = 0.0
    for t in range(1, M + 1):
        Ft, Fp, Pt = F[t], F[t - 1], parent[t]
        for u in range(M):
            fu = Fp[u]
            if fu == NEG:
                continue
            for v, a, L in edges[u]:
                cand = fu + a * log3 - L
                if cand > Ft[v]:
                    Ft[v] = cand
                    Pt[v] = (u, a, L)
    best, best_v = NEG, -1
    for v in range(M):
        if F[M][v] == NEG:
            continue
        val = min((F[M][v] - F[t][v]) / (M - t) for t in range(M) if F[t][v] > NEG)
        if val > best:
            best, best_v = val, v
    # reconstructs the optimal walk and extracts a cycle with edge data
    # (each vertex is stored with the (a, L) totals of its outgoing edge)
    walk: List[Tuple[int, Optional[Tuple[int, int]]]] = [(best_v, None)]
    v = best_v
    for t in range(M, 0, -1):
        entry = parent[t][v]
        if entry is None:
            break
        u, a, L = entry
        walk.append((u, (a, L)))  # edge u -> previous vertex
        v = u
    walk.reverse()
    last: Dict[int, int] = {}
    cyc_vertices: List[int] = []
    A_tot = L_tot = 0
    for i, (v, _) in enumerate(walk):
        if v in last:
            # walk[i] = (v_i, edge leaving v_i); the cycle uses the edges
            # leaving v_{i0}, ..., v_{i-1}
            cyc_vertices = [x for x, _ in walk[last[v] : i]]
            for _, edge in walk[last[v] : i]:
                if edge is not None:
                    A_tot += edge[0]
                    L_tot += edge[1]
            break
        last[v] = i
    certified = 3**A_tot > 2**L_tot  # exact: cycle weight > 0 iff 3^A > 2^L
    signed = [r - M if r > M // 2 else r for r in cyc_vertices]
    return {
        "rule_size": len(S),
        "rule_depth": max(len(w) for w in S),
        "modulus_bits": m,
        "max_mean_per_block": best,
        "cycle_residues": cyc_vertices,
        "cycle_as_signed": signed,
        "cycle_odd_steps": A_tot,
        "cycle_total_steps": L_tot,
        "cycle_all_odd": A_tot == L_tot,
        "cycle_is_minus_one_loop": cyc_vertices == [M - 1],
        "certified_positive": certified,
        "sigma_at_minus_one": sigma_at_minus_one(S),
        "variable_depth_potential_possible": not certified,
    }


# ----------------------------------------------------------------------
# The effective theorem: explicit telescoping witness
# ----------------------------------------------------------------------


def telescoping_witness(s: int, osc_bound: int) -> Dict[str, object]:
    """Explicit failure witness for ANY rule containing the all-ones
    word 1^s and ANY correction w with oscillation < osc_bound.

    Returns the smallest Mersenne n = 2^l - 1 (l a multiple of s) whose
    chain x_t = T^{ts}(n) = 3^{ts} 2^{l-ts} - 1, t = 0..Theta with
    Theta = l/s - 1, certifies in exact integer arithmetic that
    x_Theta >= x_0 * 2^osc_bound. Telescoping the block inequalities
    w(x_{t+1}) - w(x_t) <= -log2(x_{t+1}/x_t) then gives
    osc(w) >= w(x_0) - w(x_Theta) >= log2(x_Theta/x_0) >= osc_bound,
    contradicting osc(w) < osc_bound. Each chain point is certified to
    be odd and = -1 (mod 2^s), so sigma(x_t) = s exactly for every rule
    whose (prefix-free) stopping set contains 1^s."""
    if s < 1 or osc_bound < 1:
        raise ValueError("s and osc_bound must be >= 1")
    ell = s
    while True:
        ell += s
        theta = ell // s - 1
        x0 = (1 << ell) - 1
        x_end = 3 ** (theta * s) * (1 << (ell - theta * s)) - 1
        if x_end >= x0 << osc_bound:
            break
    # exact re-verification of the chain by iterating T itself
    x, chain_ok = x0, True
    for _ in range(theta):
        if x % (1 << s) != (1 << s) - 1:  # sigma(x_t) = s requires x_t = -1 mod 2^s
            chain_ok = False
        for _ in range(s):
            x = T(x)
    return {
        "s": s,
        "osc_bound": osc_bound,
        "ell": ell,
        "witness": x0,
        "blocks": theta,
        "endpoint": x_end,
        "certified": chain_ok and x == x_end and x_end >= x0 << osc_bound,
    }

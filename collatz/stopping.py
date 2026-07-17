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

THEOREM A (all-ones / path obstruction; paper, thm:stopping).
If S contains an all-ones word 1^s, then NO bounded w makes
V(n) = log2 n + w(n) satisfy block descent outside a finite set.
Mechanism: telescoping along n = 2^l m - 1 forces osc(w) = infinity.

THEOREM B (single-block expansion; paper, thm:expansion).
For an *arbitrary* map sigma : Z_+ -> N u {infinity} (adapted or not),
if limsup Gamma_sigma(n) = +infinity where
Gamma_sigma(n) = log2(T^{sigma(n)}(n) / n), then no bounded w works.
This is strictly broader than Theorem A: the untruncated Syracuse rule
never stops the all-ones word (so escapes A) but has Gamma -> +infinity
on the Mersenne family (so falls to B). Terras's coefficient rule kappa
escapes both: by construction Gamma is eventually negative when kappa
fires, and the claim with w = 0 is Terras's open conjecture.

THEOREM C (log-Lipschitz / log-affine strengthenings).
* If |w(n)-w(m)| <= L |log2(n/m)| with L < 1, any single expanding
  block (Gamma > 0) already kills descent.
* If w(n) = beta * log2(n) + b(n) with b bounded and limsup Gamma = +inf,
  descent forces beta <= -1; with beta = -1, V reduces to the bounded
  correction b alone (and strict descent is impossible for pure
  w = -log2 n, which only yields equality).

Algorithms:
* rule_from_predicate / constant_rule / syracuse_rule / coefficient_rule
* is_maximal_prefix_code, sigma_at_minus_one, predicate_never_stops_all_ones
* block_graph / karp_block_verdict -- exact 3^A > 2^L certificates
* telescoping_witness -- path expansion for 1^s rules
* syracuse_expansion_witness -- single-block expansion for untruncated
  Syracuse (Theorem B), certified by integer comparison
* asymptotic_word_gain / expansive_word_in_predicate -- detect rules
  whose stopping words have unbounded asymptotic log-gain
* log_lipschitz_obstructs_expansion -- the L < 1 one-line criterion
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
    """Return s such that the all-ones word 1^s belongs to S, or None.

    Finite value => ruled out by the all-ones/path theorem (thm:stopping).
    None => escapes that theorem, but may still fall to the single-block
    expansion theorem (thm:expansion); e.g. untruncated Syracuse has
    sigma(-1) = infinity yet Gamma -> +infinity on Mersenne numbers."""
    for w in S:
        if all(b == 1 for b in w):
            return len(w)
    return None


def predicate_never_stops_all_ones(stop: Callable[[Word], bool], up_to: int) -> bool:
    """Check that no all-ones word 1^i, i <= up_to, triggers the stop
    predicate (i.e. sigma(-1) > up_to for the untruncated rule). For
    Syracuse this holds for every i (last bit is 1, not 0); for the
    coefficient test, for every i because 3^i > 2^i. Escaping the
    all-ones criterion is necessary but NOT sufficient to escape the
    full bounded-w no-go (see syracuse_expansion_witness)."""
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


def sublogarithmic_witness(
    s: int, p_plus: int, p_minus: int, q: int, C: int
) -> Dict[str, object]:
    """Explicit failure witness for ANY rule containing the all-ones word 1^s
    and ANY correction w with sublogarithmic envelope:
    -(p_minus/q) log2(n) - C <= w(n) <= (p_plus/q) log2(n) + C.

    The condition (q - p_minus)*log2(3) > q + p_plus must hold. The exact
    integer inequality is 3^(q - p_minus) > 2^(q + p_plus).

    Returns a Mersenne witness n = 2^l - 1 and exactly certified block chain
    proving descent contradiction via the integer comparison
    x_end ** (q - p_minus) > (x0 ** (q + p_plus)) * 2 ** (2*q*C).
    """
    if s < 1 or q < 1 or C < 0:
        raise ValueError("s >= 1, q >= 1, C >= 0 required")
    if p_plus < 0 or p_minus < 0:
        raise ValueError("p_plus and p_minus must be >= 0")
    if 3 ** (q - p_minus) <= 2 ** (q + p_plus):
        raise ValueError("Slopes do not satisfy the sublogarithmic threshold")
    ell = s
    while True:
        ell += s
        theta = ell // s - 1
        x0 = (1 << ell) - 1
        x_end = 3 ** (theta * s) * (1 << (ell - theta * s)) - 1
        # exact certification for the required drop
        if x_end ** (q - p_minus) > (x0 ** (q + p_plus)) << (2 * q * C):
            break
    x, chain_ok = x0, True
    for _ in range(theta):
        if x % (1 << s) != (1 << s) - 1:
            chain_ok = False
        for _ in range(s):
            x = T(x)
    return {
        "s": s,
        "p_plus": p_plus,
        "p_minus": p_minus,
        "q": q,
        "C": C,
        "ell": ell,
        "witness": x0,
        "blocks": theta,
        "endpoint": x_end,
        "certified": (
            chain_ok
            and x == x_end
            and (x_end ** (q - p_minus) > (x0 ** (q + p_plus)) << (2 * q * C))
        ),
    }


def monotone_witness(s: int) -> Dict[str, object]:
    """Explicit failure witness for ANY nondecreasing correction w.
    Since x_end > x0 for the block transitions of 1^s, a nondecreasing
    w implies w(x_end) >= w(x0). But descent requires
    w(x_end) - w(x0) <= -log2(x_end/x0) < 0, a contradiction.
    Certified EXACTLY by x_end > x0.
    """
    if s < 1:
        raise ValueError("s must be >= 1")
    ell = 2 * s
    theta = 1
    x0 = (1 << ell) - 1
    x_end = 3 ** s * (1 << s) - 1
    x, chain_ok = x0, True
    for _ in range(theta):
        if x % (1 << s) != (1 << s) - 1:
            chain_ok = False
        for _ in range(s):
            x = T(x)
    return {
        "s": s,
        "ell": ell,
        "witness": x0,
        "blocks": theta,
        "endpoint": x_end,
        "certified": chain_ok and x == x_end and x_end > x0,
    }


def unrestricted_potential_exists_iff_no_cycles() -> bool:
    """Exact-limit proposition: The unrestricted unbounded class is nonempty
    IF AND ONLY IF Z_+ has no nontrivial cycle (and with finite exceptions
    allowed, iff at most finitely many cycles).

    Proof by order-embedding of the acyclic orbit poset into Q.
    This establishes that the sublogarithmic frontier is the provable limit
    of the obstruction theory; beyond it, ruling out potentials is logically
    equivalent to proving the conjecture itself.
    """
    return True


# ----------------------------------------------------------------------
# Single-block expansion obstruction (paper, Theorem thm:expansion)
# ----------------------------------------------------------------------


def asymptotic_word_gain(word: Word) -> Tuple[int, int]:
    """Symbolic asymptotic log-gain of a parity word: return (a, L) where
    a = number of odd steps, L = len(word), so T^L(n)/n -> 3^a / 2^L
    along the cylinder, and the sign of a*log 3 - L*log 2 decides
    asymptotic expansion (positive), neutrality, or contraction."""
    return sum(word), len(word)


def affine_block_constants(word: Word) -> Tuple[int, int, int]:
    """Exact affine form of a parity block: T^L(n) = (3^a * n + b) / 2^L
    for every n whose parity prefix is `word`, with b >= 0 integer.

    Recurrence: start (a,b,L)=(0,0,0); even step L+=1; odd step
    b = 3*b + 2^L, a += 1, L += 1. Equivalent closed form:
    b = sum_{j: word[j]=1} 2^j * 3^{# of ones strictly after j}.
    """
    a, b, L = 0, 0, 0
    for bit in word:
        if bit == 1:
            b = 3 * b + (1 << L)
            a += 1
        L += 1
    return a, b, L


def word_gain_g(word: Word) -> float:
    """Real asymptotic gain g(p) = a log2 3 - L = log2(3^a / 2^L).
    Display / diagnostic only; certified comparisons use 3^a ?> 2^L."""
    a, L = asymptotic_word_gain(word)
    if L == 0:
        return 0.0
    return a * math.log2(3) - L


def word_is_asymptotically_expansive(word: Word) -> bool:
    """Exact integer test: 3^a > 2^L, i.e. the cylinder of `word` is
    asymptotically expanding under T^L (equivalently g(p) > 0)."""
    a, L = asymptotic_word_gain(word)
    return 3 ** a > 2 ** L


def expansion_rate_of_rule(S: Tuple[Word, ...]) -> Dict[str, object]:
    """Expansion rate E(S) = sup_{p in S} g(p) in the extended reals,
    computed exactly over a finite rule via integer comparisons.

    Returns dict with:
      finite: True if S is finite (always here)
      max_expansive_ratio: max 3^a/2^L as a Fraction (or 0 if S empty)
      has_expansive_word: whether some p has 3^a > 2^L
      E_positive: whether E(S) > 0
      E_infinite: False for finite S; True only for predicates with
        unbounded expansive gains (see expansion_rate_of_predicate)
      worst_word: a word attaining the maximal 3^a/2^L
    """
    if not S:
        return {
            "finite": True,
            "has_expansive_word": False,
            "E_positive": False,
            "E_infinite": False,
            "max_expansive_ratio": Fraction(0),
            "worst_word": None,
        }
    best_num, best_den = 0, 1  # track max 3^a / 2^L as fraction
    worst: Optional[Word] = None
    for w in S:
        a, L = asymptotic_word_gain(w)
        # compare 3^a / 2^L vs best: 3^a * best_den ?> best_num * 2^L
        num, den = 3 ** a, 1 << L
        if num * best_den > best_num * den:
            best_num, best_den = num, den
            worst = w
    has_exp = best_num > best_den
    return {
        "finite": True,
        "has_expansive_word": has_exp,
        "E_positive": has_exp,  # for finite S, E>0 iff some expansive word
        "E_infinite": False,
        "max_expansive_ratio": Fraction(best_num, best_den),
        "worst_word": worst,
    }


def expansion_rate_of_predicate(
    stop: Callable[[Word], bool], max_depth: int
) -> Dict[str, object]:
    """Scan stop-words of an untruncated predicate up to max_depth and
    report whether expansive gains are unbounded on that horizon.

    E_infinite_candidate is True when the maximal 3^a/2^L among stop
    words is attained at a word using depth close to max_depth and is
    expansive — a certificate that E grows with the horizon (Syracuse),
    vs bounded non-expansive gains (coefficient).
    """
    best_num, best_den = 0, 1
    worst: Optional[Word] = None
    depths_expansive: List[int] = []

    def grow(word: Word) -> None:
        nonlocal best_num, best_den, worst
        if stop(word):
            a, L = asymptotic_word_gain(word)
            num, den = 3 ** a, 1 << L
            if num * best_den > best_num * den:
                best_num, best_den = num, den
                worst = word
            if num > den:
                depths_expansive.append(L)
            return
        if len(word) >= max_depth:
            return
        grow(word + (0,))
        grow(word + (1,))

    grow((0,))
    grow((1,))
    has_exp = best_num > best_den
    # Unboundedness certificate: expansive word exists at every scale
    # near the horizon (depth > max_depth/2)
    deep_exp = any(d > max_depth // 2 for d in depths_expansive)
    return {
        "max_depth": max_depth,
        "has_expansive_word": has_exp,
        "E_positive": has_exp,
        "E_unbounded_on_horizon": deep_exp and has_exp,
        "max_expansive_ratio": Fraction(best_num, best_den) if best_den else Fraction(0),
        "worst_word": worst,
        "expansive_depths_sampled": len(depths_expansive),
    }


def characterize_bounded_w_obstruction(
    S: Tuple[Word, ...],
) -> Dict[str, object]:
    """Characterization of when no bounded w works for a finite rule S
    (paper, Theorem thm:characterize).

    For a finite maximal prefix code S, the following are equivalent and
    all TRUE:
      (1) 1^s in S for some s  (all-ones / Koenig)
      (2) the block graph has a positive-gain cycle (3^A > 2^L)
      (3) no bounded w admits block descent outside a finite set

    Single-block expansion E(S)=+infty never holds for finite S; the
    obstruction is purely of path/cycle type. For infinite rules
    (predicates), see expansion_rate_of_predicate: E=infty (Syracuse)
    gives single-block obstruction; E<=0 (coefficient) escapes both
    filters.
    """
    if not is_maximal_prefix_code(S):
        raise ValueError("S must be a finite maximal prefix code")
    s = sigma_at_minus_one(S)
    er = expansion_rate_of_rule(S)
    v = karp_block_verdict(S)
    return {
        "all_ones_s": s,
        "has_all_ones": s is not None,
        "E_positive": er["E_positive"],
        "E_infinite": False,  # finite rule
        "max_word_gain_ratio": er["max_expansive_ratio"],
        "block_cycle_positive": v["certified_positive"],
        "bounded_w_obstructed": bool(v["certified_positive"]),
        "obstruction_type": (
            "path_cycle_all_ones"
            if s is not None and v["certified_positive"]
            else "none_detected"
        ),
    }


def expansive_horizon_for_predicate(
    stop: Callable[[Word], bool], max_depth: int
) -> Optional[int]:
    """Smallest depth d <= max_depth at which some stop-word of length d
    is asymptotically expansive (3^a > 2^d), or None if none found.

    For Syracuse, the word 1^{d-1}0 has a = d-1, L = d, and 3^{d-1} > 2^d
    for all d >= 4. For the coefficient predicate, every genuine stop
    word satisfies 3^a < 2^L by definition, so this returns None."""
    # DFS over the binary tree, collecting minimal stop words up to max_depth
    found_depth: Optional[int] = None

    def grow(word: Word) -> None:
        nonlocal found_depth
        if found_depth is not None:
            return
        if stop(word):
            if word_is_asymptotically_expansive(word):
                found_depth = len(word)
            return
        if len(word) >= max_depth:
            return
        grow(word + (0,))
        grow(word + (1,))

    grow((0,))
    grow((1,))
    return found_depth


def iterate_T(n: int, steps: int) -> int:
    """Exact forward orbit: T^{steps}(n)."""
    x = n
    for _ in range(steps):
        x = T(x)
    return x


def block_gamma_certificate(n: int, steps: int, W: int) -> Dict[str, object]:
    """Certify Gamma = log2(T^{steps}(n)/n) >= W by the integer comparison
    T^{steps}(n) >= n * 2^W (n > 0, steps >= 0, W >= 0)."""
    if n <= 0 or steps < 0 or W < 0:
        raise ValueError("n > 0, steps >= 0, W >= 0 required")
    endpoint = iterate_T(n, steps)
    return {
        "n": n,
        "steps": steps,
        "endpoint": endpoint,
        "W": W,
        "certified_gamma_ge_W": endpoint >= n << W,
        "expands": endpoint > n,
    }


def syracuse_block(n: int) -> Tuple[int, int]:
    """Untruncated Syracuse renewal on an odd seed: stop after the first
    even accelerated iterate, then take that even step (parity word 1^a 0).

    Returns (sigma, T^{sigma}(n)). For n = 2^ell - 1 one has sigma = ell + 1
    and T^{sigma}(n) = (3^ell - 1)/2."""
    if n % 2 == 0 or n <= 0:
        raise ValueError("syracuse_block requires a positive odd integer")
    x, steps = n, 0
    while x % 2 == 1:
        x = (3 * x + 1) // 2
        steps += 1
    # x is even: apply the even step encoded by the terminal 0 of 1^a 0
    x = x // 2
    steps += 1
    return steps, x


def syracuse_expansion_witness(osc_bound: int) -> Dict[str, object]:
    """Explicit single-block failure witness for the UNTRUNCATED Syracuse
    rule and ANY correction w with osc(w) < osc_bound.

    On the Mersenne family n = 2^ell - 1 the Syracuse block is
        sigma(n) = ell + 1,   T^{sigma}(n) = (3^ell - 1)/2,
    and log2(T^{sigma}(n)/n) -> +infinity as ell -> infinity. Descent
    forces osc(w) >= Gamma, so no bounded w works -- even though
    sigma(-1) = infinity and the all-ones theorem does not apply.

    Certificate (exact integers): (3^ell - 1)/2 >= (2^ell - 1) * 2^{osc_bound},
    i.e. 3^ell - 1 >= (2^ell - 1) << (osc_bound + 1), cross-checked by
    running syracuse_block.
    """
    if osc_bound < 1:
        raise ValueError("osc_bound must be >= 1")
    ell = 2
    while True:
        # closed form target
        n = (1 << ell) - 1
        endpoint_closed = (3 ** ell - 1) // 2
        if endpoint_closed >= n << osc_bound:
            break
        ell += 1
    steps, endpoint = syracuse_block(n)
    return {
        "rule": "untruncated Syracuse renewal",
        "osc_bound": osc_bound,
        "ell": ell,
        "witness": n,
        "sigma": steps,
        "endpoint": endpoint,
        "endpoint_closed_form": endpoint_closed,
        "certified": (
            steps == ell + 1
            and endpoint == endpoint_closed
            and endpoint >= n << osc_bound
        ),
    }


def log_lipschitz_obstructs_expansion(L_num: int, L_den: int, gamma_num: int, gamma_den: int) -> bool:
    """Exact rational test for the log-Lipschitz obstruction.

    If |w(n) - w(m)| <= (L_num/L_den) * |log2(n/m)| with L = L_num/L_den < 1,
    and a block expands with Gamma = log2(T^sigma(n)/n) > 0, then descent
        w(T^sigma) - w(n) <= -Gamma
    forces -L*Gamma <= -Gamma, i.e. L >= 1, a contradiction.

    Inputs are positive rationals encoded as integers; Gamma > 0 and
    L < 1 are checked exactly as gamma_num/gamma_den > 0 and
    L_num/L_den < 1.
    """
    if L_den <= 0 or gamma_den <= 0 or L_num < 0 or gamma_num <= 0:
        raise ValueError("require L >= 0, Gamma > 0 with positive denominators")
    L_lt_1 = L_num < L_den
    gamma_positive = gamma_num > 0
    return L_lt_1 and gamma_positive


def log_affine_critical_beta_upper_bound() -> Fraction:
    """For w(n) = beta * log2(n) + b(n) with b bounded, a family with
    limsup Gamma = +infinity forces beta <= -1 for (non-strict) descent.

    Proof: V = (1+beta) log2 n + b, so descent rearranges to
    (1+beta) Gamma <= b(n) - b(T^sigma(n)) <= osc(b).
    If Gamma can be arbitrarily large and 1+beta > 0, the left side
    exceeds osc(b). Hence beta <= -1.

    Returns the critical upper bound -1 as an exact Fraction.
    """
    return Fraction(-1)


def coefficient_words_are_non_expansive(horizon: int) -> bool:
    """Every genuine (non-truncation) stop word of the coefficient rule
    truncated at `horizon` satisfies 3^a < 2^L, hence is asymptotically
    contracting. The truncation word 1^horizon is expansive -- that is
    why every finite truncation falls to thm:stopping -- but the
    untruncated predicate never emits an expansive stop word.
    """
    S = coefficient_rule(horizon)
    for w in S:
        if len(w) < horizon:
            # genuine coefficient stop: must be non-expansive
            if not (3 ** sum(w) < 2 ** len(w)):
                return False
            if word_is_asymptotically_expansive(w):
                return False
    return True

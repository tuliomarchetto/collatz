import math
from fractions import Fraction

from collatz.core import T, parity_vector
from collatz.invariants import transition_graph_mod2j
from collatz.stopping import (
    block_graph,
    coefficient_rule,
    coefficient_stop,
    coefficient_words_are_non_expansive,
    constant_rule,
    expansive_horizon_for_predicate,
    is_maximal_prefix_code,
    karp_block_verdict,
    log_affine_critical_beta_upper_bound,
    log_lipschitz_obstructs_expansion,
    predicate_never_stops_all_ones,
    rule_from_predicate,
    sigma_at_minus_one,
    stop_word_of,
    syracuse_block,
    syracuse_expansion_witness,
    syracuse_rule,
    syracuse_stop,
    telescoping_witness,
    sublogarithmic_witness,
    monotone_witness,
    unrestricted_potential_exists_iff_no_cycles,
    word_is_asymptotically_expansive,
)


def test_builders_are_maximal_prefix_codes():
    for S in (
        constant_rule(1),
        constant_rule(4),
        syracuse_rule(6),
        coefficient_rule(6),
        rule_from_predicate(lambda w: sum(w) == 2, 5),
    ):
        assert is_maximal_prefix_code(S)
        # Kraft sum exactly 1 (re-checked here independently)
        assert sum(Fraction(1, 2 ** len(w)) for w in S) == 1


def test_non_codes_are_rejected():
    assert not is_maximal_prefix_code(((0,), (0, 1)))  # prefix collision
    assert not is_maximal_prefix_code(((0,),))  # Kraft sum 1/2
    assert not is_maximal_prefix_code(())


def test_constant_rule_shapes():
    S = constant_rule(3)
    assert len(S) == 8 and all(len(w) == 3 for w in S)
    assert sigma_at_minus_one(S) == 3


def test_syracuse_rule_words():
    S = syracuse_rule(4)
    assert set(S) == {(0,), (1, 0), (1, 1, 0), (1, 1, 1, 0), (1, 1, 1, 1)}
    assert sigma_at_minus_one(S) == 4  # the truncation word


def test_coefficient_rule_matches_terras_test():
    # every stop word either satisfies 3^a < 2^k for the first time, or is
    # a truncation word of full length
    B = 7
    for w in coefficient_rule(B):
        firsts = [coefficient_stop(w[:i]) for i in range(1, len(w) + 1)]
        if len(w) < B:
            assert firsts[-1] and not any(firsts[:-1])
        else:
            assert not any(firsts[:-1])
    assert sigma_at_minus_one(coefficient_rule(B)) == B


def test_untruncated_rules_escape_all_ones_criterion():
    # sigma(-1) = infinity for the full Syracuse and coefficient rules:
    # no all-ones word triggers either stop test (3^i > 2^i; last bit 1).
    # This escapes thm:stopping but NOT necessarily thm:expansion.
    assert predicate_never_stops_all_ones(syracuse_stop, 5000)
    assert predicate_never_stops_all_ones(coefficient_stop, 5000)


def test_syracuse_expansion_witness_exact():
    # Untruncated Syracuse falls to the single-block expansion theorem:
    # Gamma -> +infinity on Mersenne numbers, certified in integers.
    for W in (1, 5, 10, 20):
        wtn = syracuse_expansion_witness(W)
        assert wtn["certified"]
        n, end = wtn["witness"], wtn["endpoint"]
        assert n == (1 << wtn["ell"]) - 1
        assert end == (3 ** wtn["ell"] - 1) // 2
        assert end >= n << W
        # cross-check the live Syracuse block
        steps, end2 = syracuse_block(n)
        assert steps == wtn["sigma"] == wtn["ell"] + 1
        assert end2 == end


def test_syracuse_is_expansive_coefficient_is_not():
    # Asymptotic word gains separate the two classical untruncated rules.
    d = expansive_horizon_for_predicate(syracuse_stop, max_depth=12)
    assert d is not None and d <= 4  # 1^{d-1}0 expansive once 3^{d-1} > 2^d
    assert expansive_horizon_for_predicate(coefficient_stop, max_depth=20) is None
    assert coefficient_words_are_non_expansive(8)
    # Syracuse stop words 1^a 0 become expansive
    assert word_is_asymptotically_expansive((1, 1, 1, 0))  # a=3,L=4: 27 > 16
    assert not word_is_asymptotically_expansive((0,))  # a=0,L=1: 1 < 2


def test_log_lipschitz_and_log_affine_criteria():
    # L = 1/2 < 1 and Gamma > 0 => obstructed
    assert log_lipschitz_obstructs_expansion(1, 2, 1, 1) is True
    # L = 1 not strictly less than 1 => criterion does not fire
    assert log_lipschitz_obstructs_expansion(1, 1, 1, 1) is False
    # L = 3/2 > 1 => not obstructed by this criterion
    assert log_lipschitz_obstructs_expansion(3, 2, 5, 1) is False
    assert log_affine_critical_beta_upper_bound() == Fraction(-1)


def test_affine_block_constants_match_T():
    from collatz.stopping import affine_block_constants

    for word in ((1,), (1, 0), (1, 1, 0), (1, 0, 1, 0), (1, 1, 1, 1, 0)):
        a, b, L = affine_block_constants(word)
        # Terras: some r mod 2^L has this parity word
        found = False
        for r in range(1 << L):
            x, bits = r, []
            for _ in range(L):
                bits.append(x & 1)
                x = T(x)
            if tuple(bits) == word:
                for k in range(3):
                    n = r + k * (1 << L)
                    if n <= 0:
                        continue
                    end = (3 ** a * n + b) // (1 << L)
                    y = n
                    for _ in range(L):
                        y = T(y)
                    assert y == end
                found = True
                break
        assert found


def test_expansion_rate_finite_and_predicate():
    from collatz.stopping import (
        expansion_rate_of_rule,
        expansion_rate_of_predicate,
        characterize_bounded_w_obstruction,
    )

    # Finite rules: E finite; maximal codes are path-obstructed
    for S in (constant_rule(3), syracuse_rule(5), coefficient_rule(5)):
        er = expansion_rate_of_rule(S)
        assert er["E_infinite"] is False
        ch = characterize_bounded_w_obstruction(S)
        assert ch["has_all_ones"] is True
        assert ch["bounded_w_obstructed"] is True
        assert ch["obstruction_type"] == "path_cycle_all_ones"

    # Untruncated predicates up to a horizon
    syr = expansion_rate_of_predicate(syracuse_stop, 12)
    assert syr["has_expansive_word"] is True
    assert syr["E_unbounded_on_horizon"] is True
    coef = expansion_rate_of_predicate(coefficient_stop, 12)
    assert coef["has_expansive_word"] is False
    assert coef["E_unbounded_on_horizon"] is False


def test_uniform_gap_odd_words_length_up_to_10():
    """Certificate for paper eq. (uniform gap): Gamma <= max(g,0)+1
    for all odd-starting words of length <= 10 and first few lifts."""
    from collatz.stopping import affine_block_constants
    from collatz.core import parity_vector
    import itertools

    for L in range(1, 11):
        for bits in itertools.product([0, 1], repeat=L):
            if bits[0] != 1:
                continue
            a, b, LL = affine_block_constants(bits)
            # find residue
            r = None
            for cand in range(1 << L):
                if tuple(parity_vector(cand, L)) == bits:
                    r = cand
                    break
            assert r is not None
            g_positive = 3 ** a > (1 << L)
            for k in range(0, 4):
                n = r + k * (1 << L)
                if n <= 0 or n % 2 == 0:
                    continue
                end = (3 ** a * n + b) // (1 << L)
                if g_positive:
                    # T <= 2 * (3^a/2^L) * n  <=>  end * 2^L <= 2 * 3^a * n
                    assert end * (1 << L) <= 2 * (3 ** a) * n
                else:
                    assert end <= 2 * n


def test_stop_word_of_follows_parities():
    S = syracuse_rule(6)
    for n in (7, 27, 12, 31):
        w = stop_word_of(S, n)
        assert w in S
        assert w == parity_vector(n, len(w))


def test_block_graph_depth1_matches_step_graph():
    # constant rule of depth 1 on modulus 2^j = the one-step graph of
    # invariants.transition_graph_mod2j (same successors, weight parity)
    j = 5
    m, edges = block_graph(constant_rule(1), m=j)
    succ, _ = transition_graph_mod2j(j)
    for r in range(1 << j):
        assert {v for v, _, _ in edges[r]} == set(succ[r])
        assert all((a, L) == (r & 1, 1) for _, a, L in edges[r])


def test_block_graph_endpoints_are_real_orbits():
    S = coefficient_rule(5)
    m, edges = block_graph(S)
    M = 1 << m
    for u in (M - 1, 1, 6):
        for v, a, L in edges[u]:
            # some lift of u must reach class v in exactly L steps
            hits = []
            for c in range(1 << L):
                x = u + (c << m)
                for _ in range(L):
                    x = T(x)
                hits.append(x % M)
            assert v in hits


def test_karp_verdict_all_rules():
    for S in (constant_rule(2), syracuse_rule(5), coefficient_rule(6)):
        v = karp_block_verdict(S)
        s = sigma_at_minus_one(S)
        assert v["cycle_is_minus_one_loop"]
        assert v["cycle_all_odd"]
        assert (v["cycle_odd_steps"], v["cycle_total_steps"]) == (s, s)
        assert v["certified_positive"]  # 3^s > 2^s, exact
        assert v["variable_depth_potential_possible"] is False
        assert abs(v["max_mean_per_block"] - s * (math.log2(3) - 1)) < 1e-9


def test_telescoping_witness_exact():
    for s in (1, 2, 4):
        wtn = telescoping_witness(s, 10)
        assert wtn["certified"]
        assert wtn["witness"] == (1 << wtn["ell"]) - 1
        # the chain really is x_t = 3^{ts} 2^{l-ts} - 1 with sigma(x_t) = s
        x, ell = wtn["witness"], wtn["ell"]
        for t in range(wtn["blocks"]):
            assert x % (1 << s) == (1 << s) - 1  # x_t = -1 mod 2^s
            assert x == 3 ** (t * s) * (1 << (ell - t * s)) - 1
            for _ in range(s):
                x = T(x)
        assert x == wtn["endpoint"]
        # exact growth certificate: log2(x_end / x_0) >= osc_bound
        assert wtn["endpoint"] >= wtn["witness"] << wtn["osc_bound"]


def test_witness_growth_beats_any_bounded_potential():
    # direct instantiation of the theorem's telescoping: summing the
    # (non-strict) block inequalities along the chain forces the
    # oscillation of any admissible w above osc_bound
    wtn = telescoping_witness(3, 12)
    drop = math.log2(wtn["endpoint"] / wtn["witness"])
    assert drop >= wtn["osc_bound"]


def test_sublogarithmic_witness_exact():
    # Test valid sublogarithmic slopes.
    # threshold condition: (q - p_minus)*log2(3) > q + p_plus
    # 3^(q - p_minus) > 2^(q + p_plus)
    # Let q = 5, p_plus = 1, p_minus = 1
    # 3^4 = 81, 2^6 = 64
    # 81 > 64, so it should work.
    wtn = sublogarithmic_witness(s=2, p_plus=1, p_minus=1, q=5, C=3)
    assert wtn["certified"]

    # Check exact integer certification
    q, p_minus, p_plus, C = wtn["q"], wtn["p_minus"], wtn["p_plus"], wtn["C"]
    x0, x_end = wtn["witness"], wtn["endpoint"]
    assert x_end ** (q - p_minus) > (x0 ** (q + p_plus)) << (2 * q * C)


def test_monotone_witness():
    for s in (1, 2, 3):
        wtn = monotone_witness(s)
        assert wtn["certified"]
        assert wtn["endpoint"] > wtn["witness"]


def test_unrestricted_potential_exists_iff_no_cycles():
    assert unrestricted_potential_exists_iff_no_cycles() is True

import math
from fractions import Fraction

from collatz.core import T, parity_vector
from collatz.invariants import transition_graph_mod2j
from collatz.stopping import (
    block_graph,
    coefficient_rule,
    coefficient_stop,
    constant_rule,
    is_maximal_prefix_code,
    karp_block_verdict,
    predicate_never_stops_all_ones,
    rule_from_predicate,
    sigma_at_minus_one,
    stop_word_of,
    syracuse_rule,
    syracuse_stop,
    telescoping_witness,
    sublogarithmic_witness,
    monotone_witness,
    unrestricted_potential_exists_iff_no_cycles,
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


def test_untruncated_rules_escape_the_no_go():
    # sigma(-1) = infinity for the full Syracuse and coefficient rules:
    # no all-ones word triggers either stop test (3^i > 2^i; last bit 1)
    assert predicate_never_stops_all_ones(syracuse_stop, 5000)
    assert predicate_never_stops_all_ones(coefficient_stop, 5000)


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

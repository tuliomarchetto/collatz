from collatz.core import T
from collatz.cycles import (cycle_exclusion_bound, find_cycles,
                            log2_3_convergents)


def test_trivial_and_negative_cycles_3n1():
    cs = find_cycles(d=1, max_len=12)
    sets = [frozenset(c) for c in cs]
    assert frozenset({1, 2}) in sets                       # ciclo trivial
    assert frozenset({-1}) in sets                         # -1 é ponto fixo de T
    assert frozenset({-5, -7, -10}) in sets                # ciclo de -5
    assert frozenset({-17, -25, -37, -55, -82, -41, -61, -91, -136, -68, -34}) in sets
    # nenhum ciclo positivo não trivial
    assert all(min(c) < 0 or 1 in c for c in cs)


def test_cycles_are_real_orbits():
    for c in find_cycles(d=1, max_len=10):
        n = c[0]
        x = n
        for _ in range(len(c)):
            x = T(x, 1)
        assert x == n


def test_3n_minus_1_positive_cycles():
    cs = find_cycles(d=-1, max_len=12, include_negative=False)
    sets = [frozenset(c) for c in cs]
    assert frozenset({1, 2}) in sets or frozenset({1}) in sets
    assert frozenset({5, 7, 10}) in sets
    assert any(17 in s and len(s) == 11 for s in sets)


def test_3n_plus_5_has_nontrivial_cycles():
    cs = find_cycles(d=5, max_len=8, include_negative=False)
    assert any(19 in set(c) for c in cs)


def test_convergents_of_log2_3():
    convs = log2_3_convergents()
    assert (2, 1) in convs and (3, 2) in convs and (8, 5) in convs
    assert (19, 12) in convs and (65, 41) in convs
    # certificado exato de alternância
    for i, (p, q) in enumerate(convs[:10]):
        above = (1 << p) > 3 ** q
        assert above == (i % 2 == 1)


def test_exclusion_bound_grows_with_N():
    b1 = cycle_exclusion_bound(10 ** 6)
    b2 = cycle_exclusion_bound(2 ** 71)
    assert b1["min_odd_steps"] >= 10          # já exclui ciclos curtos
    assert b2["min_odd_steps"] > b1["min_odd_steps"]
    assert b2["min_odd_steps"] > 10 ** 9      # bilhões de passos ímpares

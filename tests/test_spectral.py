from fractions import Fraction

from collatz.spectral import (spectral_gap, stationary_distribution,
                              stationary_exact, stationary_uniform_check,
                              syracuse_transfer_matrix)


def test_rows_sum_to_one_exactly():
    states, P = syracuse_transfer_matrix(2)
    for r in states:
        assert sum(P[r].values()) == Fraction(1)


def test_uniform_is_NOT_stationary():
    # achado estrutural: a medida invariante da cadeia de Syracuse não é
    # a uniforme — mod 3 ela é (1/3, 2/3)
    assert not stationary_uniform_check(1)
    pi = stationary_exact(1)
    assert pi == {1: Fraction(1, 3), 2: Fraction(2, 3)}


def test_stationary_exact_is_stationary():
    for k in (1, 2):
        states, P = syracuse_transfer_matrix(k)
        pi = stationary_exact(k)
        assert sum(pi.values()) == 1
        new = {s: Fraction(0) for s in states}
        for r in states:
            for s, w in P[r].items():
                new[s] += pi[r] * w
        assert new == pi


def test_power_iteration_agrees_with_exact():
    k = 2
    pi_f = stationary_distribution(k)
    pi_e = stationary_exact(k)
    assert all(abs(pi_f[r] - float(pi_e[r])) < 1e-9 for r in pi_f)


def test_gap_is_nontrivial():
    lam2 = spectral_gap(2)
    assert 0.0 <= lam2 < 0.99   # cadeia mistura: |lambda_2| < 1


def test_memory_loss_rank_collapse():
    from collatz.spectral import memory_loss_check
    for k in (1, 2, 3):
        assert memory_loss_check(k)

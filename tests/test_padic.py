import math

from collatz.padic import (bad_set_measure, census_is_binomial,
                           parity_census, shift_conjugacy_check,
                           terras_bijection_check)


def test_terras_bijection():
    for k in (1, 4, 8, 12):
        assert terras_bijection_check(k)


def test_shift_conjugacy():
    assert shift_conjugacy_check(10)


def test_census_binomial():
    for k in (4, 8, 12):
        assert census_is_binomial(parity_census(k), k)


def test_bad_set_decays():
    m8, _ = bad_set_measure(8)
    m16, r16 = bad_set_measure(16)
    assert m16 < m8 < 0.5
    # mesma ordem de grandeza da taxa de grandes desvios
    assert 0.1 < m16 / r16 < 10

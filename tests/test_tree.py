from collatz.tree import (coverage_density, growth_rate, inverse_children,
                          inverse_tree, missing_below)


def test_inverse_children():
    assert inverse_children(2) == [4, 1]
    assert inverse_children(5) == [10, 3]
    assert inverse_children(4) == [8]      # (8-1)/3 não é inteiro


def test_inverse_is_consistent_with_T():
    from collatz.core import T
    for m in range(1, 200):
        for c in inverse_children(m):
            assert T(c) == m


def test_coverage_grows_to_full():
    c1 = coverage_density(100, 20)
    c2 = coverage_density(100, 90)
    assert c2 >= c1
    assert c2 == 1.0                       # todos 1..100 alcançados


def test_missing_shrinks():
    assert missing_below(50, 80) == []


def test_growth_factor_near_4_3():
    rates = growth_rate(26)
    tail = rates[-5:]
    avg = sum(tail) / len(tail)
    assert 1.15 < avg < 1.5

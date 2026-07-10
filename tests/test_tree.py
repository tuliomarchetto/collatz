from collatz.tree import (coverage_density, empirical_bounds, growth_rate,
                          inverse_children, inverse_tree, missing_below,
                          required_depth)


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


def test_required_depth_small_x():
    """required_depth(X) deve ser o max total_stopping_time em 1..X.
    A árvore inversa a essa profundidade deve cobrir todo 1..X."""
    d = required_depth(50)
    assert isinstance(d, int) and d > 0
    # a árvore inversa à profundidade exata deve cobrir 1..50
    assert coverage_density(50, d) == 1.0


def test_required_depth_consistency():
    """required_depth é monotonamente crescente."""
    d1 = required_depth(20)
    d2 = required_depth(100)
    assert d2 >= d1


def test_empirical_bounds_structure():
    """Cada nível da árvore inversa deve ter min <= max, e o nível 0 é (1,2)."""
    bounds = empirical_bounds(15)
    assert bounds[0] == (1, 2)
    for lo, hi in bounds[1:]:
        if lo == 0 and hi == 0:
            break  # árvore terminou antes
        assert lo > 0
        assert lo <= hi


def test_empirical_bounds_max_is_power_of_2():
    """O max de cada nível deve ser 2^k (ramo par dobra sempre)."""
    bounds = empirical_bounds(10)
    # nível 0: (1,2) = 2^1; nível 1: max=4=2^2; etc.
    for i, (lo, hi) in enumerate(bounds):
        if lo == 0:
            break
        assert hi & (hi - 1) == 0, f"nível {i}: max {hi} não é potência de 2"


from collatz.tree import (
    coverage_density,
    empirical_bounds,
    growth_rate,
    inverse_children,
    missing_below,
    required_depth,
)


def test_inverse_children():
    assert inverse_children(2) == [4, 1]
    assert inverse_children(5) == [10, 3]
    assert inverse_children(4) == [8]  # (8-1)/3 is not an integer


def test_inverse_is_consistent_with_T():
    from collatz.core import T

    for m in range(1, 200):
        for c in inverse_children(m):
            assert T(c) == m


def test_coverage_grows_to_full():
    c1 = coverage_density(100, 20)
    c2 = coverage_density(100, 90)
    assert c2 >= c1
    assert c2 == 1.0  # all of 1..100 reached


def test_missing_shrinks():
    assert missing_below(50, 80) == []


def test_growth_factor_near_4_3():
    rates = growth_rate(26)
    tail = rates[-5:]
    avg = sum(tail) / len(tail)
    assert 1.15 < avg < 1.5


def test_required_depth_small_x():
    """required_depth(X) must be the max total_stopping_time over 1..X.
    The inverse tree at that depth must cover all of 1..X."""
    d = required_depth(50)
    assert isinstance(d, int) and d > 0
    # the inverse tree at the exact depth must cover 1..50
    assert coverage_density(50, d) == 1.0


def test_required_depth_consistency():
    """required_depth is monotonically increasing."""
    d1 = required_depth(20)
    d2 = required_depth(100)
    assert d2 >= d1


def test_empirical_bounds_structure():
    """Each level of the inverse tree must have min <= max, and level 0 is (1,2)."""
    bounds = empirical_bounds(15)
    assert bounds[0] == (1, 2)
    for lo, hi in bounds[1:]:
        if lo == 0 and hi == 0:
            break  # tree ended earlier
        assert lo > 0
        assert lo <= hi


def test_empirical_bounds_max_is_power_of_2():
    """The max of each level must be 2^k (the even branch always doubles)."""
    bounds = empirical_bounds(10)
    # level 0: (1,2) = 2^1; level 1: max=4=2^2; etc.
    for i, (lo, hi) in enumerate(bounds):
        if lo == 0:
            break
        assert hi & (hi - 1) == 0, f"level {i}: max {hi} is not a power of 2"

import math

from collatz.invariants import (
    conserved_partition,
    drift_by_class,
    induced_map_exists,
    induced_map_search,
    karp_max_mean_cycle,
    lyapunov_verdict,
    transient_classes,
)


def test_induced_maps_are_2adic():
    assert induced_map_exists(4, 2)
    assert not induced_map_exists(2, 2)
    assert not induced_map_exists(3, 3)
    for m2, m1 in induced_map_search(12):
        assert m1 == 2 * m2


def test_transient_mod3():
    assert transient_classes(3) == {0}
    assert 0 in transient_classes(9)


def test_conserved_partition_mod8_refines_fully():
    blocks = conserved_partition(8)
    assert all(len(b) == 1 for b in blocks)  # no hidden discrete invariant


def test_karp_finds_minus_one_obstruction():
    mean, cyc = karp_max_mean_cycle(7)
    assert abs(mean - (math.log2(3) - 1)) < 1e-9
    assert cyc == [127] or set(cyc) == {127}  # residue -1 mod 2^7


def test_lyapunov_impossible():
    v = lyapunov_verdict(6)
    assert v["lyapunov_possible"] is False
    assert -1 in v["cycle_as_signed"]


def test_drift_negative_at_depth():
    dr = drift_by_class(2, depth=12)
    # global mean drift = log2(3)/2 - 1 per step, times 12 steps
    expected = 12 * (math.log2(3) / 2 - 1)
    mean = sum(dr.values()) / len(dr)
    assert abs(mean - expected) < 1e-9
    assert all(v < 0 for v in dr.values())

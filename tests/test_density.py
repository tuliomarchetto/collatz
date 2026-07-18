"""Tests for collatz.density (G11 laboratory hooks)."""

from fractions import Fraction

from collatz import density, padic


def test_bad_set_measure_exact_matches_float_padic():
    for k in (1, 4, 8, 10):
        meas, n_bad, total = density.bad_set_measure_exact(k)
        assert total == 1 << k
        assert 0 <= n_bad <= total
        assert meas == Fraction(n_bad, total)
        float_meas, _ = padic.bad_set_measure(k)
        assert abs(float(meas) - float_meas) < 1e-12


def test_bad_set_envelope_decays():
    """Terras: bad-set measure → 0 (envelope); oscillates within dyadic bands."""
    m8, _, _ = density.bad_set_measure_exact(8)
    m16, _, _ = density.bad_set_measure_exact(16)
    m20, _, _ = density.bad_set_measure_exact(20)
    # Envelope decays: larger k sits below the early peak at k=1.
    assert m16 < m8
    assert m20 < Fraction(1, 4)
    assert m16 < Fraction(1, 5)


def test_bad_set_threshold_certified():
    for k in range(1, 12):
        j = density.bad_set_threshold(k)
        assert 3**j >= 2**k
        if j > 0:
            assert 3 ** (j - 1) < 2**k


def test_harmonic_and_log_density_partial():
    assert density.harmonic_partial(1) == 1
    assert density.harmonic_partial(2) == Fraction(3, 2)
    # Finite set {2, 4} up to n=4: (1/2 + 1/4) / H_4
    H4 = density.harmonic_partial(4)
    got = density.log_density_partial([2, 4], 4)
    assert got == (Fraction(1, 2) + Fraction(1, 4)) / H4


def test_residue_class_log_density_partial_evens():
    # Partial log-density of evens up to 10 is positive and < 1.
    d = density.residue_class_log_density_partial(0, 2, 10)
    assert 0 < d < 1


def test_empirical_probe_structure():
    probe = density.empirical_long_stopping_log_density(200, bound=20)
    assert probe.limit == 200
    assert probe.bound == 20
    assert probe.n_exceed >= 0
    assert 0.0 <= probe.empirical_log_density <= 1.0
    assert "empirical" in probe.note.lower()


def test_interface_map_nonempty():
    m = density.interface_map()
    assert "Tao almost-bounded Col_min for every f→∞" in m
    assert "NOT implemented" in m["Tao almost-bounded Col_min for every f→∞"]

from fractions import Fraction

from collatz.transfer import (absorption_profile, finite_section_nilpotency,
                              haar_mixing_check_2adic,
                              inverse_branches_check_2adic,
                              koopman_decay_profile, power_weight_obstruction,
                              stationary_projective_check,
                              syracuse_branch_contraction_check,
                              syracuse_w1_coefficient,
                              transfer_2adic_matrix,
                              transfer_2adic_w1_coefficient,
                              wasserstein_padic)


def test_wasserstein_point_masses():
    one = Fraction(1)
    # mesmas medidas -> 0
    assert wasserstein_padic({4: one}, {4: one}, 3, 2) == 0
    # x=1, y=2 diferem mod 3 (v=0): distância 1
    assert wasserstein_padic({1: one}, {2: one}, 3, 2) == 1
    # x=1, y=4 congruentes mod 3, diferem mod 9 (v=1): distância 1/3
    assert wasserstein_padic({1: one}, {4: one}, 3, 2) == Fraction(1, 3)


def test_syracuse_branches_contract_by_exactly_one_third():
    assert syracuse_branch_contraction_check(3)


def test_syracuse_w1_coefficient_below_one_third_and_sharpening():
    # cota uniforme tau_k <= 1/3 (a lacuna espectral do operador infinito),
    # com valores exatos crescendo para 1/3
    c2, _ = syracuse_w1_coefficient(2)
    c3, _ = syracuse_w1_coefficient(3)
    assert c2 == Fraction(5, 21)
    assert c3 == Fraction(455, 1387)
    assert c2 < c3 <= Fraction(1, 3)


def test_stationary_measures_are_projective():
    # pi_k projeta em pi_{k-1}: os pi_k são os cilindros de UMA medida em Z_3
    for k in (2, 3):
        assert stationary_projective_check(k)


def test_koopman_decay_and_finite_time_equidistribution():
    prof = koopman_decay_profile(3)
    assert prof["decay"]                # dev_n <= Lip(f)/3^n
    assert prof["finite_time"]          # U^k f = pi(f) EXATAMENTE
    assert prof["devs"][-1] == 0


def test_inverse_branches_2adic():
    assert inverse_branches_check_2adic(5)


def test_transfer_2adic_doubly_stochastic():
    k = 5
    P = transfer_2adic_matrix(k)
    col = {y: Fraction(0) for y in range(1 << k)}
    for x, row in P.items():
        assert sum(row.values()) == 1
        for y, w in row.items():
            col[y] += w
    assert all(c == 1 for c in col.values())   # Haar é invariante


def test_transfer_2adic_w1_coefficient_is_exactly_one_half():
    for k in (2, 3, 5):
        c, _ = transfer_2adic_w1_coefficient(k)
        assert c == Fraction(1, 2)


def test_haar_mixing_in_finite_time():
    assert haar_mixing_check_2adic(5)


def test_finite_section_is_nilpotent_for_collatz():
    r = finite_section_nilpotency(5000)
    assert r["acyclic"]
    assert r["cycle"] is None
    assert r["index"] > 0
    # o índice cresce ~ c log N
    r2 = finite_section_nilpotency(50_000)
    assert r2["acyclic"] and r2["index"] > r["index"]


def test_finite_section_detects_cycle_in_3n_minus_1():
    # validação do detector no sistema irmão: espectro NÃO trivial
    r = finite_section_nilpotency(1000, d=-1)
    assert not r["acyclic"]
    assert r["cycle"] == [5, 7, 10]


def test_power_weight_obstruction_witness():
    for t in (3, 5, 8):
        w = power_weight_obstruction(t)
        assert w["all_odd"]
        assert w["ratio_matches_formula"]
        assert w["ratio"] == Fraction(3 ** t - 1, 2 ** t - 1) > 1


def test_absorption_profile_decays():
    ap = absorption_profile(5000)
    m = ap["profile"]
    ts = sorted(m)
    assert m[ts[0]] >= m[ts[-1]]
    assert ap["rate"] is None or 0 < ap["rate"] < 1
    assert 0.96 < ap["reference_rate"] < 0.97

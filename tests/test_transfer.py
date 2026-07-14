from fractions import Fraction

from collatz.spectral import memory_loss_check, syracuse_transfer_matrix
from collatz.transfer import (
    absorption_profile,
    finite_section_nilpotency,
    haar_mixing_check_2adic,
    inverse_branches_check_2adic,
    koopman_decay_profile,
    power_weight_obstruction,
    stationary_projective_check,
    syracuse_branch_contraction_check,
    syracuse_kernel_projective_check,
    syracuse_w1_coefficient,
    transfer_2adic_matrix,
    transfer_2adic_w1_coefficient,
    wasserstein_padic,
)


def test_wasserstein_point_masses():
    one = Fraction(1)
    # same measures -> 0
    assert wasserstein_padic({4: one}, {4: one}, 3, 2) == 0
    # x=1, y=2 differ mod 3 (v=0): distance 1
    assert wasserstein_padic({1: one}, {2: one}, 3, 2) == 1
    # x=1, y=4 congruent mod 3, differ mod 9 (v=1): distance 1/3
    assert wasserstein_padic({1: one}, {4: one}, 3, 2) == Fraction(1, 3)


def test_syracuse_branches_contract_by_exactly_one_third():
    assert syracuse_branch_contraction_check(3)


def test_syracuse_w1_coefficient_below_one_third_and_sharpening():
    # uniform bound tau_k <= 1/3 (the spectral gap of the infinite operator),
    # with exact values increasing toward 1/3
    c2, _ = syracuse_w1_coefficient(2)
    c3, _ = syracuse_w1_coefficient(3)
    assert c2 == Fraction(5, 21)
    assert c3 == Fraction(455, 1387)
    assert c2 < c3 <= Fraction(1, 3)


def test_syracuse_kernel_projective_check():
    # P_k is EXACTLY the pushforward of P_{k+1} under reduction mod 3^k
    assert syracuse_kernel_projective_check(2)
    assert syracuse_kernel_projective_check(3)
    assert syracuse_kernel_projective_check(4)


def test_tau_k_is_provably_nondecreasing():
    # Corollary of syracuse_kernel_projective_check (pushforward under a
    # 1-Lipschitz map cannot increase W1): tau_k <= tau_{k+1} for all k.
    taus = [syracuse_w1_coefficient(k)[0] for k in range(2, 6)]
    assert taus == sorted(taus)
    assert all(t <= Fraction(1, 3) for t in taus)


def test_finest_resolution_pairs_have_exactly_zero_w1_cost():
    # Direct consequence of spectral.memory_loss_check: P_k(r,.) depends
    # only on r mod 3^{k-1}, so pairs at the finest resolution
    # v_3(r-s) = k-1 have IDENTICAL transition laws, hence W1 = 0. This
    # is why the maximizing pair of tau_k can never sit at that finest
    # resolution (it is observed at v_3 = k-2 instead, see
    # todo/tau_k_data.csv).
    for k in (2, 3, 4):
        assert memory_loss_check(k)
        states, P = syracuse_transfer_matrix(k)
        step = 3 ** (k - 1)
        M = 3**k
        for r in states:
            s = (r + step) % M
            if s % 3 != 0:
                assert wasserstein_padic(P[r], P[s], 3, k) == 0


def test_stationary_measures_are_projective():
    # pi_k projects onto pi_{k-1}: the pi_k are the cylinders of A SINGLE measure on Z_3
    for k in (2, 3):
        assert stationary_projective_check(k)


def test_koopman_decay_and_finite_time_equidistribution():
    prof = koopman_decay_profile(3)
    assert prof["decay"]  # dev_n <= Lip(f)/3^n
    assert prof["finite_time"]  # U^k f = pi(f) EXACTLY
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
    assert all(c == 1 for c in col.values())  # Haar is invariant


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
    # the index grows ~ c log N
    r2 = finite_section_nilpotency(50_000)
    assert r2["acyclic"] and r2["index"] > r["index"]


def test_finite_section_detects_cycle_in_3n_minus_1():
    # detector validation on the sibling system: NON-trivial spectrum
    r = finite_section_nilpotency(1000, d=-1)
    assert not r["acyclic"]
    assert r["cycle"] == [5, 7, 10]


def test_power_weight_obstruction_witness():
    for t in (3, 5, 8):
        w = power_weight_obstruction(t)
        assert w["all_odd"]
        assert w["ratio_matches_formula"]
        assert w["ratio"] == Fraction(3**t - 1, 2**t - 1) > 1


def test_absorption_profile_decays():
    ap = absorption_profile(5000)
    m = ap["profile"]
    ts = sorted(m)
    assert m[ts[0]] >= m[ts[-1]]
    assert ap["rate"] is None or 0 < ap["rate"] < 1
    assert 0.96 < ap["reference_rate"] < 0.97

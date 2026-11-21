"""Regression tests for mathematical certificate scope and exact residuals."""
import pytest

from collatz import stopping


def test_false_unrestricted_iff_is_not_a_certificate():
    with pytest.raises(NotImplementedError, match="non-strict"):
        stopping.unrestricted_potential_exists_iff_no_cycles()


def test_cylinder_descent_uses_affine_residual_not_only_coefficient():
    # Seed 1 has prefix 10: coefficient 3/4 contracts, but endpoint 1
    # only equals its seed. Seed 5 in the same cylinder descends to 4.
    certificate = stopping.cylinder_descent_certificate((1, 0))
    assert certificate["residue"] == 1
    assert certificate["modulus"] == 4
    assert certificate["affine_constant"] == 1
    assert certificate["coefficient_contracts"] is True
    assert certificate["all_positive_seeds_descend_nonstrictly"] is True
    assert certificate["all_positive_seeds_descend_strictly"] is False
    assert certificate["first_strict_descent_seed"] == 5


def test_cylinder_certificates_against_independent_forward_iteration():
    from itertools import product
    from collatz.core import T, parity_vector

    for length in range(1, 8):
        for word in product((0, 1), repeat=length):
            cert = stopping.cylinder_descent_certificate(word)
            modulus = 2 ** length
            first = next(n for n in range(1, modulus + 1)
                         if parity_vector(n, length) == word)
            assert cert["smallest_positive_seed"] == first
            for n in (first, first + modulus, first + 4 * modulus):
                endpoint = n
                for _ in word:
                    endpoint = T(endpoint)
                assert endpoint * modulus == cert["multiplier"] * n + cert["affine_constant"]
                for strict, key in ((False, "first_nonstrict_descent_seed"),
                                    (True, "first_strict_descent_seed")):
                    threshold = cert[key]
                    assert (threshold is not None and n >= threshold) == (
                        endpoint < n if strict else endpoint <= n
                    )


@pytest.mark.parametrize("word", [(), (2,), (-1, 0)])
def test_cylinder_certificate_rejects_invalid_words(word):
    with pytest.raises(ValueError, match="binary"):
        stopping.cylinder_descent_certificate(word)


def test_odd_to_even_witness_is_a_real_block_gain():
    from fractions import Fraction
    # Corrected walk definition must include these terminal even vertices.
    for j in range(1, 8):
        seed = 2 ** (2 * j) - 1
        endpoint = stopping.iterate_T(seed, 2 * j + 1)
        assert endpoint == (3 ** (2 * j) - 1) // 2
        assert endpoint % 2 == 0
        assert Fraction(endpoint, seed) > Fraction(3, 2) ** (2 * j) / 2


def test_block_gamma_certificate_checks_exact_boundary():
    equal = stopping.block_gamma_certificate(3, 1, 0)
    assert equal["endpoint"] == 5
    assert equal["certified_gamma_ge_W"] is True
    assert stopping.block_gamma_certificate(3, 1, 1)["certified_gamma_ge_W"] is False
    assert stopping.block_gamma_certificate(3, 0, 0)["expands"] is False
    for args in ((0, 1, 0), (3, -1, 0), (3, 1, -1)):
        with pytest.raises(ValueError):
            stopping.block_gamma_certificate(*args)


def test_coefficient_budget_exhaustion_is_unresolved_not_counterexample():
    assert stopping.coefficient_stopping_time(3, cap=1) is None
    assert stopping.coefficient_block_map(3, cap=1) is None
    result = stopping.kappa_walk_gain_nonpositive(3, cap=1)
    assert result["all_blocks_contracting"] is False
    assert result["violation"]["reason"] == "kappa not reached within cap"


@pytest.mark.parametrize("arguments, marker", [
    (["density", "--bad-set", "4"], "exact terras bad-set"),
    (["stopping", "--rule", "coefficient", "--depth", "3"], "coefficient"),
])
def test_research_cli_routes_execute(arguments, marker):
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "-m", "collatz", *arguments],
                            capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert marker in result.stdout.lower()

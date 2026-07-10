from collatz.symmetries import (
    affine_conjugacy_search,
    modular_affine_automorphisms,
    semiconjugacy_multiples,
)


def test_negation_conjugates_3n1_and_3nm1():
    found = affine_conjugacy_search(1, -1, max_a=3, max_b=5)
    assert (-1, 0) in found


def test_scaling_selfsimilarity():
    assert semiconjugacy_multiples(5)
    assert semiconjugacy_multiples(7)
    # and as an affine conjugacy 3n+1 -> 3n+5 with phi(x) = 5x
    found = affine_conjugacy_search(1, 5, max_a=6, max_b=3)
    assert (5, 0) in found


def test_identity_is_automorphism():
    autos = modular_affine_automorphisms(8)
    assert (1, 0) in autos

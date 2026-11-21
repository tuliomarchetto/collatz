"""Regression tests for verified core and density audit findings."""

from fractions import Fraction

import pytest

from collatz.core import total_stopping_time, trajectory
from collatz.density import (
    log_density_partial,
    residue_class_log_density_partial,
    stopping_time_to_one,
)


@pytest.mark.parametrize("seed, budget", [(2, 1), (4, 2), (1, 0)])
def test_total_stopping_time_includes_budget_endpoint(seed, budget):
    assert total_stopping_time(seed, max_steps=budget) == budget
    if seed != 1:
        assert total_stopping_time(seed, max_steps=budget - 1) == -1


@pytest.mark.parametrize("seed, budget", [(2, 1), (4, 2), (1, 0)])
def test_stopping_time_to_one_includes_budget_endpoint(seed, budget):
    assert stopping_time_to_one(seed, max_steps=budget) == budget
    if seed != 1:
        assert stopping_time_to_one(seed, max_steps=budget - 1) is None


@pytest.mark.parametrize("residue", [-5, -2, 4, 7])
def test_residue_density_normalizes_equivalent_representatives(residue):
    # Up to 4, the class 1 modulo 3 is {1, 4}, and H_4 = 25/12.
    assert residue_class_log_density_partial(residue, 3, 4) == Fraction(3, 5)


def test_log_density_counts_each_set_member_once():
    assert log_density_partial([1, 1, 2, 2, 0, -1, 3], 2) == Fraction(1)


@pytest.mark.parametrize(
    "seed, accelerated, expected",
    [
        (20, True, [20, 10, 5, 7, 10]),
        (40, False, [40, 20, 10, 5, 14, 7, 20]),
    ],
)
def test_trajectory_stops_at_first_repeat_after_transient(seed, accelerated, expected):
    assert trajectory(seed, d=-1, max_steps=20, accelerated=accelerated) == expected
    assert trajectory(seed, d=-1, max_steps=2, accelerated=accelerated) == expected[:3]

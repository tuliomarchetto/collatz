"""Reproduce candidate correctness issues exposed during the coverage review.

This audit intentionally reports discrepancies without changing research code.
"""
import json
from fractions import Fraction
from collatz.core import total_stopping_time, trajectory
from collatz.density import residue_class_log_density_partial, log_density_partial, stopping_time_to_one

findings = []
def record(label, actual, expected):
    findings.append({"case": label, "actual": str(actual), "expected": str(expected), "matches_contract": actual == expected})

record("2 reaches 1 in exactly one allowed accelerated step (core)", total_stopping_time(2, max_steps=1), 1)
record("2 reaches 1 in exactly one allowed accelerated step (density)", stopping_time_to_one(2, max_steps=1), 1)
record("seed 1 requires zero steps, with zero budget (core)", total_stopping_time(1, max_steps=0), 0)
record("seed 1 requires zero steps, with zero budget (density)", stopping_time_to_one(1, max_steps=0), 0)
for residue in (-1, 2, 5):
    expected = log_density_partial([n for n in range(1, 11) if n % 3 == residue % 3], 10)
    record(f"residue {residue} mod 3 up to 10", residue_class_log_density_partial(residue, 3, 10), expected)
record("set density should not depend on duplicate enumeration", log_density_partial([1, 1], 1), Fraction(1))
path = trajectory(10, d=-1, max_steps=8)
record("trajectory contract stops on a locally repeated value (10 enters 7,10,5 cycle)", path, [10, 5, 7, 10])
# A seed outside the eventual cycle distinguishes seed-return from general repeat detection.
path = trajectory(20, d=-1, max_steps=8)
record("trajectory stops at first repeat after entering a cycle from seed 20", path, [20, 10, 5, 7, 10])
print(json.dumps(findings, indent=2))

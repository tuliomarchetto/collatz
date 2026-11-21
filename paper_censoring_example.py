"""Reproduce the finite-budget censoring example discussed in the paper.

The probe includes unresolved seeds. This script records an upper-envelope
measurement, not an exact exceedance count or asymptotic density theorem.
"""
import json
from collatz.density import empirical_long_stopping_log_density, stopping_time_to_one

short = empirical_long_stopping_log_density(3, 100, max_steps=1)
resolved = empirical_long_stopping_log_density(3, 100, max_steps=10)
assert stopping_time_to_one(3, max_steps=10) == 5
assert short.n_exceed == 1
assert resolved.n_exceed == 0
print(json.dumps({
    "seed": 3, "threshold": 100, "actual_total_stopping_time": 5,
    "short_budget": 1, "short_budget_inclusive_count": short.n_exceed,
    "resolved_budget": 10, "resolved_exceedance_count": resolved.n_exceed,
    "interpretation": "short-budget result includes unresolved seeds; not exact exceedance"
}, indent=2))

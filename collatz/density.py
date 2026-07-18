"""
Almost-all / logarithmic-density laboratory hooks (Tier 3 G11).

This module does NOT claim progress on the Collatz conjecture. It records
the finite, exact-arithmetic shadows of the almost-all apparatus that the
field actually uses:

* Terras (1976): natural-density almost-all finite stopping time, via the
  exact 2-adic bad-set measure (residue classes mod 2^k that still grow
  after k accelerated steps).
* Korec (1994): Col_min(N) ≤ N^θ for almost all N (natural density), any
  θ > log 3 / log 4.
* Tao (Forum Math. Pi 2022, arXiv:1909.03562): Col_min(N) ≤ f(N) for every
  f → ∞, for almost all N in the sense of *logarithmic* density.

What this module computes exactly (rationals / integers only for certified
claims; floats only as display):

1. Exact rational bad-set measure mod 2^k (Terras; already in padic.py,
   re-exported with a rational certificate).
2. Exact partial logarithmic-density sums for finite sets of residues —
   the discrete ingredient of log-density bookkeeping.
3. Finite-horizon empirical log-density of seeds whose stopping time
   exceeds a bound — an *empirical probe*, never a proof.

See todo/G11_PROGRAM.md for the research-program scope and the explicit
fence: none of this folds into the current manuscript's claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from . import padic
from .core import T


# ---------------------------------------------------------------------------
# 1. Exact Terras bad-set (rational)
# ---------------------------------------------------------------------------


def bad_set_measure_exact(k: int) -> Tuple[Fraction, int, int]:
    """Exact rational measure of the Terras bad set mod 2^k.

    A residue class n mod 2^k is *bad* when after k accelerated steps the
    growth factor satisfies 3^{#odds} ≥ 2^k (orbit has not yet dropped in
    log-scale). By Terras's bijection the parity census is exactly
    Binomial(k, ·), so the measure is
        (# of parity words with 3^{wt} ≥ 2^k) / 2^k
    as an exact Fraction.

    Returns (measure, n_bad, 2^k).
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    if k == 0:
        return Fraction(0), 0, 1
    # Integer comparison 3^j ≥ 2^k ⇔ j * log 3 ≥ k * log 2, certified by
    # comparing powers (exact).
    census = padic.parity_census(k)
    bad = 0
    for j, c in census.items():
        if 3**j >= 2**k:
            bad += c
    total = 1 << k
    return Fraction(bad, total), bad, total


def bad_set_threshold(k: int) -> int:
    """Least j such that 3^j ≥ 2^k (exact integer search)."""
    j = 0
    p3 = 1
    while p3 < (1 << k):
        j += 1
        p3 *= 3
    return j


def bad_set_table(max_k: int) -> List[Dict[str, object]]:
    """Exact bad-set measures for k = 1..max_k, for laboratory display."""
    rows: List[Dict[str, object]] = []
    for k in range(1, max_k + 1):
        meas, n_bad, total = bad_set_measure_exact(k)
        rows.append(
            {
                "k": k,
                "measure": meas,
                "n_bad": n_bad,
                "total": total,
                "threshold_j": bad_set_threshold(k),
                "measure_float": float(meas),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# 2. Logarithmic-density bookkeeping (exact partial sums)
# ---------------------------------------------------------------------------


def harmonic_partial(n: int) -> Fraction:
    """H_n = sum_{k=1}^n 1/k as an exact rational (for small n only)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    s = Fraction(0)
    for k in range(1, n + 1):
        s += Fraction(1, k)
    return s


def log_density_partial(members: Sequence[int], n: int) -> Fraction:
    """Partial logarithmic density of a set A up to n:
        (sum_{a ∈ A, 1 ≤ a ≤ n} 1/a) / H_n .

    Exact rational. For a finite A the limit as n→∞ is 0; this is only a
    finite-n probe. Tao (2022) uses log-density as the notion of 'almost
    all' for Col_min(N) ≤ f(N).
    """
    if n < 1:
        raise ValueError("n must be ≥ 1")
    num = Fraction(0)
    for a in members:
        if 1 <= a <= n:
            num += Fraction(1, a)
    return num / harmonic_partial(n)


def residue_class_log_density_partial(
    residue: int, modulus: int, n: int
) -> Fraction:
    """Partial log-density of { m : m ≡ residue (mod modulus) } up to n.

    As n→∞ this tends to 1/modulus (harmonic series on arithmetic
    progressions). Exact rational at finite n.
    """
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    members = range(residue if residue > 0 else modulus, n + 1, modulus)
    return log_density_partial(members, n)


# ---------------------------------------------------------------------------
# 3. Empirical stopping-time probes (float display; NOT certified claims)
# ---------------------------------------------------------------------------


@dataclass
class StoppingProbe:
    """Empirical log-density of seeds whose total stopping time ≥ bound.

    All fields derived from a finite ascending sieve; the log-density value
    is a float for display only and is labelled empirical.
    """

    limit: int
    bound: int
    n_exceed: int
    exceed_seeds: List[int]
    empirical_log_density: float  # display only
    note: str = (
        "empirical finite-n probe; NOT a proof of positive/zero log-density"
    )


def stopping_time_to_one(n: int, d: int = 1, max_steps: int = 1_000_000) -> Optional[int]:
    """Total accelerated steps from n down to 1, or None if max_steps hit."""
    x = n
    for s in range(max_steps):
        if x == 1:
            return s
        x = T(x, d)
    return None


def empirical_long_stopping_log_density(
    limit: int, bound: int, max_steps: int = 1_000_000
) -> StoppingProbe:
    """Among odd seeds 3..limit, those with stopping time ≥ bound; report
    the partial log-density of that finite set up to `limit`.

    This is a laboratory probe for the almost-all heuristics (Terras / Tao).
    It is *not* a substitute for Tao's theorem and must not be quoted as one.
    """
    if limit < 3 or bound < 1:
        raise ValueError("limit ≥ 3 and bound ≥ 1 required")
    exceed: List[int] = []
    for n in range(3, limit + 1, 2):
        st = stopping_time_to_one(n, max_steps=max_steps)
        if st is None or st >= bound:
            exceed.append(n)
    # Partial log-density as float for display (H_n via math.log is fine here:
    # the probe is explicitly empirical).
    if not exceed:
        emp = 0.0
    else:
        num = sum(1.0 / a for a in exceed)
        # H_n ≈ ln n + γ; use exact-ish sum for small limit
        H = sum(1.0 / k for k in range(1, limit + 1))
        emp = num / H
    return StoppingProbe(
        limit=limit,
        bound=bound,
        n_exceed=len(exceed),
        exceed_seeds=exceed[:50],  # cap stored seeds
        empirical_log_density=emp,
    )


# ---------------------------------------------------------------------------
# 4. Interface map: what the lab already has vs what Tao needs
# ---------------------------------------------------------------------------


def interface_map() -> Dict[str, str]:
    """Static map from almost-all ingredients to this repository.

    Returned for documentation / CLI; the prose lives in todo/G11_PROGRAM.md.
    """
    return {
        "Terras bad-set measure (natural density, finite k)": (
            "padic.bad_set_measure / density.bad_set_measure_exact — "
            "exact rational, certified"
        ),
        "Terras bijection / Bernoulli conjugacy": (
            "padic.terras_bijection_check, padic.shift_conjugacy_check — "
            "exact, finite k"
        ),
        "Syracuse transfer on Z/3^k Z and Z_3": (
            "transfer.py, spectral.py; paper thm:z3 / thm:tausharp — "
            "exact W1 contraction τ=1/3 (measure side, not pointwise)"
        ),
        "Logarithmic density (partial sums)": (
            "density.log_density_partial — exact rational at finite n; "
            "no limit theorems proved here"
        ),
        "Tao first-passage / skew walk on Z/3^n Z char. functions": (
            "NOT implemented — open research program (see G11_PROGRAM.md)"
        ),
        "Tao almost-bounded Col_min for every f→∞": (
            "NOT implemented — theorem of Tao 2022; out of scope for this "
            "laboratory's current submission"
        ),
        "Pointwise modular Lyapunov": (
            "obstructed by thm:main (Lean-formalized in lean/); "
            "the obstruction is why almost-all methods are the live frontier"
        ),
    }

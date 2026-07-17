#!/usr/bin/env python3
"""
Reproduce every number quoted in the manuscript (paper/main.tex) and in
the report (REPORT.md / RELATORIO.md, Part III).

Usage:
    python reproduce_paper_results.py           # full run (~1-2 min)
    python reproduce_paper_results.py --quick   # skip the slowest sections

Each section R1..R9 recomputes one block of results from scratch using
only the `collatz` package (pure standard-library Python, exact
arithmetic) and CHECKS the recomputed value against the number printed
in the paper. The script exits with status 0 only if every check
passes, so it doubles as a verification certificate in CI.

This script consolidates and replaces the exploratory scripts
`scratch.py`, `scratch2.py`, `scratch3.py` that preceded it.
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from fractions import Fraction

from collatz import (
    cycles,
    invariants,
    padic,
    search,
    spectral,
    stopping,
    symmetries,
    transfer,
    tree,
)

_failures: list[str] = []


def check(label: str, got, expected) -> None:
    """Compare a recomputed value against the value quoted in the paper."""
    ok = got == expected
    mark = "ok" if ok else "MISMATCH"
    print(f"    [{mark}] {label}: {got!r}" + ("" if ok else f"  (paper says {expected!r})"))
    if not ok:
        _failures.append(label)


def section(title: str):
    print(f"\n== {title}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quick", action="store_true",
                    help="skip the slowest sections (R1 sieve at 200k, tau_4)")
    args = ap.parse_args()
    t0 = time.time()

    # ------------------------------------------------------------------
    section("R1. Direct sieve: every n <= 200,000 converges to 1"
            " [paper Table 1; REPORT Part III, 'Global Computational Sieve']")
    limit = 20_000 if args.quick else 200_000
    res = search.verify_range(limit)
    check(f"all n <= {limit:,} converge (empirical, NOT a proof)", res.all_converge, True)
    n_rec, s_rec = res.stopping_records[-1]
    print(f"    stopping-time record (steps to drop below seed): n = {n_rec}, {s_rec} steps")
    if not args.quick:
        check("stopping-time record for n <= 200,000", (n_rec, s_rec), (35_655, 135))
        check("excursion record for n <= 200,000",
              res.excursion_records[-1], (159_487, 8_601_188_876))

    # ------------------------------------------------------------------
    section("R2. Exact cycle enumeration via parity vectors"
            " [paper Table 2; REPORT Part III, 'Analytical Discovery of Extended Cycles']")
    cs = cycles.find_cycles(d=1, max_len=14, include_negative=True)
    # Each cycle tuple starts at its element of least absolute value.
    check("3n+1 cycles of length <= 14 in Z (by least-|.| element)",
          sorted(c[0] for c in cs), [-17, -5, -1, 1])
    check("only positive 3n+1 cycle is the trivial {1,2}",
          sorted(c for c in cs if min(c) > 0), [(1, 2)])
    cs_m = cycles.find_cycles(d=-1, max_len=14, include_negative=False)
    check("3n-1 has nontrivial positive cycles (detector validation)",
          sorted(min(c) for c in cs_m), [1, 5, 17])
    cs_5 = cycles.find_cycles(d=5, max_len=14, include_negative=False)
    check("3n+5 has a cycle through 19 and 49",
          any(19 in c and 49 in c for c in cs_5), True)

    # ------------------------------------------------------------------
    section("R3. Diophantine cycle exclusion (continued fractions of log2 3)"
            " [paper Table 3; REPORT Part III, 'Exclusion via Diophantine Compression']")
    b = cycles.cycle_exclusion_bound(200_000)
    check("N = 200,000: any nontrivial cycle has > k odd steps, k =",
          b["min_odd_steps"], 428)
    check("N = 200,000: minimum cycle length (T steps)",
          b["min_length_T_steps"], 676)
    b71 = cycles.cycle_exclusion_bound(2 ** 71)
    check("N = 2^71 (published verification): minimum odd steps",
          b71["min_odd_steps"], 65_470_613_320)
    check("N = 2^71: minimum cycle elements (~103 billion)",
          b71["min_elements"], 103_443_569_045)

    # ------------------------------------------------------------------
    section("R4. Karp maximum mean cycle mod 2^j: the -1 obstruction"
            " [paper Table 4; REPORT Part III, 'Practical Identification of -1 mod 2^j']"
            "\n    (Numerical instantiation of the Main Theorem, which is proved analytically.)")
    for j in range(5, 11):
        v = invariants.lyapunov_verdict(j)
        mean = v["max_mean_log2_growth"]
        # Exact certificate: the extracted optimal cycle must consist solely
        # of odd residues, so its mean is exactly log2(3) - 1 (> 0 iff 3 > 2);
        # no cycle can exceed the maximum edge weight, which is log2(3) - 1.
        all_odd = all(r % 2 == 1 for r in v["cycle_residues"])
        check(f"j = {j}: optimal cycle is the all-odd class of -1 mod 2^{j}",
              (all_odd, v["cycle_as_signed"]), (True, [-1]))
        check(f"j = {j}: float mean agrees with log2(3) - 1 to 1e-12",
              abs(mean - (math.log2(3) - 1)) < 1e-12, True)
        check(f"j = {j}: no modular Lyapunov function exists",
              v["lyapunov_possible"], False)

    # ------------------------------------------------------------------
    section("R5. Inverse tree of 1: exact covering depth and level bounds"
            " [paper Table 5; REPORT Part III, 'Diffusion Balance (Inverse Tree)']"
            "\n    (Consolidates the former scratch.py / scratch2.py / scratch3.py experiments.)")
    # Forward computation: maximum total stopping time under T for n <= 1000
    # equals the depth of the deepest node in the tree rooted at 1.
    d1000 = tree.required_depth(1000)
    check("minimum inverse-tree depth (root 1) covering 1..1000", d1000, 113)
    # Cross-check by the independent inverse-tree BFS. inverse_tree() seeds
    # its level 0 with {1, 2} (skipping the trivial loop 1 -> 2 -> 1), so a
    # node with total stopping time s is reached after s - 1 BFS iterations:
    # coverage completes at iteration 112, not 111.
    reached, _ = tree.inverse_tree(d1000 - 1, cap=1_000_000)
    check("BFS covers all of 1..1000 after 112 iterations from {1, 2}",
          all(n in reached for n in range(1, 1001)), True)
    reached_shallow, _ = tree.inverse_tree(d1000 - 2, cap=1_000_000)
    check("111 iterations do NOT cover 1..1000 (witness: 871)",
          [n for n in range(1, 1001) if n not in reached_shallow], [871])
    eb = tree.empirical_bounds(30)
    check("new-node range at level 30 of the exact (unpruned) tree",
          eb[30], (123, 2147483648))

    # ------------------------------------------------------------------
    section("R6. Syracuse transfer operator mod 3^k: exact stationary measure"
            " [paper Table 6; REPORT Part III, 'Empirical Rank Collapse (3^k)']")
    pi = spectral.stationary_exact(1)
    check("stationary measure mod 3", pi, {1: Fraction(1, 3), 2: Fraction(2, 3)})
    check("uniform measure is NOT stationary (k = 2)",
          spectral.stationary_uniform_check(2), False)
    check("memory loss in exactly k steps (rank collapse, k = 3)",
          spectral.memory_loss_check(3), True)
    gap = spectral.spectral_gap(3)
    check("second eigenvalue is numerically 0 (|lambda_2| < 1e-9)", gap < 1e-9, True)

    # ------------------------------------------------------------------
    section("R7. Exact Wasserstein contraction coefficients"
            " [paper Table 7; REPORT Part III, 'Absolute Measures (tau_k Wasserstein)']")
    tau2, _ = transfer.syracuse_w1_coefficient(2)
    tau3, _ = transfer.syracuse_w1_coefficient(3)
    check("tau_2 (exact fraction)", tau2, Fraction(5, 21))
    check("tau_3 (exact fraction)", tau3, Fraction(455, 1387))
    # Closed form of Theorem 4.6 (thm:tausharp): tau_k = (1/3)(1-q^2)/(1+q+q^2),
    # q = 2^{-2*3^{k-2}}. The brute-force maxima above certify it independently.
    check("closed form matches brute force at k = 2",
          transfer.syracuse_tau_closed_form(2), tau2)
    check("closed form matches brute force at k = 3",
          transfer.syracuse_tau_closed_form(3), tau3)
    check("extremal sphere v_3 = k-2: every pair realizes the closed-form W1"
          " and rows coincide mod 3^{k-1} (k = 2, 3, 4)",
          all(transfer.syracuse_extremal_sphere_check(k) for k in (2, 3, 4)), True)
    check("gap 1/3 - tau_5 = q(1+2q)/(3(1+q+q^2)), q = 2^-54 (exact rational)",
          Fraction(1, 3) - transfer.syracuse_tau_closed_form(5),
          (lambda q: q * (1 + 2 * q) / (3 * (1 + q + q * q)))(Fraction(1, 2**54)))
    check("gap 1/3 - tau_k < 2^{-2*3^{k-2}} for k = 2..8",
          all(Fraction(1, 3) - transfer.syracuse_tau_closed_form(k)
              < Fraction(1, 2 ** (2 * 3 ** (k - 2))) for k in range(2, 9)), True)
    if not args.quick:
        tau4, _ = transfer.syracuse_w1_coefficient(4)
        check("tau_4 (exact fraction)", tau4, Fraction(7_635_497_415, 22_906_579_627))
        check("tau_4 ~ 0.33333206", f"{float(tau4):.8f}", "0.33333206")
        check("closed form matches brute force at k = 4",
              transfer.syracuse_tau_closed_form(4), tau4)
        check("extremal sphere check at k = 5",
              transfer.syracuse_extremal_sphere_check(5), True)
        check("tau_2 < tau_3 < tau_4 <= 1/3 (monotone ascent to the bound)",
              tau2 < tau3 < tau4 <= Fraction(1, 3), True)
    check("Syracuse branches contract Z_3 by exactly 1/3",
          transfer.syracuse_branch_contraction_check(3), True)
    c2, _ = transfer.transfer_2adic_w1_coefficient(6)
    check("2-adic transfer operator W1 coefficient (exactly 1/2)",
          c2, Fraction(1, 2))
    check("L^k f equals the exact Haar average on Z_2 (k = 6)",
          transfer.haar_mixing_check_2adic(6), True)
    check("stationary family pi_k is projective (k = 3)",
          transfer.stationary_projective_check(3), True)

    # ------------------------------------------------------------------
    section("R8. Structural cross-checks (Terras conjugacy, symmetries)"
            " [paper Sect. 7; REPORT Part I context]")
    check("parity vector is a bijection on Z/2^k (Terras, k = 14)",
          padic.terras_bijection_check(14), True)
    check("phi(x) = -x conjugates 3n+1 with 3n-1",
          (-1, 0) in symmetries.affine_conjugacy_search(1, -1), True)
    check("phi(x) = 5x embeds 3n+1 into 3n+5",
          symmetries.semiconjugacy_multiples(5), True)

    # ------------------------------------------------------------------
    section("R9. Variable-depth stopping-time potentials: the strengthened no-go"
            " [paper Theorem thm:stopping + Sect. sec:karp block graphs;"
            " REPORT Part I 'Variable-Depth' + Part III]"
            "\n    (Every rule below stops the all-ones parity word, hence lies in the"
            "\n    no-go class; the obstruction cycle is certified in exact integers.)")
    rules = [(f"constant depth {k}", stopping.constant_rule(k)) for k in (1, 2, 3)]
    rules += [(f"Syracuse renewal truncated at B = {b}", stopping.syracuse_rule(b))
              for b in (3, 4, 5, 6)]
    rules += [(f"Terras coefficient rule truncated at B = {b}",
               stopping.coefficient_rule(b)) for b in (3, 4, 5, 6)]
    for name, S in rules:
        check(f"{name}: rule is a finite maximal prefix code (exact Kraft sum)",
              stopping.is_maximal_prefix_code(S), True)
        s = stopping.sigma_at_minus_one(S)
        check(f"{name}: sigma(-1) is finite (all-ones stop word present)",
              s is not None, True)
        v = stopping.karp_block_verdict(S)
        # Exact certificate: the optimal block cycle is the all-ones self-loop
        # at -1 mod 2^m with A = L = sigma(-1) steps, and its total weight is
        # positive iff 3^A > 2^L -- an integer comparison, no floats trusted.
        check(f"{name}: Karp optimal cycle = all-ones self-loop at -1",
              (v["cycle_is_minus_one_loop"], v["cycle_all_odd"]), (True, True))
        check(f"{name}: cycle steps (A, L) = (s, s) with s = sigma(-1)",
              (v["cycle_odd_steps"], v["cycle_total_steps"]), (s, s))
        check(f"{name}: positivity certified exactly by 3^A > 2^L",
              v["certified_positive"], True)
        check(f"{name}: float mean/block agrees with s*(log2(3)-1) to 1e-12",
              abs(v["max_mean_per_block"] - s * (math.log2(3) - 1)) < 1e-12, True)
        check(f"{name}: no variable-depth potential exists for the rule",
              v["variable_depth_potential_possible"], False)
    # Effective telescoping witnesses quoted in the paper: explicit Mersenne
    # n = 2^ell - 1 defeating ANY correction w with oscillation < 10.
    for s_blk, ell_expected in ((1, 19), (2, 20), (3, 21)):
        wtn = stopping.telescoping_witness(s_blk, 10)
        check(f"telescoping witness for 1^{s_blk} rules, osc < 10: n = 2^ell - 1, ell =",
              (wtn["ell"], wtn["certified"]), (ell_expected, True))
    # Boundary of the theorem: the UNTRUNCATED Syracuse and coefficient rules
    # never stop the all-ones word (last bit is 1; 3^i > 2^i exactly), so they
    # escape the no-go -- and must: the descent claim for the untruncated
    # coefficient rule with w = 0 is Terras's coefficient stopping time
    # conjecture (open). Not a gap in the theorem, but its exact frontier.
    check("untruncated Syracuse rule: no all-ones stop word up to depth 10,000",
          stopping.predicate_never_stops_all_ones(stopping.syracuse_stop, 10_000), True)
    check("untruncated coefficient rule: no all-ones stop word up to depth 10,000",
          stopping.predicate_never_stops_all_ones(stopping.coefficient_stop, 10_000),
          True)

    # ------------------------------------------------------------------
    dt = time.time() - t0
    print(f"\n{'=' * 68}")
    if _failures:
        print(f"FAILED: {len(_failures)} value(s) do not match the paper:")
        for f in _failures:
            print("  -", f)
        print(f"(elapsed {dt:.1f}s)")
        return 1
    print(f"All quoted results reproduced exactly. (elapsed {dt:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
CLI for the Collatz laboratory.

Examples:
    python -m collatz all                      # full report
    python -m collatz verify --limit 1000000   # counterexample sieve
    python -m collatz cycles --d -1 --max-len 16
    python -m collatz exclude --limit-bits 71  # cycle exclusion (N = 2^71, Barina 2025)
    python -m collatz lyapunov --j 10
    python -m collatz stopping --rule coefficient --depth 6
    python -m collatz spectral --k 4
    python -m collatz transfer --k3 3 --k2 6 --n 100000
    python -m collatz tree --depth 120 --x 1000
    python -m collatz density --bad-set 16   # Terras bad-set (exact rational)
    python -m collatz density --interface   # almost-all ingredient map (G11)
"""

from __future__ import annotations

import argparse
import math
import sys

from . import (
    cycles,
    density,
    invariants,
    padic,
    report,
    search,
    spectral,
    stopping,
    transfer,
    tree,
)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="collatz",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("all", help="full report of findings")
    p.add_argument("--limit", type=int, default=10_000_000)
    p.add_argument("--cycle-len", type=int, default=14)
    p.add_argument("-o", "--output", help="save report to a file")

    p = sub.add_parser("verify", help="verification/counterexample sieve")
    p.add_argument("--limit", type=int, default=1_000_000)
    p.add_argument("--d", type=int, default=1)

    p = sub.add_parser("cycles", help="exact enumeration of cycles")
    p.add_argument("--d", type=int, default=1)
    p.add_argument("--max-len", type=int, default=16)
    p.add_argument("--positive-only", action="store_true")

    p = sub.add_parser("exclude", help="Diophantine exclusion of cycles")
    p.add_argument(
        "--limit-bits",
        type=int,
        default=71,
        help="assume every n <= 2^bits has been verified "
        "(71 = published record, Barina 2025)",
    )

    p = sub.add_parser("lyapunov", help="maximum mean cycle (Karp) mod 2^j")
    p.add_argument("--j", type=int, default=9)

    p = sub.add_parser(
        "stopping", help="variable-depth stopping-time potentials (block Karp)"
    )
    p.add_argument(
        "--rule",
        choices=["constant", "syracuse", "coefficient"],
        default="coefficient",
        help="adapted stopping rule (truncated at --depth)",
    )
    p.add_argument("--depth", type=int, default=6, help="depth / truncation horizon")
    p.add_argument(
        "--osc", type=int, default=10, help="oscillation bound for the witness"
    )

    p = sub.add_parser("spectral", help="transfer operator mod 3^k")
    p.add_argument("--k", type=int, default=3)

    p = sub.add_parser("transfer", help="infinite (p-adic) transfer operator")
    p.add_argument(
        "--k3", type=int, default=3, help="3^k level of the Syracuse chain section"
    )
    p.add_argument(
        "--k2", type=int, default=6, help="2^k level of the operator section on Z_2"
    )
    p.add_argument(
        "--n", type=int, default=100_000, help="[1,N] window of the section on Z_+"
    )

    p = sub.add_parser("tree", help="inverse tree: coverage/growth")
    p.add_argument("--depth", type=int, default=120)
    p.add_argument("--x", type=int, default=1000)

    p = sub.add_parser("terras", help="verification of the 2-adic structure")
    p.add_argument("--k", type=int, default=16)

    p = sub.add_parser(
        "density",
        help="almost-all / log-density laboratory hooks (G11; no new claims)",
    )
    p.add_argument(
        "--bad-set",
        type=int,
        metavar="K",
        help="print exact Terras bad-set measures for k = 1..K",
    )
    p.add_argument(
        "--log-probe",
        action="store_true",
        help="empirical log-density of long stopping times (display only)",
    )
    p.add_argument("--limit", type=int, default=5_000, help="probe limit (odd seeds)")
    p.add_argument(
        "--bound", type=int, default=40, help="stopping-time threshold for --log-probe"
    )
    p.add_argument(
        "--interface",
        action="store_true",
        help="print the map from almost-all ingredients to this repo",
    )

    args = ap.parse_args(argv)

    if args.cmd == "all":
        text = report.run_all(verify_limit=args.limit, cycle_len=args.cycle_len)
        print(text)
        if args.output:
            with open(args.output, "w") as fh:
                fh.write(text + "\n")
            print(f"\n[report saved to {args.output}]", file=sys.stderr)

    elif args.cmd == "verify":
        r = search.verify_range(args.limit, d=args.d)
        if r.all_converge:
            print(f"Every n <= {args.limit:,} converges (3n{args.d:+d}).")
            print("Stopping-time records:", r.stopping_records[-5:])
            print("Excursion records:", r.excursion_records[-3:])
        else:
            print(f"Candidate COUNTEREXAMPLE: n = {r.counterexample}")
            if r.cycle:
                print(f"Cycle: {r.cycle}")

    elif args.cmd == "cycles":
        cs = cycles.find_cycles(
            d=args.d, max_len=args.max_len, include_negative=not args.positive_only
        )
        print(
            f"{len(cs)} cycles of the system 3n{args.d:+d} with length <= {args.max_len}:"
        )
        for c in cs:
            print("  ", c)

    elif args.cmd == "exclude":
        b = cycles.cycle_exclusion_bound(2**args.limit_bits)
        print(f"Assuming every n <= 2^{args.limit_bits} converges:")
        print(f"  nontrivial cycles have > {b['min_odd_steps']:,} odd steps")
        print(f"  and > {b['min_length_T_steps']:,} elements.")

    elif args.cmd == "lyapunov":
        v = invariants.lyapunov_verdict(args.j)
        print(
            f"mod 2^{args.j}: maximum mean = {v['max_mean_log2_growth']:.6f} "
            f"(log2(3)-1 = {math.log2(3)-1:.6f})"
        )
        print(f"optimal cycle (signed): {v['cycle_as_signed']}")
        print("Is a modular Lyapunov function possible?", v["lyapunov_possible"])

    elif args.cmd == "stopping":
        builders = {
            "constant": stopping.constant_rule,
            "syracuse": stopping.syracuse_rule,
            "coefficient": stopping.coefficient_rule,
        }
        S = builders[args.rule](args.depth)
        v = stopping.karp_block_verdict(S)
        print(
            f"rule '{args.rule}' truncated at depth {args.depth}: "
            f"{v['rule_size']} stop words, sigma(-1) = {v['sigma_at_minus_one']}"
        )
        print(
            f"block Karp mod 2^{v['modulus_bits']}: max mean/block = "
            f"{v['max_mean_per_block']:.6f}; optimal cycle (signed) = "
            f"{v['cycle_as_signed']}"
        )
        print(
            f"exact certificate: A = {v['cycle_odd_steps']} odd steps, "
            f"L = {v['cycle_total_steps']} total steps, 3^A > 2^L: "
            f"{v['certified_positive']} (all-ones loop at -1: "
            f"{v['cycle_is_minus_one_loop']})"
        )
        print(
            "Is a variable-depth stopping-time potential possible?",
            v["variable_depth_potential_possible"],
        )
        s = v["sigma_at_minus_one"]
        if isinstance(s, int):
            wtn = stopping.telescoping_witness(s, args.osc)
            print(
                f"telescoping witness (osc < {args.osc}): n = 2^{wtn['ell']} - 1, "
                f"{wtn['blocks']} blocks of {s} steps, certified: {wtn['certified']}"
            )

    elif args.cmd == "spectral":
        print("uniform stationary (exact):", spectral.stationary_uniform_check(args.k))
        print(f"|lambda_2| ~ {spectral.spectral_gap(args.k):.6f}")

    elif args.cmd == "transfer":
        c3, arg3 = transfer.syracuse_w1_coefficient(args.k3)
        print(
            f"Z_3 (Syracuse), level 3^{args.k3}: exact W1 coefficient = "
            f"{c3} ≈ {float(c3):.8f} (uniform bound 1/3; extremal pair {arg3})"
        )
        print(
            "  branches contract by exactly 1/3:",
            transfer.syracuse_branch_contraction_check(min(args.k3, 4)),
        )
        print(
            "  projective family pi_k -> pi_{k-1}:",
            transfer.stationary_projective_check(args.k3),
        )
        prof = transfer.koopman_decay_profile(args.k3)
        print(
            f"  decay dev_n <= Lip/3^n: {prof['decay']}; "
            f"U^k f = pi(f) exact: {prof['finite_time']}"
        )
        c2, arg2 = transfer.transfer_2adic_w1_coefficient(args.k2)
        print(
            f"Z_2 (T's transfer operator), level 2^{args.k2}: exact W1 "
            f"coefficient = {c2} (extremal pair {arg2})"
        )
        print(
            "  inverse branches + 1/2 contraction:",
            transfer.inverse_branches_check_2adic(min(args.k2, 7)),
        )
        print(
            "  L^k f = exact Haar average:", transfer.haar_mixing_check_2adic(args.k2)
        )
        sec = transfer.finite_section_nilpotency(args.n)
        print(
            f"Z_+ (pushforward), section [1,{args.n:,}]: acyclic = {sec['acyclic']}, "
            f"nilpotency index = {sec['index']} "
            f"(~{sec['index'] / math.log(args.n):.1f}·ln N; witness {sec['witness']})"
        )
        w = transfer.power_weight_obstruction(8)
        print(
            f"  obstruction to n^theta weights: n = {w['n']} has 8 odd steps, "
            f"T^8(n)/n = {w['ratio']} ≈ {float(w['ratio']):.2f} > 1"
        )
        abs_prof = transfer.absorption_profile(min(args.n, 100_000))
        print(
            f"  density contraction: rate ≈ {abs_prof['rate']:.4f}/step "
            f"(large-deviations reference {abs_prof['reference_rate']:.4f})"
        )

    elif args.cmd == "tree":
        cov = tree.coverage_density(args.x, args.depth)
        print(f"coverage of 1..{args.x} @ depth {args.depth}: {cov:.2%}")
        print("missing:", tree.missing_below(args.x, args.depth))

    elif args.cmd == "terras":
        k = args.k
        print("Q_k bijection:", padic.terras_bijection_check(k))
        print("shift conjugacy:", padic.shift_conjugacy_check(min(k, 14)))
        print("binomial census:", padic.census_is_binomial(padic.parity_census(k), k))
        m_bad, r_rate = padic.bad_set_measure(k)
        print(f"bad-set measure: {m_bad:.6f} (theoretical rate {r_rate:.6f})")

    elif args.cmd == "density":
        ran = False
        if args.interface:
            ran = True
            print("Almost-all ingredient map (G11; see todo/G11_PROGRAM.md):\n")
            for label, description in density.interface_map().items():
                print(f"  • {label}\n      → {description}")
        if args.bad_set is not None:
            ran = True
            print(f"Exact Terras bad-set measure mod 2^k, k = 1..{args.bad_set}:")
            for row in density.bad_set_table(args.bad_set):
                print(
                    f"  k = {row['k']:2d}: measure = {row['measure']} "
                    f"= {row['n_bad']}/{row['total']} "
                    f"≈ {row['measure_float']:.6f} "
                    f"(threshold j = {row['threshold_j']})"
                )
        if args.log_probe:
            ran = True
            probe = density.empirical_long_stopping_log_density(
                args.limit, args.bound
            )
            print(
                f"Empirical probe: odd seeds in 3..{probe.limit} with "
                f"stopping time ≥ {probe.bound}:"
            )
            print(f"  n_exceed = {probe.n_exceed}")
            print(
                f"  partial log-density ≈ {probe.empirical_log_density:.6f} "
                f"(float display only)"
            )
            print(f"  note: {probe.note}")
        if not ran:
            print(
                "Specify --bad-set K, --log-probe, and/or --interface. "
                "See todo/G11_PROGRAM.md.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

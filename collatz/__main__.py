"""
CLI for the Collatz laboratory.

Examples:
    python -m collatz all                      # full report
    python -m collatz verify --limit 1000000   # counterexample sieve
    python -m collatz cycles --d -1 --max-len 16
    python -m collatz exclude --limit-bits 71  # cycle exclusion (N = 2^71, Barina 2025)
    python -m collatz lyapunov --j 10
    python -m collatz spectral --k 4
    python -m collatz transfer --k3 3 --k2 6 --n 100000
    python -m collatz tree --depth 120 --x 1000
"""

from __future__ import annotations

import argparse
import math
import sys

from . import (
    cycles,
    invariants,
    padic,
    report,
    search,
    spectral,
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
    p.add_argument("--limit", type=int, default=200_000)
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

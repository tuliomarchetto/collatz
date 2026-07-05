"""
CLI do laboratório Collatz.

Exemplos:
    python -m collatz all                      # relatório completo
    python -m collatz verify --limit 1000000   # crivo de contraexemplos
    python -m collatz cycles --d -1 --max-len 16
    python -m collatz exclude --limit-bits 71  # exclusão de ciclos (N = 2^71)
    python -m collatz lyapunov --j 10
    python -m collatz spectral --k 4
    python -m collatz transfer --k3 3 --k2 6 --n 100000
    python -m collatz tree --depth 120 --x 1000
"""

from __future__ import annotations

import argparse
import math
import sys

from . import (cycles, invariants, padic, report, search, spectral,
               symmetries, transfer, tree)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="collatz", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("all", help="relatório completo de achados")
    p.add_argument("--limit", type=int, default=200_000)
    p.add_argument("--cycle-len", type=int, default=14)
    p.add_argument("-o", "--output", help="salvar relatório em arquivo")

    p = sub.add_parser("verify", help="crivo de verificação/contraexemplo")
    p.add_argument("--limit", type=int, default=1_000_000)
    p.add_argument("--d", type=int, default=1)

    p = sub.add_parser("cycles", help="enumeração exata de ciclos")
    p.add_argument("--d", type=int, default=1)
    p.add_argument("--max-len", type=int, default=16)
    p.add_argument("--positive-only", action="store_true")

    p = sub.add_parser("exclude", help="exclusão diofantina de ciclos")
    p.add_argument("--limit-bits", type=int, default=71,
                   help="assume todo n <= 2^bits verificado")

    p = sub.add_parser("lyapunov", help="ciclo de média máxima (Karp) mod 2^j")
    p.add_argument("--j", type=int, default=9)

    p = sub.add_parser("spectral", help="operador de transferência mod 3^k")
    p.add_argument("--k", type=int, default=3)

    p = sub.add_parser("transfer", help="operador de transferência infinito (p-ádico)")
    p.add_argument("--k3", type=int, default=3, help="nível 3^k da seção da cadeia de Syracuse")
    p.add_argument("--k2", type=int, default=6, help="nível 2^k da seção do operador em Z_2")
    p.add_argument("--n", type=int, default=100_000, help="janela [1,N] da seção em Z_+")

    p = sub.add_parser("tree", help="árvore inversa: cobertura/crescimento")
    p.add_argument("--depth", type=int, default=120)
    p.add_argument("--x", type=int, default=1000)

    p = sub.add_parser("terras", help="verificação da estrutura 2-ádica")
    p.add_argument("--k", type=int, default=16)

    args = ap.parse_args(argv)

    if args.cmd == "all":
        text = report.run_all(verify_limit=args.limit, cycle_len=args.cycle_len)
        print(text)
        if args.output:
            with open(args.output, "w") as fh:
                fh.write(text + "\n")
            print(f"\n[relatório salvo em {args.output}]", file=sys.stderr)

    elif args.cmd == "verify":
        r = search.verify_range(args.limit, d=args.d)
        if r.all_converge:
            print(f"Todo n <= {args.limit:,} converge (3n{args.d:+d}).")
            print("Recordes de parada:", r.stopping_records[-5:])
            print("Recordes de excursão:", r.excursion_records[-3:])
        else:
            print(f"CONTRAEXEMPLO candidato: n = {r.counterexample}")
            if r.cycle:
                print(f"Ciclo: {r.cycle}")

    elif args.cmd == "cycles":
        cs = cycles.find_cycles(d=args.d, max_len=args.max_len,
                                include_negative=not args.positive_only)
        print(f"{len(cs)} ciclos do sistema 3n{args.d:+d} com comprimento <= {args.max_len}:")
        for c in cs:
            print("  ", c)

    elif args.cmd == "exclude":
        b = cycles.cycle_exclusion_bound(2 ** args.limit_bits)
        print(f"Assumindo todo n <= 2^{args.limit_bits} convergente:")
        print(f"  ciclos não triviais têm > {b['min_odd_steps']:,} passos ímpares")
        print(f"  e > {b['min_length_T_steps']:,} elementos.")

    elif args.cmd == "lyapunov":
        v = invariants.lyapunov_verdict(args.j)
        print(f"mod 2^{args.j}: média máxima = {v['max_mean_log2_growth']:.6f} "
              f"(log2(3)-1 = {math.log2(3)-1:.6f})")
        print(f"ciclo ótimo (com sinal): {v['cycle_as_signed']}")
        print("Função de Lyapunov modular possível?", v["lyapunov_possible"])

    elif args.cmd == "spectral":
        print("uniforme estacionária (exato):", spectral.stationary_uniform_check(args.k))
        print(f"|lambda_2| ~ {spectral.spectral_gap(args.k):.6f}")

    elif args.cmd == "transfer":
        c3, arg3 = transfer.syracuse_w1_coefficient(args.k3)
        print(f"Z_3 (Syracuse), nível 3^{args.k3}: coeficiente W1 exato = "
              f"{c3} ≈ {float(c3):.8f} (cota uniforme 1/3; par extremal {arg3})")
        print("  ramos contraem por exatamente 1/3:",
              transfer.syracuse_branch_contraction_check(min(args.k3, 4)))
        print("  família projetiva pi_k -> pi_{k-1}:",
              transfer.stationary_projective_check(args.k3))
        prof = transfer.koopman_decay_profile(args.k3)
        print(f"  decaimento dev_n <= Lip/3^n: {prof['decay']}; "
              f"U^k f = pi(f) exato: {prof['finite_time']}")
        c2, arg2 = transfer.transfer_2adic_w1_coefficient(args.k2)
        print(f"Z_2 (transferência de T), nível 2^{args.k2}: coeficiente W1 "
              f"exato = {c2} (par extremal {arg2})")
        print("  ramos inversos + contração 1/2:",
              transfer.inverse_branches_check_2adic(min(args.k2, 7)))
        print("  L^k f = média de Haar exata:",
              transfer.haar_mixing_check_2adic(args.k2))
        sec = transfer.finite_section_nilpotency(args.n)
        print(f"Z_+ (pushforward), seção [1,{args.n:,}]: acíclica = {sec['acyclic']}, "
              f"índice de nilpotência = {sec['index']} "
              f"(~{sec['index'] / math.log(args.n):.1f}·ln N; testemunha {sec['witness']})")
        w = transfer.power_weight_obstruction(8)
        print(f"  obstrução a pesos n^theta: n = {w['n']} tem 8 passos ímpares, "
              f"T^8(n)/n = {w['ratio']} ≈ {float(w['ratio']):.2f} > 1")
        ap = transfer.absorption_profile(min(args.n, 100_000))
        print(f"  contração em densidade: taxa ≈ {ap['rate']:.4f}/passo "
              f"(referência grandes desvios {ap['reference_rate']:.4f})")

    elif args.cmd == "tree":
        cov = tree.coverage_density(args.x, args.depth)
        print(f"cobertura de 1..{args.x} @ profundidade {args.depth}: {cov:.2%}")
        print("ausentes:", tree.missing_below(args.x, args.depth))

    elif args.cmd == "terras":
        k = args.k
        print("bijeção Q_k:", padic.terras_bijection_check(k))
        print("conjugação com shift:", padic.shift_conjugacy_check(min(k, 14)))
        print("censo binomial:", padic.census_is_binomial(padic.parity_census(k), k))
        m, r = padic.bad_set_measure(k)
        print(f"medida do conjunto ruim: {m:.6f} (taxa teórica {r:.6f})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Busca direta de contraexemplos.

Um contraexemplo da Conjectura de Collatz seria:
  (a) um ciclo não trivial em inteiros positivos, ou
  (b) uma órbita divergente.

Algoritmos deste módulo:

* verify_range(N)      — crivo ascendente: prova computacionalmente que todo
                         n <= N converge a 1 (ou devolve o contraexemplo).
                         Enquanto verifica, coleta RECORDES de tempo de parada
                         e de excursão máxima — as estatísticas extremais são
                         elas próprias uma propriedade estrutural (crescimento
                         ~ c·log n e ~ n^2 respectivamente).
* brent_cycle_detect   — detecção de ciclo em órbita (algoritmo de Brent,
                         memória O(1)): encontra o ciclo se a órbita for
                         eventualmente periódica.
* divergence_probe     — sondagem de candidatos a órbita divergente.

Validação: aplicados ao sistema 3n-1 (d=-1), estes algoritmos ENCONTRAM os
ciclos não triviais {5,7,10} e {17,25,37,...} — evidência de que, se um
contraexemplo análogo existisse no 3n+1, seria detectado.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple

from .core import T


@dataclass
class VerifyResult:
    limit: int
    d: int
    all_converge: bool
    counterexample: Optional[int] = None       # semente que não converge
    cycle: Optional[Tuple[int, ...]] = None    # ciclo não trivial encontrado
    stopping_records: List[Tuple[int, int]] = field(default_factory=list)
    excursion_records: List[Tuple[int, int]] = field(default_factory=list)


def verify_range(limit: int, d: int = 1, max_steps: int = 100_000) -> VerifyResult:
    """Verifica convergência de todo 2 <= n <= limit sob T (sistema 3n+d).

    Estratégia clássica de crivo ascendente: ao processar n em ordem
    crescente, basta iterar até a órbita cair abaixo de n (tudo abaixo já
    está verificado).  Pares caem imediatamente (n/2 < n), então só ímpares
    são iterados.

    Se uma órbita retorna à própria semente, um CICLO foi encontrado e é
    devolvido.  Se exceder max_steps sem cair, é devolvida como candidata a
    contraexemplo (divergência ou ciclo muito longo).
    """
    res = VerifyResult(limit=limit, d=d, all_converge=True)
    best_stop = 0
    best_exc = 0
    for n in range(3, limit + 1, 2):
        x = n
        steps = 0
        peak = n
        while x >= n:
            x = T(x, d)
            steps += 1
            if x > peak:
                peak = x
            if x == n:  # órbita fechou: ciclo com menor elemento n
                cyc = [n]
                y = T(n, d)
                while y != n:
                    cyc.append(y)
                    y = T(y, d)
                res.all_converge = False
                res.counterexample = n
                res.cycle = tuple(cyc)
                return res
            if steps > max_steps:
                res.all_converge = False
                res.counterexample = n
                return res
        if steps > best_stop:
            best_stop = steps
            res.stopping_records.append((n, steps))
        if peak > best_exc:
            best_exc = peak
            res.excursion_records.append((n, peak))
    return res


def brent_cycle_detect(n: int, d: int = 1,
                       max_power: int = 60) -> Optional[Tuple[int, int, int]]:
    """Algoritmo de Brent para detecção de ciclo na órbita de n sob T.

    Devolve (mu, lam, menor_elemento_do_ciclo) — índice de entrada no ciclo,
    comprimento do ciclo e seu menor elemento — ou None se nenhum ciclo for
    fechado dentro de 2^max_power passos (órbita possivelmente divergente).
    """
    f: Callable[[int], int] = lambda x: T(x, d)
    power = lam = 1
    tortoise = n
    hare = f(n)
    while tortoise != hare:
        if power > (1 << max_power):
            return None
        if lam == power:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1
    # comprimento lam conhecido; encontra mu
    tortoise = hare = n
    for _ in range(lam):
        hare = f(hare)
    mu = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
    # menor elemento do ciclo
    x = tortoise
    lo = x
    for _ in range(lam):
        x = f(x)
        if x < lo:
            lo = x
    return mu, lam, lo


def divergence_probe(n: int, d: int = 1, ceiling_bits: int = 4096,
                     max_steps: int = 1_000_000) -> dict:
    """Sondagem de divergência: segue a órbita de n e reporta se ela
    ultrapassa 2^ceiling_bits (candidata FORTE a divergência) ou se converge
    / entra em ciclo.  Nenhum algoritmo pode PROVAR divergência por
    simulação finita; este classifica candidatos para análise posterior."""
    x = n
    peak = n
    for i in range(max_steps):
        if x == 1:
            return {"n": n, "verdict": "converge", "steps": i, "peak": peak}
        if x.bit_length() > ceiling_bits:
            return {"n": n, "verdict": "explode", "steps": i, "peak_bits": x.bit_length()}
        x = T(x, d)
        if x > peak:
            peak = x
        if x == n:
            return {"n": n, "verdict": "ciclo", "steps": i + 1, "peak": peak}
    return {"n": n, "verdict": "indeterminado", "steps": max_steps, "peak": peak}

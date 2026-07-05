"""
Núcleo: mapas de Collatz e ferramentas de trajetória.

Três formas do mapa são usadas na literatura e aqui:

* Mapa original      C(n) = n/2 se n par;  3n+d se n ímpar.
* Mapa acelerado     T(n) = n/2 se n par;  (3n+d)/2 se n ímpar.
  (cada passo divide por 2 exatamente uma vez; é a forma canônica para
  análise 2-ádica e para a teoria de ciclos)
* Mapa de Syracuse   S(n) = (3n+d) / 2^v2(3n+d), definido de ímpares em
  ímpares (usado no operador de transferência mod 3^k).

O parâmetro d (ímpar, padrão +1) permite estudar os sistemas irmãos 3n-1 e
3n+5, que POSSUEM ciclos não triviais — servindo de bancada de validação
para os algoritmos de busca de contraexemplo.
"""

from __future__ import annotations

from typing import Iterator, List, Tuple


def v2(n: int) -> int:
    """Valuação 2-ádica: maior a com 2^a | n (n != 0)."""
    if n == 0:
        raise ValueError("v2(0) é infinita")
    return (n & -n).bit_length() - 1


def collatz_step(n: int, d: int = 1) -> int:
    """Mapa original C(n) para o sistema 3n+d."""
    return n // 2 if n % 2 == 0 else 3 * n + d


def T(n: int, d: int = 1) -> int:
    """Mapa acelerado T(n) para o sistema 3n+d."""
    return n // 2 if n % 2 == 0 else (3 * n + d) // 2


def syracuse(n: int, d: int = 1) -> int:
    """Mapa de Syracuse (ímpar -> ímpar): remove TODAS as potências de 2."""
    if n % 2 == 0:
        raise ValueError("syracuse é definido apenas para ímpares")
    m = 3 * n + d
    return m >> v2(m)


def trajectory(n: int, d: int = 1, max_steps: int = 10_000,
               accelerated: bool = True) -> List[int]:
    """Trajetória de n sob T (ou C), até atingir 1, um valor repetido
    localmente (ciclo curto) ou max_steps."""
    step = T if accelerated else collatz_step
    out = [n]
    x = n
    for _ in range(max_steps):
        if x == 1 and d == 1:
            break
        x = step(x, d)
        out.append(x)
        if x == n:  # fechou ciclo
            break
    return out


def orbit(n: int, d: int = 1, accelerated: bool = True) -> Iterator[int]:
    """Iterador infinito da órbita de n."""
    step = T if accelerated else collatz_step
    x = n
    while True:
        yield x
        x = step(x, d)


def parity_vector(n: int, k: int, d: int = 1) -> Tuple[int, ...]:
    """Vetor de paridade (p_0,...,p_{k-1}) com p_i = paridade de T^i(n).

    Teorema de Terras (1976): para o mapa acelerado, n mod 2^k determina e é
    determinado pelo vetor de paridade de comprimento k — uma bijeção
    Z/2^k <-> {0,1}^k.  Verificada computacionalmente em `padic`.
    """
    ps = []
    x = n
    for _ in range(k):
        p = x & 1
        ps.append(p)
        x = (3 * x + d) // 2 if p else x // 2
    return tuple(ps)


def stopping_time(n: int, d: int = 1, max_steps: int = 10_000) -> int:
    """Menor i >= 1 com T^i(n) < n ('tempo de parada'); -1 se não ocorrer
    em max_steps.  A conjectura equivale a: todo n >= 2 tem tempo de parada
    finito."""
    x = n
    for i in range(1, max_steps + 1):
        x = T(x, d)
        if x < n:
            return i
    return -1


def total_stopping_time(n: int, d: int = 1, max_steps: int = 10_000_000) -> int:
    """Número de passos de T até atingir 1; -1 se não atingir em max_steps."""
    x = n
    for i in range(max_steps):
        if x == 1:
            return i
        x = T(x, d)
    return -1


def max_excursion(n: int, d: int = 1, max_steps: int = 10_000_000) -> int:
    """Maior valor atingido pela órbita de n antes de chegar a 1."""
    x = n
    hi = n
    for _ in range(max_steps):
        if x == 1:
            return hi
        x = T(x, d)
        if x > hi:
            hi = x
    return hi

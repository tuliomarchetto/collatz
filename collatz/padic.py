"""
Estrutura 2-ádica: a simetria fundamental do mapa acelerado.

Teorema de Terras (1976) / Lagarias (1985).  A aplicação

    Q_k : Z/2^k -> {0,1}^k,   n |-> vetor de paridade de comprimento k

é uma BIJEÇÃO, e o mapa acelerado T é conjugado ao shift de Bernoulli:
o vetor de paridade de T(n) é o shift do vetor de paridade de n.  Em
outras palavras, estendido aos inteiros 2-ádicos Z_2, T é
mensuravelmente isomorfo ao shift (sigma-álgebra e medida de Haar), e a
paridade dos iterados de um n "aleatório" é uma sequência i.i.d. de
moedas justas.  Esta é a simetria estrutural mais forte conhecida do
sistema — e a razão pela qual heurísticas probabilísticas prevêem
convergência (deriva média log(3)/2 - log 2 < 0 por passo).

Algoritmos:

* terras_bijection_check(k)  — verifica exatamente a bijetividade de Q_k.
* shift_conjugacy_check(k)   — verifica Q_{k-1}(T(n)) = shift(Q_k(n)).
* parity_census(k)           — distribuição EXATA do nº de passos ímpares
                               entre os primeiros k passos, sobre n mod 2^k:
                               deve ser Binomial(k, 1/2).  Daí segue a
                               medida exata do "conjunto ruim" (classes que
                               ainda crescem após k passos) e sua taxa de
                               decaimento — comparada com a taxa de grandes
                               desvios  1 - H(1/log2(3)) (H = entropia binária).
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

from .core import parity_vector


def terras_bijection_check(k: int) -> bool:
    """True sse n |-> vetor de paridade(n, k) é bijetivo em Z/2^k."""
    seen = set()
    for n in range(1 << k):
        seen.add(parity_vector(n, k))
    return len(seen) == (1 << k)


def shift_conjugacy_check(k: int) -> bool:
    """Verifica a conjugação com o shift: para todo n mod 2^k, o vetor de
    paridade de T(n) (comprimento k-1) é o shift do vetor de n."""
    from .core import T
    for n in range(1 << k):
        pv = parity_vector(n, k)
        pv_shift = parity_vector(T(n), k - 1)
        if pv[1:] != pv_shift:
            return False
    return True


def parity_census(k: int) -> Dict[int, int]:
    """Conta, para n percorrendo Z/2^k, quantos têm exatamente j passos
    ímpares nos primeiros k passos de T.  Resultado esperado (e implicado
    pela bijeção de Terras): coeficiente binomial C(k, j)."""
    census: Dict[int, int] = {}
    for n in range(1 << k):
        j = sum(parity_vector(n, k))
        census[j] = census.get(j, 0) + 1
    return census


def census_is_binomial(census: Dict[int, int], k: int) -> bool:
    return all(census.get(j, 0) == math.comb(k, j) for j in range(k + 1))


def bad_set_measure(k: int) -> Tuple[float, float]:
    """Medida (fração de resíduos mod 2^k) do conjunto 'ruim': classes cujo
    fator de crescimento após k passos é >= 1, i.e. 3^j >= 2^k, ou seja
    j > k/log2(3).

    Devolve (medida_exata, taxa_teorica) onde a taxa teórica de decaimento
    por grandes desvios é 2^{-k(1-H(theta))}, theta = 1/log2 3 ~ 0.6309.
    A conjectura 'quase todo n tem tempo de parada finito' (Terras) é
    exatamente a afirmação de que essa medida -> 0; a taxa quantifica-a.
    """
    alpha = math.log2(3)
    theta = 1 / alpha
    census = parity_census(k)
    bad = sum(c for j, c in census.items() if j * alpha >= k)
    measure = bad / (1 << k)

    def H(p: float) -> float:
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    rate = 2 ** (-k * (1 - H(theta)))
    return measure, rate

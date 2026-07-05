"""
Teoria exata de ciclos: enumeração por vetores de paridade e exclusão por
frações contínuas.

FATO ESTRUTURAL CENTRAL.  Para o mapa acelerado T do sistema 3n+d, após L
passos com vetor de paridade p = (p_0,...,p_{L-1}) contendo k uns:

    T^L(n) = (3^k · n + b(p)) / 2^L,

onde b(p) é o inteiro dado pela recorrência
    b_0 = 0;  b_{i+1} = 3·b_i + d·2^i  se p_i = 1,  senão  b_{i+1} = b_i.

Um ciclo de comprimento L é exatamente um ponto fixo T^L(n) = n, ou seja

    n = b(p) / (2^L - 3^k).                                   (*)

Isto reduz a busca de ciclos a um problema ARITMÉTICO exato:

* find_cycles          — enumera todos os ciclos de comprimento <= L_max do
                         sistema 3n+d em Z (positivos e negativos), testando
                         a integralidade de (*) para cada vetor de paridade.
                         Encontra os ciclos negativos famosos (-1, -5, -17)
                         e os ciclos não triviais de 3n-1 e 3n+5.
* cycle_exclusion_bound — dado que todo n <= N converge (verificado), deriva
                         um LIMITE INFERIOR RIGOROSO para o número de passos
                         ímpares k de qualquer ciclo não trivial, usando os
                         convergentes da fração contínua de alpha = log2(3).

A exclusão usa a identidade multiplicativa em torno do ciclo:
    2^L = prod_{passos ímpares} (3 + d/x_i)                    (**)
com todos os x_i > N, o que força
    0 < L - k·alpha <= k·eps,   eps = log2(1 + 1/(3N)),
isto é, L/k aproxima alpha por CIMA com erro ~ 1/(3N·ln2).  Pela teoria das
melhores aproximações racionais, para q_i <= k < q_{i+1} (denominadores dos
convergentes de alpha) vale ||k·alpha|| >= ||q_i·alpha|| > 1/(q_i + q_{i+1});
logo um ciclo exige k > 1/(eps·(q_i + q_{i+1})).  Varremos os intervalos
entre denominadores consecutivos e devolvemos o maior K tal que TODO
k <= K é impossível.  (Método na linha de Eliahou 1993 / Simons–de Weger.)
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Dict, List, Optional, Set, Tuple

from .core import T


# ----------------------------------------------------------------------
# Enumeração exata de ciclos
# ----------------------------------------------------------------------

def _fixed_point(parity: Tuple[int, ...], d: int) -> Optional[int]:
    """Resolve (*) para o vetor de paridade dado; devolve n inteiro ou None."""
    L = len(parity)
    k = sum(parity)
    b = 0
    pw = 1  # 2^i
    for p in parity:
        if p:
            b = 3 * b + d * pw
        pw <<= 1
    den = (1 << L) - 3 ** k
    if den == 0 or b % den != 0:
        return None
    return b // den


def _realizes(n: int, parity: Tuple[int, ...], d: int) -> bool:
    """Confere que a órbita real de n tem exatamente esse vetor de paridade
    e retorna a n (ciclo genuíno, não só solução algébrica)."""
    x = n
    for p in parity:
        if (x & 1) != p:
            return False
        x = T(x, d)
    return x == n


def find_cycles(d: int = 1, max_len: int = 20,
                include_negative: bool = True) -> List[Tuple[int, ...]]:
    """Enumera TODOS os ciclos do mapa acelerado T (sistema 3n+d) com
    comprimento <= max_len, em inteiros (positivos e, opcionalmente,
    negativos e zero).

    Correção: todo ciclo contém ao menos um passo ímpar (exceto o ponto
    fixo 0), logo pode ser rotacionado para começar em p_0 = 1; enumeramos
    apenas vetores com p_0 = 1 e deduplicamos pelo conjunto de elementos.

    Para d=1 o resultado esperado (e conjecturado completo em positivos) é
    apenas o ciclo trivial {1,2}; em negativos aparecem os ciclos de
    -1, -5 e -17 — prova de que o detector funciona.
    """
    seen: Set[frozenset] = set()
    cycles: List[Tuple[int, ...]] = []
    for L in range(1, max_len + 1):
        for mask in range(1 << (L - 1)):
            parity = (1,) + tuple((mask >> i) & 1 for i in range(L - 1))
            n = _fixed_point(parity, d)
            if n is None or n == 0:
                continue
            if n < 0 and not include_negative:
                continue
            if not _realizes(n, parity, d):
                continue
            orb = [n]
            x = T(n, d)
            while x != n:
                orb.append(x)
                x = T(x, d)
            key = frozenset(orb)
            if key not in seen:
                seen.add(key)
                m = min(orb, key=abs)
                i = orb.index(m)
                cycles.append(tuple(orb[i:] + orb[:i]))
    cycles.sort(key=lambda c: (len(c), min(c)))
    return cycles


# ----------------------------------------------------------------------
# Frações contínuas de log2(3) e exclusão de ciclos
# ----------------------------------------------------------------------

def log2_3_convergents(max_den: int = 10 ** 30,
                       exact_certificate_upto: int = 10 ** 5) -> List[Tuple[int, int]]:
    """Convergentes p/q de alpha = log2(3), com denominador <= max_den.

    Os quocientes parciais são extraídos de uma aproximação decimal com 120
    dígitos.  Certificação:
    * para q <= exact_certificate_upto, cada convergente é verificado
      EXATAMENTE comparando os inteiros 2^p e 3^q (alternância acima/abaixo
      de alpha) — aritmética inteira pura;
    * para q maiores, a expansão permanece correta enquanto q^2 for muito
      menor que 10^prec (o erro da aproximação decimal, ~10^-120, é menor
      que 1/(2·q_i·q_{i+1}), condição clássica para a FC de uma aproximação
      coincidir com a do número); o laço para antes desse limite."""
    getcontext().prec = 120
    alpha = Decimal(3).ln() / Decimal(2).ln()
    x = alpha
    p0, q0, p1, q1 = 1, 0, 0, 1  # convergentes anteriores
    out: List[Tuple[int, int]] = []
    for _ in range(200):
        a = int(x)
        p0, q0, p1, q1 = a * p0 + p1, a * q0 + q1, p0, q0
        if q0 > max_den or q0 * q0 > 10 ** 100:
            break
        expected_above = (len(out) % 2 == 1)  # 1/1 abaixo, 2/1 acima, 3/2 abaixo...
        if q0 <= exact_certificate_upto:
            # certificado exato: p0/q0 > alpha  <=>  2^p0 > 3^q0
            above = (1 << p0) > 3 ** q0
            if above != expected_above:
                raise ArithmeticError("expansão contínua inconsistente (certificado exato)")
        else:
            above = Fraction(p0, q0) > Fraction(str(alpha))
            if above != expected_above:
                raise ArithmeticError("precisão decimal insuficiente para os convergentes")
        out.append((p0, q0))
        frac = x - a
        if frac == 0:
            break
        x = 1 / frac
    return out


def cycle_exclusion_bound(verified_limit: int) -> Dict[str, int]:
    """Limite inferior rigoroso para ciclos não triviais do 3n+1.

    Hipótese: todo 2 <= n <= verified_limit converge (p.ex. o resultado de
    verify_range, ou o limite computacional publicado ~2^71, Barina).

    Devolve {'min_odd_steps': K, 'min_length': L, 'min_elements': ...}:
    qualquer ciclo não trivial em positivos tem MAIS de K passos ímpares e
    comprimento (em passos de T) maior que L.

    Derivação (ver docstring do módulo): um ciclo com k passos ímpares e
    todos os elementos > N satisfaz 0 < L - k·alpha <= k·eps com
    eps = log2(1 + 1/(3N)); para q_i <= k < q_{i+1} vale
    dist(k·alpha, Z) > 1/(q_i + q_{i+1}); logo k > 1/(eps·(q_i+q_{i+1})).
    """
    N = verified_limit
    getcontext().prec = 120
    ln2 = Decimal(2).ln()
    eps_dec = (1 + Decimal(1) / (3 * N)).ln() / ln2
    # eps como fração superior segura
    eps = Fraction(int(eps_dec * 10 ** 60) + 1, 10 ** 60)

    convs = log2_3_convergents()
    K = 0  # todo k <= K está excluído
    for i in range(len(convs) - 1):
        _, qi = convs[i]
        _, qi1 = convs[i + 1]
        # dentro de [qi, qi1): exclui k <= 1/(eps*(qi+qi1))
        cap = int(Fraction(1, 1) / (eps * (qi + qi1)))
        if cap >= qi1 - 1:
            K = max(K, qi1 - 1)      # intervalo inteiro excluído; continua
        else:
            K = max(K, min(cap, qi1 - 1))
            break
    # comprimento L > k*alpha > K*1.58; elementos do ciclo = L (todos distintos)
    min_len = int(K * Fraction(158, 100))
    return {
        "verified_limit": N,
        "min_odd_steps": K,
        "min_length_T_steps": min_len,
        "min_elements": min_len,
    }

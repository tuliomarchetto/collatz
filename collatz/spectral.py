"""
Operador de transferência de Syracuse módulo 3^k.

Modelo (o mesmo usado por Tao, 2019, "Almost all orbits..."): para n ímpar
"típico", o mapa de Syracuse S(n) = (3n+1)/2^a tem a ~ Geométrica(1/2)
(consequência exata da bijeção de Terras).  Projetando em Z/3^k, obtém-se
uma cadeia de Markov nos resíduos r com 3 ∤ r:

    r  ->  (3r + 1) · inv(2^a)  (mod 3^k),   P(a) = 2^{-a}.

Como 2 é raiz primitiva mod 3^k, inv(2^a) é periódico em a com período
ord = φ(3^k) = 2·3^{k-1}; somando a série geométrica, a matriz de
transição é EXATA em aritmética racional:

    P[r][r'] = (soma sobre a<=ord com transição r->r' de 2^{-a}) / (1 - 2^{-ord}).

Algoritmos:
* syracuse_transfer_matrix(k) — matriz exata (Fraction).
* stationary_uniform_check(k) — testa se a uniforme é estacionária.
  ACHADO: não é!  Mod 3 a medida invariante é (1/3, 2/3) — o viés
  (3n+1)/2^a ≡ (-1)^a (mod 3), P(a ímpar) = 2/3, propaga-se para todo
  3^k.  Um invariante de medida explícito e exato da dinâmica projetada.
* stationary_exact(k) — a medida invariante exata (racional), por
  eliminação gaussiana.
* spectral_gap(k) — módulo do segundo autovalor por iteração de potência
  no complemento espectral da estacionária; lacuna espectral grande =
  mixing rápido = as órbitas esquecem o resíduo inicial exponencialmente
  rápido.  Estrutura a perseguir: gap uniforme em k daria equidistribuição
  quantitativa (na medida invariante) — o tipo de ingrediente que alimenta
  resultados "para quase todo n" (Tao 2019).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Tuple


def _states(k: int) -> List[int]:
    return [r for r in range(3 ** k) if r % 3 != 0]


def syracuse_transfer_matrix(k: int) -> Tuple[List[int], Dict[int, Dict[int, Fraction]]]:
    """Matriz de transição exata da cadeia de Syracuse em {r mod 3^k, 3∤r}.

    Devolve (estados, P) com P[r][r'] racional exato."""
    M = 3 ** k
    states = _states(k)
    ord_ = 2 * 3 ** (k - 1)          # ordem de 2 mod 3^k (2 é raiz primitiva)
    assert pow(2, ord_, M) == 1
    inv2 = pow(2, -1, M)
    norm = Fraction(1) - Fraction(1, 2 ** ord_)
    P: Dict[int, Dict[int, Fraction]] = {r: {} for r in states}
    for r in states:
        target = (3 * r + 1) % M
        t = target
        for a in range(1, ord_ + 1):
            t = (t * inv2) % M       # t = (3r+1)·inv(2^a)
            if t % 3 != 0:           # sempre verdade: (3r+1)/2^a ≢ 0 mod 3
                w = Fraction(1, 2 ** a) / norm
                P[r][t] = P[r].get(t, Fraction(0)) + w
    return states, P


def stationary_uniform_check(k: int) -> bool:
    """Verifica EXATAMENTE se a uniforme sobre os estados é estacionária
    (matriz duplamente estocástica).

    ACHADO (descoberto por este código): NÃO é — p.ex. mod 3 a medida
    invariante exata é pi(1) = 1/3, pi(2) = 2/3: os iterados de Syracuse
    visitam 2 (mod 3) duas vezes mais que 1 (mod 3), porque
    (3n+1)/2^a ≡ 2^{-a} ≡ (-1)^a (mod 3) e a é ímpar com probabilidade
    2/3.  A medida invariante correta é calculada por stationary_exact."""
    states, P = syracuse_transfer_matrix(k)
    col: Dict[int, Fraction] = {r: Fraction(0) for r in states}
    for r in states:
        row_sum = sum(P[r].values())
        if row_sum != 1:
            return False
        for s, w in P[r].items():
            col[s] += w
    return all(c == 1 for c in col.values())


def stationary_exact(k: int) -> Dict[int, Fraction]:
    """Medida invariante EXATA (racional) da cadeia de Syracuse mod 3^k:
    resolve pi·P = pi, soma(pi) = 1 por eliminação gaussiana em Fraction.

    Este é um invariante estrutural genuíno da dinâmica projetada: a única
    medida de probabilidade preservada pelo operador de transferência."""
    states, P = syracuse_transfer_matrix(k)
    n = len(states)
    idx = {r: i for i, r in enumerate(states)}
    # sistema (P^T - I) pi = 0, com última linha substituída por soma = 1
    A: List[List[Fraction]] = [[Fraction(0)] * (n + 1) for _ in range(n)]
    for r in states:
        for s, w in P[r].items():
            A[idx[s]][idx[r]] += w
    for i in range(n):
        A[i][i] -= 1
    A[n - 1] = [Fraction(1)] * n + [Fraction(1)]
    # eliminação gaussiana com pivoteamento parcial
    for col_i in range(n):
        piv = next(row for row in range(col_i, n) if A[row][col_i] != 0)
        A[col_i], A[piv] = A[piv], A[col_i]
        inv = 1 / A[col_i][col_i]
        A[col_i] = [v * inv for v in A[col_i]]
        for row in range(n):
            if row != col_i and A[row][col_i] != 0:
                f = A[row][col_i]
                A[row] = [a - f * b for a, b in zip(A[row], A[col_i])]
    return {r: A[idx[r]][n] for r in states}


def stationary_distribution(k: int, iters: int = 2000,
                            tol: float = 1e-13) -> Dict[int, float]:
    """Distribuição estacionária por iteração de potência (float)."""
    states, P = syracuse_transfer_matrix(k)
    Pf = {r: {s: float(w) for s, w in row.items()} for r, row in P.items()}
    pi = {r: 1.0 / len(states) for r in states}
    for _ in range(iters):
        new = {r: 0.0 for r in states}
        for r in states:
            pr = pi[r]
            for s, w in Pf[r].items():
                new[s] += pr * w
        delta = max(abs(new[r] - pi[r]) for r in states)
        pi = new
        if delta < tol:
            break
    return pi


def memory_loss_check(k: int) -> bool:
    """Verifica EXATAMENTE o colapso de posto do operador de transferência:
    estados r ≡ r' (mod 3^{k-1}) têm linhas IDÊNTICAS, pois a linha só
    depende de 3r+1 (mod 3^k), que só depende de r (mod 3^{k-1}).

    Consequência (por indução): P^k tem posto 1 — a cadeia atinge a medida
    invariante em EXATAMENTE k passos e o espectro além de lambda_1 = 1 é
    {0}.  ACHADO ESTRUTURAL: a projeção mod 3^k não retém nenhuma memória
    de longo prazo; nenhuma obstrução à convergência pode viver em
    aritmética 3-ádica finita — sobra apenas a estrutura 2-ádica/global."""
    M = 3 ** k
    states, P = syracuse_transfer_matrix(k)
    if k == 1:
        pairs = [(1, 2)]
    else:
        step = 3 ** (k - 1)
        pairs = [(r, r + step) for r in states if r + step < M and (r + step) % 3 != 0]
    return all(P[a] == P[b] for a, b in pairs)


def spectral_gap(k: int, iters: int = 400) -> float:
    """Estimativa de |lambda_2| da cadeia mod 3^k por iteração de potência
    na ação à direita f -> P f, removendo a componente espectral do
    autovalor 1 (autovetor direito constante, autovetor esquerdo pi):
    f -> f - (pi·f)·1.  Lacuna espectral = 1 - |lambda_2|."""
    states, P = syracuse_transfer_matrix(k)
    Pf = {r: {s: float(w) for s, w in row.items()} for r, row in P.items()}
    pi = {r: float(v) for r, v in stationary_exact(k).items()}
    import math

    def project(v):
        c = sum(pi[r] * v[r] for r in states)
        return {r: v[r] - c for r in states}

    f = project({r: math.sin(1.0 + 2.7 * i) for i, r in enumerate(states)})
    norm = math.sqrt(sum(v * v for v in f.values()))
    f = {r: v / norm for r, v in f.items()}
    lam = 0.0
    for _ in range(iters):
        g = project({r: sum(w * f[s] for s, w in Pf[r].items()) for r in states})
        norm = math.sqrt(sum(v * v for v in g.values()))
        if norm == 0.0:
            return 0.0
        lam = norm            # ||P f|| com ||f|| = 1
        f = {r: v / norm for r, v in g.items()}
    return lam

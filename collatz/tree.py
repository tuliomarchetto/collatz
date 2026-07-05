"""
Árvore inversa (grafo de pré-imagens de 1).

A conjectura equivale a: a árvore inversa do mapa acelerado T, enraizada
em 1 (excluindo o laço 1->2->1), cobre TODOS os inteiros positivos.
Pré-imagens de m sob T:

    2m               (sempre — desfaz um passo par),
    (2m - 1)/3       (quando inteiro e ímpar — desfaz um passo ímpar).

Um contraexemplo seria exatamente um inteiro fora da árvore.

Algoritmos:
* inverse_tree(depth)      — BFS exata até a profundidade dada.
* coverage_density(X, ..)  — fração dos n <= X alcançados; deve tender a 1
                             (Krasikov–Lagarias provam densidade >= X^0.84
                             para o conjunto alcançado).
* growth_rate(depth)       — nº de nós por nível; o fator assintótico
                             previsto pela heurística de ramificação é
                             (1 + 1/3)·... ~ 4/3 por nível para os nós que
                             admitem o ramo ímpar (2m-1 ≡ 0 mod 3 ocorre
                             para 1/3 dos m; o algoritmo mede o fator real).
* missing_below(X, depth)  — os menores inteiros AINDA não alcançados na
                             profundidade dada (candidatos estruturais a
                             estudar; todos desaparecem ao aprofundar sse a
                             conjectura vale).
"""

from __future__ import annotations

from typing import Dict, List, Set, Tuple


def inverse_children(m: int) -> List[int]:
    """Pré-imagens de m sob T em inteiros positivos."""
    kids = [2 * m]
    q, r = divmod(2 * m - 1, 3)
    if r == 0 and q % 2 == 1 and q > 0:
        kids.append(q)
    return kids


def inverse_tree(depth: int, cap: int | None = None) -> Tuple[Set[int], List[int]]:
    """BFS da árvore inversa a partir de 1.  Devolve (nós alcançados,
    nº de nós novos por nível).

    `cap`: nós maiores que o teto são registrados mas NÃO expandidos —
    poda que mantém o custo O(cap) e permite grandes profundidades.  A
    cobertura reportada é então um MINORANTE da cobertura verdadeira."""
    reached: Set[int] = {1, 2}
    frontier = [2]
    levels = [1]
    for _ in range(depth):
        nxt: List[int] = []
        for m in frontier:
            for c in inverse_children(m):
                if c not in reached:
                    reached.add(c)
                    if cap is None or c <= cap:
                        nxt.append(c)
        levels.append(len(nxt))
        frontier = nxt
        if not frontier:
            break
    return reached, levels


def coverage_density(X: int, depth: int, cap: int | None = None) -> float:
    """Fração dos inteiros 1..X alcançados pela árvore inversa até a
    profundidade dada.  Convergência a 1 quando depth cresce <=> conjectura
    (restrita a n <= X).  cap padrão: 1000·X (a excursão máxima de órbitas
    pequenas excede muito X — p.ex. 703 sobe a 125252 sob T)."""
    if cap is None:
        cap = max(1_000_000, 1000 * X)
    reached, _ = inverse_tree(depth, cap=cap)
    hit = sum(1 for n in range(1, X + 1) if n in reached)
    return hit / X


def growth_rate(depth: int) -> List[float]:
    """Fator de crescimento nível a nível do nº de nós novos (sem poda).
    Heurística de ramificação prevê fator ~ 4/3 por nível."""
    _, levels = inverse_tree(depth)
    return [levels[i + 1] / levels[i] for i in range(1, len(levels) - 1) if levels[i]]


def missing_below(X: int, depth: int, cap: int | None = None) -> List[int]:
    """Menores inteiros <= X ainda fora da árvore na profundidade dada."""
    if cap is None:
        cap = max(1_000_000, 1000 * X)
    reached, _ = inverse_tree(depth, cap=cap)
    return [n for n in range(1, X + 1) if n not in reached][:20]


def required_depth(X: int) -> int:
    """Calcula a profundidade exata e rigorosa necessária na árvore inversa
    para cobrir todos os inteiros de 1 até X. Por definição, isso é
    exatamente o tempo de parada total máximo (total stopping time) no
    intervalo [1, X]."""
    memo = {1: 0}
    max_d = 0
    for n in range(1, X + 1):
        curr = n
        steps = 0
        path = []
        while curr not in memo:
            path.append(curr)
            if curr % 2 == 0:
                curr //= 2
            else:
                curr = 3 * curr + 1
            steps += 1
        total = steps + memo[curr]
        for i, val in enumerate(path):
            memo[val] = total - i
        if memo[n] > max_d:
            max_d = memo[n]
    return max_d


def empirical_bounds(depth: int) -> List[Tuple[int, int]]:
    """Calcula os limites inferior e superior (min, max) dos nós
    na árvore inversa, nível por nível, até a profundidade dada.
    Mostra rigorosamente a expansão do conjunto de nós alcançados."""
    reached: Set[int] = {1, 2}
    frontier = [2]
    bounds = [(1, 1)]  # depth 0
    for _ in range(depth):
        nxt = []
        for m in frontier:
            kids = [2 * m]
            q, r = divmod(2 * m - 1, 3)
            if r == 0 and q % 2 == 1 and q > 0:
                kids.append(q)
            for c in kids:
                if c not in reached:
                    reached.add(c)
                    nxt.append(c)
        frontier = nxt
        if not frontier:
            break
        bounds.append((min(frontier), max(frontier)))
    return bounds

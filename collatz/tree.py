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
    """Profundidade EXATA mínima da árvore inversa para cobrir todos os
    inteiros de 1 a X.  Equivalente ao tempo de parada total máximo (sob o
    mapa acelerado T) entre todos os n em 1..X.

    A conjectura é equivalente a: required_depth(X) é finito para todo X."""
    from .core import total_stopping_time
    return max(total_stopping_time(n) for n in range(1, X + 1))


def empirical_bounds(depth: int) -> List[Tuple[int, int]]:
    """Para cada nível 0..depth da árvore inversa, devolve (min_nó, max_nó)
    dentre os nós NOVOS naquele nível.

    O nível 0 contém {1, 2} (raiz + ciclo trivial).  O max em cada nível é
    exatamente 2^k (o ramo par dobra o max anterior); o min desce
    gradualmente conforme o ramo ímpar (2m-1)/3 produz nós menores — a
    difusão para trás da árvore inversa capturando inteiros pequenos."""
    reached: Set[int] = {1, 2}
    frontier = [2]
    bounds: List[Tuple[int, int]] = [(1, 2)]
    for _ in range(depth):
        nxt: List[int] = []
        for m in frontier:
            for c in inverse_children(m):
                if c not in reached:
                    reached.add(c)
                    nxt.append(c)
        if nxt:
            bounds.append((min(nxt), max(nxt)))
        else:
            bounds.append((0, 0))
            break
        frontier = nxt
    return bounds

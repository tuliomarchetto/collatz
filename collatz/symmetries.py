"""
Busca de simetrias: conjugações entre sistemas 3n+d e automorfismos dos
grafos de transição modulares.

1. CONJUGAÇÕES AFINS EXATAS — affine_conjugacy_search(d, d'):
   procura mapas φ(x) = a·x + b (a, b inteiros) com

       φ(T_d(x)) = T_{d'}(φ(x))   para todo x,

   isto é, φ transporta a dinâmica do sistema 3n+d na do 3n+d'.
   Achados estruturais que o algoritmo redescobre sozinho:
     * φ(x) = -x  conjuga 3n+1 com 3n-1: o problema "3n-1 em positivos"
       (que TEM ciclos não triviais) é exatamente o "3n+1 em negativos".
       Toda simetria de reflexão do problema está aí.
     * φ(x) = d·x conjuga 3n+1 com a restrição de 3n+d aos múltiplos de d
       (auto-similaridade da família).
   Consequência metodológica: contraexemplos dos sistemas irmãos são
   imagens de simetrias — a busca por contraexemplo do 3n+1 deve procurar
   estruturas que quebrem essas simetrias, não que as repitam.

2. AUTOMORFISMOS AFINS DO GRAFO MODULAR — modular_affine_automorphisms(m):
   permutações afins x -> ax+b de Z/m que preservam a relação de transição
   de T.  Grupo trivial = a dinâmica projetada é "rígida" módulo m.

O teste de conjugação é exato: T é afim por paridade com período 2 em n,
e φ é afim; a identidade vale para todo x sse vale num intervalo de
comprimento > 2·|a|·2 (verificamos com folga)."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from .core import T


def _is_conjugacy(a: int, b: int, d1: int, d2: int, test_range: int = 200) -> bool:
    """Verifica φ(T_{d1}(x)) == T_{d2}(φ(x)) para x em [-R, R].  Como ambos
    os lados são funções afins por classes de x mod 2 (e φ afeta paridade
    com período 2), igualdade em 4·|a|+8 pontos consecutivos por classe
    implica igualdade global; test_range=200 dá folga para |a| <= 20."""
    for x in range(-test_range, test_range + 1):
        lhs = a * T(x, d1) + b
        rhs = T(a * x + b, d2)
        if lhs != rhs:
            return False
    return True


def affine_conjugacy_search(d1: int, d2: int, max_a: int = 20,
                            max_b: int = 40) -> List[Tuple[int, int]]:
    """Todas as conjugações afins φ(x)=ax+b (0<|a|<=max_a, |b|<=max_b) do
    sistema 3n+d1 no 3n+d2."""
    found = []
    for a in [i for i in range(-max_a, max_a + 1) if i != 0]:
        for b in range(-max_b, max_b + 1):
            if _is_conjugacy(a, b, d1, d2):
                found.append((a, b))
    return found


def semiconjugacy_multiples(d: int) -> bool:
    """Verifica a auto-similaridade x -> d·x: T_d(d·x) == d·T_1(x)?"""
    return all(T(d * x, d) == d * T(x, 1) for x in range(-100, 101))


def _edges_mod(m: int, d: int = 1) -> Set[Tuple[int, int]]:
    edges = set()
    for n in range(2 * m):
        edges.add((n % m, T(n, d) % m))
    return edges


def modular_affine_automorphisms(m: int, d: int = 1) -> List[Tuple[int, int]]:
    """Automorfismos afins x -> ax+b de Z/m que preservam o conjunto de
    arestas do grafo de transição de T mod m.  Devolve a lista de (a, b);
    (1, 0) — a identidade — está sempre presente."""
    edges = _edges_mod(m, d)
    from math import gcd
    autos = []
    for a in range(1, m):
        if gcd(a, m) != 1:
            continue
        for b in range(m):
            ok = all(((a * u + b) % m, (a * v + b) % m) in edges for (u, v) in edges)
            if ok:
                autos.append((a, b))
    return autos

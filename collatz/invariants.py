"""
Busca automática de invariantes.

Três famílias de algoritmos:

1. INVARIANTES MODULARES EXATOS — induced_map_search(M):
   procura pares (m1, m2) tais que T(n) mod m2 é FUNÇÃO de n mod m1.
   Achado estrutural: T(n) mod m é determinado por n mod 2m (e nada menos,
   para m potência de 2) — a torre Z/2^{k+1} -> Z/2^k cujo limite inverso
   é Z_2, confirmando que a única "coordenada" fatorável da dinâmica é a
   2-ádica.

2. PARTIÇÕES CONSERVADAS — conserved_partition(m):
   computa a partição estável mais grossa de Z/m sob a relação de
   transição (bissimulação / refinamento de partição, como minimização de
   DFA).  Qualquer função constante nos blocos é uma "quantidade discreta
   conservada pela dinâmica projetada".  Também detecta classes
   TRANSIENTES (que a dinâmica abandona e nunca reentra) — p.ex. os
   múltiplos de 3: T nunca produz múltiplo de 3 a partir de passo ímpar,
   logo a dinâmica de longo prazo vive em n coprimo com 3.

3. FUNÇÃO DE LYAPUNOV / CICLO DE MÉDIA MÁXIMA — karp_max_mean_cycle(j):
   Se existisse f(n) = log n + w(n mod 2^j) estritamente decrescente ao
   longo de toda órbita, a conjectura (parte de divergência) estaria
   provada.  Tal w existe sse o CICLO DE MÉDIA MÁXIMA do grafo de
   transição em Z/2^j (pesos = log2 do fator multiplicativo do passo) for
   negativo.  O algoritmo de Karp computa esse valor exatamente.
   ACHADO ESTRUTURAL: o máximo é log2(3) - 1 > 0, atingido no laço do
   resíduo -1 mod 2^j — e todos os ciclos de média positiva correspondem a
   pontos periódicos 2-ádicos que são os ciclos de INTEIROS NEGATIVOS
   (-1, -5, -17).  Ou seja: a obstrução ao método de Lyapunov modular é
   exatamente a existência dos ciclos negativos; nenhuma testemunha
   modular finita pode provar a conjectura — uma explicação algorítmica
   da dificuldade do problema (cf. Conway: generalizações indecidíveis).
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Set, Tuple

from .core import T


# ----------------------------------------------------------------------
# 1. Mapas induzidos módulo m
# ----------------------------------------------------------------------

def induced_map_exists(m1: int, m2: int, d: int = 1) -> bool:
    """True sse n mod m1 determina T(n) mod m2 (teste exato: basta conferir
    todos os resíduos com dois levantamentos, pois T é afim por paridade e
    o comportamento é periódico em n de período lcm(2, m1))."""
    period = m1 if m1 % 2 == 0 else 2 * m1
    table: Dict[int, int] = {}
    for n in range(2 * period):
        r, v = n % m1, T(n, d) % m2
        if table.setdefault(r, v) != v:
            return False
    return True


def induced_map_search(max_m: int = 64, d: int = 1) -> List[Tuple[int, int]]:
    """Para cada m2 <= max_m, encontra o MENOR m1 tal que n mod m1 determina
    T(n) mod m2.  Devolve a lista (m2, m1_minimo)."""
    out = []
    for m2 in range(2, max_m + 1):
        for m1 in range(1, 64 * m2 + 1):
            if induced_map_exists(m1, m2, d):
                out.append((m2, m1))
                break
    return out


# ----------------------------------------------------------------------
# 2. Partição conservada (bissimulação) e classes transientes
# ----------------------------------------------------------------------

def _successors_mod(m: int, d: int = 1) -> Dict[int, Set[int]]:
    """Relação de transição em Z/m: r -> {T(n) mod m : n ≡ r (mod m)}.
    Basta considerar os levantamentos n = r e n = r + m (paridades opostas
    se m é ímpar) e n = r, r+m, ..., cobrindo o período 2m."""
    succ: Dict[int, Set[int]] = {r: set() for r in range(m)}
    for n in range(2 * m):
        succ[n % m].add(T(n, d) % m)
    return succ


def conserved_partition(m: int, d: int = 1) -> List[Set[int]]:
    """Partição estável mais grossa de Z/m que refina o observável
    'paridade' (o único observável intrínseco da dinâmica, pois é ele que
    decide o ramo do mapa): refinamento iterativo pela assinatura
    'conjunto de blocos sucessores' até ponto fixo (bissimulação, como
    minimização de DFA).  Blocos de tamanho > 1 sobreviventes seriam
    invariantes discretos ocultos; para m = 2^k a partição refina até
    singletons — equivalente à bijeção de Terras (k paridades futuras
    distinguem n mod 2^k)."""
    succ = _successors_mod(m, d)
    # coloração inicial: paridade quando ela é função do resíduo (m par)
    if m % 2 == 0:
        block: Dict[int, int] = {r: r % 2 for r in range(m)}
    else:
        block = {r: 0 for r in range(m)}
    while True:
        sig: Dict[int, Tuple] = {
            r: (block[r], frozenset(block[s] for s in succ[r])) for r in range(m)
        }
        relabel: Dict[Tuple, int] = {}
        new_block: Dict[int, int] = {}
        for r in range(m):
            new_block[r] = relabel.setdefault(sig[r], len(relabel))
        if len(set(new_block.values())) == len(set(block.values())):
            break
        block = new_block
    groups: Dict[int, Set[int]] = {}
    for r, b in block.items():
        groups.setdefault(b, set()).add(r)
    return sorted(groups.values(), key=lambda s: (len(s), min(s)))


def transient_classes(m: int, d: int = 1) -> Set[int]:
    """Classes de resíduo mod m que, uma vez abandonadas pela órbita, nunca
    são reentradas: nenhuma OUTRA classe transita para elas (arestas de
    entrada apenas do laço próprio).  P.ex. m=3: {0} — nenhum n coprimo
    com 3 tem T(n) múltiplo de 3; logo toda órbita abandona os múltiplos
    de 3 em tempo finito e a dinâmica de longo prazo vive em 3 ∤ n.
    Idem, a árvore inversa de 1 não contém múltiplo de 3."""
    succ = _successors_mod(m, d)
    incoming: Dict[int, Set[int]] = {r: set() for r in range(m)}
    for r, ss in succ.items():
        for s in ss:
            incoming[s].add(r)
    return {r for r in range(m)
            if incoming[r] <= {r} and (succ[r] - {r})}


# ----------------------------------------------------------------------
# 3. Ciclo de média máxima (Karp) — obstrução à função de Lyapunov modular
# ----------------------------------------------------------------------

def transition_graph_mod2j(j: int) -> Tuple[List[List[int]], List[float]]:
    """Grafo de transição em Z/2^j para T.  Cada resíduo r tem exatamente
    dois sucessores (levantamentos r e r+2^j), todos os arcos saindo de r
    têm o mesmo peso: log2(3/2) se r ímpar, -1 se r par (fator
    multiplicativo do passo).  Devolve (lista de sucessores, peso por nó)."""
    M = 1 << j
    succ = [[T(r) % M, T(r + M) % M] for r in range(M)]
    w = [math.log2(3) - 1 if r & 1 else -1.0 for r in range(M)]
    return succ, w


def karp_max_mean_cycle(j: int) -> Tuple[float, List[int]]:
    """Algoritmo de Karp: valor exato (em float) do ciclo de média máxima do
    grafo de transição mod 2^j, e um ciclo que o atinge.

    Interpretação: qualquer órbita real induz um passeio neste grafo, e o
    crescimento assintótico de log2(n) por passo é majorado pela média do
    melhor ciclo alcançável.  Média máxima < 0 provaria não-divergência.
    """
    succ, w = transition_graph_mod2j(j)
    M = len(succ)
    NEG = float("-inf")
    # F[t][v] = maior peso de um passeio de comprimento t terminando em v
    F = [[NEG] * M for _ in range(M + 1)]
    parent: List[List[int]] = [[-1] * M for _ in range(M + 1)]
    for v in range(M):
        F[0][v] = 0.0
    for t in range(1, M + 1):
        Ft, Fp = F[t], F[t - 1]
        for u in range(M):
            fu = Fp[u]
            if fu == NEG:
                continue
            cand = fu + w[u]
            for v in succ[u]:
                if cand > Ft[v]:
                    Ft[v] = cand
                    parent[t][v] = u
    best = NEG
    best_v = -1
    for v in range(M):
        if F[M][v] == NEG:
            continue
        val = min(
            (F[M][v] - F[t][v]) / (M - t)
            for t in range(M) if F[t][v] > NEG
        )
        if val > best:
            best, best_v = val, v
    # reconstrói um passeio e extrai um ciclo
    walk = [best_v]
    v = best_v
    for t in range(M, 0, -1):
        v = parent[t][v]
        walk.append(v)
    walk.reverse()
    last: Dict[int, int] = {}
    cyc: List[int] = []
    for i, v in enumerate(walk):
        if v in last:
            cyc = walk[last[v]:i]
            break
        last[v] = i
    return best, cyc


def lyapunov_verdict(j: int) -> Dict[str, object]:
    """Executa Karp e interpreta: os nós do ciclo ótimo são levantados a
    inteiros 2-ádicos; ciclos de média positiva devem corresponder aos
    ciclos de inteiros NEGATIVOS do 3n+1 (p.ex. resíduo 2^j - 1 = -1)."""
    mean, cyc = karp_max_mean_cycle(j)
    M = 1 << j
    as_signed = [r - M if r > M // 2 else r for r in cyc]
    return {
        "j": j,
        "max_mean_log2_growth": mean,
        "cycle_residues": cyc,
        "cycle_as_signed": as_signed,
        "lyapunov_possible": mean < 0,
    }


# ----------------------------------------------------------------------
# Deriva (drift) esperada por classe de resíduo
# ----------------------------------------------------------------------

def drift_by_class(m: int, depth: int, d: int = 1) -> Dict[int, float]:
    """Deriva média de log2 após `depth` passos, condicionada a n mod m,
    calculada EXATAMENTE fazendo a média sobre os resíduos mod m·2^depth
    (que determinam as primeiras `depth` paridades).  Deriva negativa em
    toda classe é evidência (não prova) de contração típica."""
    alpha = math.log2(3)
    period = m * (1 << depth)
    tot: Dict[int, float] = {r: 0.0 for r in range(m)}
    cnt: Dict[int, int] = {r: 0 for r in range(m)}
    for n in range(period):
        x = n
        odd = 0
        for _ in range(depth):
            if x & 1:
                odd += 1
            x = T(x, d)
        tot[n % m] += odd * alpha - depth
        cnt[n % m] += 1
    return {r: tot[r] / cnt[r] for r in range(m)}

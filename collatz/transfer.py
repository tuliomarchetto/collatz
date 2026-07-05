"""
Operador de transferência INFINITO: das projeções mod 3^k a operadores em
espaços funcionais p-ádicos.

Motivação.  O módulo `spectral` constrói as matrizes de transferência da
cadeia de Syracuse projetada em Z/3^k e descobre que seu espectro é trivial
({1} ∪ {0}: colapso de posto em k passos).  A lacuna espectral ℓ² das seções
finitas portanto NÃO carrega informação no limite k → ∞.  Este módulo
substitui as projeções por operadores nos espaços infinitos dos quais elas
são seções, e identifica a norma em que a lacuna espectral sobrevive ao
limite — e é uniforme em k.

1. Operador de Koopman da cadeia de Syracuse em C(Z_3).  A cadeia
   x ↦ (3x+1)·2^{-a}, P(a) = 2^{-a}, faz sentido em Z_3 (2 é invertível) e é
   um IFS com contração UNIFORME: cada ramo phi_a(x) = (3x+1)·2^{-a} satisfaz

       |phi_a(x) − phi_a(y)|_3 = (1/3)·|x − y|_3      (exato, pois
       phi_a(x) − phi_a(y) = 3·2^{-a}(x−y) e |2|_3 = 1, |3|_3 = 1/3).

   Consequências espectrais (verificadas exatamente aqui em níveis finitos):
   * O coeficiente de contração de Wasserstein (Dobrushin) do núcleo é
     <= 1/3 em TODO nível 3^k — cota uniforme em k, ao contrário da lacuna
     ℓ² (valores exatos: 5/21, 455/1387, ... ↗ 1/3).  Logo, no espaço
     Lip(Z_3), U = Pi + R com Pi = projeção de posto 1 sobre a medida
     invariante e raio espectral de R <= 1/3.
   * Contração global (ponto fixo de Banach em Wasserstein): existe UMA
     medida invariante mu em Z_3 — a "medida de Syracuse" (Tao 2019) — e
     toda medida inicial converge exponencialmente, taxa 3^{-n}.  As
     estacionárias finitas pi_k formam família projetiva consistente
     (verificação exata): elas SÃO os valores de mu nos cilindros.
   * Equidistribuição em tempo finito: U^k f = pi_k(f) EXATAMENTE para toda
     f de nível k (o colapso de posto de `spectral` relido: é a sombra da
     contração 1/3 — funções de nível k têm "frequência" 3-ádica k e cada
     passo de U apaga um dígito).

2. Operador de transferência de T em C(Z_2).  Todo x em Z_2 tem exatamente
   dois T-preimagens, 2x e (2x−1)/3 (3 é invertível em Z_2), cada uma com
   jacobiano de Haar 1/2:

       (Lf)(x) = (1/2)·f(2x) + (1/2)·f((2x−1)/3).

   Cada ramo inverso contrai a métrica 2-ádica por exatamente 1/2; o
   coeficiente de Wasserstein é EXATAMENTE 1/2 em todo nível 2^k; L^k f =
   média de Haar exata.  Espectro em Lip(Z_2): {1} ∪ disco de raio 1/2 —
   mixing máximo, densidade invariante = Haar (dual funcional-analítico da
   conjugação de Terras com o shift, módulo `padic`).

3. Onde a conjectura vive: ℓ¹(Z_+).  As contrações acima são globais em
   espaços onde Z_+ é invisível (Haar-nulo; massas pontuais não são
   Lipschitz-duais).  Este módulo mede exatamente o que resta em Z_+:
   * Seções finitas [1, N] do pushforward de T são NILPOTENTES fora do
     ciclo {1,2} (o grafo é um DAG — qualquer ciclo seria um contraexemplo):
     espectro {0} de novo, com índice de nilpotência ~ c·log N.
   * NENHUM peso puro w(n) = n^theta dá contração uniforme em ℓ¹_w em t
     passos, para NENHUM t: testemunha exata n = 2^t − 1 ≡ −1 (mod 2^t)
     com t passos ímpares seguidos e razão T^t(n)/n = (3^t−1)/(2^t−1) > 1.
     É a MESMA obstrução do ciclo de Karp (`invariants`): o ponto 2-ádico −1.
   * A contração em Z_+ é apenas "em densidade": a massa ainda não absorvida
     em {1,2} decai exponencialmente com taxa medida por absorption_profile
     (referência: taxa de grandes desvios 2^{-(1-H(1/log2 3))} por passo).

Síntese espectral: todas as faces compactas/finitas do problema têm espectro
trivial {1} ∪ {0}, e os operadores infinitos têm lacunas espectrais MÁXIMAS
(raio 1/3 em Z_3, 1/2 em Z_2) com contração global provada.  A conjectura
não é uma questão espectral em nenhum espaço homogêneo: vive exatamente na
fronteira singular Z_+ ⊂ Z_2 (medida nula), onde a dinâmica move massas
pontuais isometricamente e a contração de densidades não a alcança.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

from .core import T, total_stopping_time
from .spectral import stationary_exact, syracuse_transfer_matrix

Measure = Dict[int, Fraction]


def _vp(n: int, p: int) -> int:
    """Valuação p-ádica de um inteiro não nulo."""
    if n == 0:
        raise ValueError("v_p(0) é infinita")
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def _vp_fraction(q: Fraction, p: int) -> int:
    """Valuação p-ádica de um racional não nulo."""
    return _vp(q.numerator, p) - _vp(q.denominator, p)


# ---------------------------------------------------------------------------
# Wasserstein exato em ultramétricas p-ádicas
# ---------------------------------------------------------------------------

def wasserstein_padic(mu: Measure, nu: Measure, p: int, k: int) -> Fraction:
    """Distância de Wasserstein W1 EXATA (racional) entre medidas de mesma
    massa em Z/p^k com a métrica p-ádica d(x, y) = p^{-v_p(x-y)}.

    Em ultramétricas o transporte ótimo é o casamento guloso hierárquico
    (célula a célula), o que dá a fórmula fechada

        W1 = sum_{j=1}^{k-1} (p^{-(j-1)} - p^{-j})·m_j  +  p^{-(k-1)}·m_k,

    onde m_j = (1/2)·sum_{c mod p^j} |mu(c) - nu(c)| é a massa que precisa
    atravessar fronteiras de células de nível j.  (Cota inferior: todo
    acoplamento move >= m_j através do nível j; a gulosa atinge todas as
    m_j simultaneamente.)"""
    W = Fraction(0)
    for j in range(1, k + 1):
        pj = p ** j
        cells: Dict[int, Fraction] = {}
        for r, m in mu.items():
            cells[r % pj] = cells.get(r % pj, Fraction(0)) + m
        for r, m in nu.items():
            cells[r % pj] = cells.get(r % pj, Fraction(0)) - m
        m_j = sum(abs(v) for v in cells.values()) / 2
        if j < k:
            W += (Fraction(1, p ** (j - 1)) - Fraction(1, p ** j)) * m_j
        else:
            W += Fraction(1, p ** (k - 1)) * m_j
    return W


def w1_contraction_coefficient(P: Dict[int, Measure], p: int, k: int
                               ) -> Tuple[Fraction, Optional[Tuple[int, int]]]:
    """Coeficiente de contração de Wasserstein (Dobrushin) EXATO do núcleo P
    no nível p^k:

        tau = max_{x != y}  W1(P[x], P[y]) / d(x, y).

    tau < 1 implica contração global: medida invariante única e convergência
    W1 a taxa tau^n de QUALQUER medida inicial (Banach); o operador de
    Koopman satisfaz Lip(Uf) <= tau·Lip(f) (dualidade de Kantorovich), logo
    spec(U|Lip) ⊆ {1} ∪ {|z| <= tau}.  tau é computado exatamente e, ao
    contrário da lacuna ℓ² das seções finitas, é UNIFORME em k — é a
    propriedade espectral que sobrevive ao operador infinito."""
    states = sorted(P)
    best = Fraction(0)
    arg: Optional[Tuple[int, int]] = None
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            d = Fraction(1, p ** _vp(x - y, p))
            ratio = wasserstein_padic(P[x], P[y], p, k) / d
            if ratio > best:
                best, arg = ratio, (x, y)
    return best, arg


# ---------------------------------------------------------------------------
# 1. O operador infinito em Z_3 (cadeia de Syracuse)
# ---------------------------------------------------------------------------

def syracuse_branch_contraction_check(k: int, amax: int = 6) -> bool:
    """Verifica EXATAMENTE que cada ramo phi_a(x) = (3x+1)/2^a da cadeia de
    Syracuse contrai a métrica 3-ádica por fator exatamente 1/3:

        v_3(phi_a(x) - phi_a(y)) = v_3(x - y) + 1

    para todos os pares de estados x != y mod 3^k e todo a <= amax.  (Os
    valores phi_a(x) são racionais 2-integrais, logo elementos de Z_3; a
    verificação usa aritmética racional exata.)  Este é o fato que torna a
    cadeia um IFS uniformemente contrativo em Z_3."""
    states = [r for r in range(3 ** k) if r % 3 != 0]
    for a in range(1, amax + 1):
        for i, x in enumerate(states):
            for y in states[i + 1:]:
                diff = Fraction(3 * x + 1, 2 ** a) - Fraction(3 * y + 1, 2 ** a)
                if _vp_fraction(diff, 3) != _vp(x - y, 3) + 1:
                    return False
    return True


def syracuse_w1_coefficient(k: int) -> Tuple[Fraction, Optional[Tuple[int, int]]]:
    """Coeficiente de Wasserstein exato da cadeia de Syracuse no nível 3^k.

    ACHADO: tau_k <= 1/3 para TODO k (cota provada pelo acoplamento de
    mesmo `a` + contração 1/3 dos ramos; aqui computada exatamente), com
    valores exatos tau_2 = 5/21, tau_3 = 455/1387,
    tau_4 = 7635497415/22906579627 ≈ 0.33333206 ↗ 1/3: nas seções finitas
    acoplamentos entre ramos distintos ainda ajudam, mas no limite o
    coeficiente do operador infinito é exatamente 1/3.  A cota uniforme
    tau <= 1/3 é a lacuna espectral que sobrevive a k → ∞:
    spec(U|Lip(Z_3)) ⊆ {1} ∪ {|z| <= 1/3}."""
    _, P = syracuse_transfer_matrix(k)
    return w1_contraction_coefficient(P, 3, k)


def stationary_projective_check(k: int) -> bool:
    """Verifica EXATAMENTE que as medidas estacionárias finitas são uma
    família projetiva: a projeção mod 3^{k-1} de pi_k é pi_{k-1}.

    Consequência (com a contração 1/3, via Banach/Kolmogorov): as pi_k são
    os valores nos cilindros da ÚNICA medida invariante mu em Z_3 — a
    medida de Syracuse cuja equidistribuição alimenta Tao 2019."""
    pi_k = stationary_exact(k)
    pi_prev = stationary_exact(k - 1)
    M = 3 ** (k - 1)
    proj: Dict[int, Fraction] = {}
    for r, m in pi_k.items():
        proj[r % M] = proj.get(r % M, Fraction(0)) + m
    return proj == pi_prev


def koopman_decay_profile(k: int, f: Optional[Dict[int, Fraction]] = None) -> Dict:
    """Itera o operador de Koopman U^n f no nível 3^k, EXATAMENTE, e mede

        dev_n = max_x |U^n f(x) - pi(f)|.

    Verificações espectrais embutidas no resultado:
    * dev_n <= Lip_3(f)·(1/3)^n  (a contração 1/3 em ação: 'decay' devolve
      True se a cota vale para todo n);
    * dev_k = 0 EXATAMENTE ('finite_time' True): U^k f é constante = pi(f)
      — equidistribuição em tempo finito nos cilindros, a releitura
      espectral do colapso de posto de `spectral.memory_loss_check`."""
    states, P = syracuse_transfer_matrix(k)
    pi = stationary_exact(k)
    if f is None:  # função de teste "genérica" (racional, não Lipschitz-ajustada)
        f = {r: Fraction((r * r + 1) % 11, 11) for r in states}
    lip = Fraction(0)
    for i, x in enumerate(states):
        for y in states[i + 1:]:
            lip = max(lip, abs(f[x] - f[y]) * 3 ** _vp(x - y, 3))
    mean = sum(pi[r] * f[r] for r in states)
    devs: List[Fraction] = []
    g = f
    for _ in range(k):
        g = {x: sum(w * g[y] for y, w in P[x].items()) for x in states}
        devs.append(max(abs(g[x] - mean) for x in states))
    decay = all(dev <= lip * Fraction(1, 3 ** (n + 1))
                for n, dev in enumerate(devs))
    return {"lipschitz": lip, "mean": mean, "devs": devs,
            "decay": decay, "finite_time": devs[-1] == 0}


# ---------------------------------------------------------------------------
# 2. O operador infinito em Z_2 (transferência do mapa acelerado T)
# ---------------------------------------------------------------------------

def inverse_branches_check_2adic(k: int) -> bool:
    """Verifica EXATAMENTE, mod 2^k, que os dois ramos do operador de
    transferência são as T-preimagens em Z_2 e que cada um contrai a
    métrica 2-ádica por fator exatamente 1/2:

        T(2x) = x;   y = (2x-1)/3 é ímpar em Z_2 e T(y) = x;
        v_2(ramo(x) - ramo(y)) = v_2(x - y) + 1."""
    M2 = 1 << (k + 1)                       # trabalha mod 2^{k+1} p/ ver v+1
    inv3 = pow(3, -1, M2)
    for x in range(1 << k):
        y = ((2 * x - 1) * inv3) % M2
        if y % 2 == 0:                       # (2x-1)/3 deve ser ímpar em Z_2
            return False
        if (3 * y + 1) // 2 % (1 << k) != x:  # T(y) = x mod 2^k
            return False
    for x in range(1 << k):
        for y in range(x + 1, 1 << k):
            v = _vp(x - y, 2)
            b0 = (2 * x - 2 * y) % M2
            b1 = ((2 * x - 1) * inv3 - (2 * y - 1) * inv3) % M2
            for b in (b0, b1):
                if v + 1 < k + 1 and _vp(b if b else M2, 2) != v + 1:
                    return False
    return True


def transfer_2adic_matrix(k: int) -> Dict[int, Measure]:
    """Núcleo do operador de transferência de T no nível 2^k:

        (Lf)(x) = (1/2)f(2x) + (1/2)f((2x-1)/3)   (mod 2^k, 3 invertível).

    É a cadeia de Markov 'reversa' (passeio nos ramos inversos com pesos de
    Haar).  Duplamente estocástica: Haar (uniforme) é a densidade
    invariante — L1 = 1 e a coluna de cada y soma 1."""
    M = 1 << k
    inv3 = pow(3, -1, M)
    half = Fraction(1, 2)
    P: Dict[int, Measure] = {}
    for x in range(M):
        row: Measure = {}
        for img in ((2 * x) % M, ((2 * x - 1) * inv3) % M):
            row[img] = row.get(img, Fraction(0)) + half
        P[x] = row
    return P


def transfer_2adic_w1_coefficient(k: int) -> Tuple[Fraction, Optional[Tuple[int, int]]]:
    """Coeficiente de Wasserstein exato do operador de transferência 2-ádico.

    ACHADO: tau = 1/2 EXATAMENTE para todo k >= 2 — spec(L|Lip(Z_2)) ⊆
    {1} ∪ {|z| <= 1/2}, lacuna espectral máxima do mapa 2-para-1: o análogo
    funcional-analítico da conjugação de Terras com o shift de Bernoulli."""
    return w1_contraction_coefficient(transfer_2adic_matrix(k), 2, k)


def haar_mixing_check_2adic(k: int, f: Optional[Dict[int, Fraction]] = None) -> bool:
    """Verifica EXATAMENTE que L^k f = média de Haar de f, para f racional
    arbitrária de nível 2^k: mixing completo em tempo finito nos cilindros
    (L manda funções de nível k em funções de nível k-1 — cada passo apaga
    um dígito 2-ádico, espelho exato do shift de Terras)."""
    M = 1 << k
    P = transfer_2adic_matrix(k)
    if f is None:
        f = {x: Fraction((x * x * x + x + 1) % 13, 13) for x in range(M)}
    mean = sum(f.values()) / M
    g = f
    for _ in range(k):
        g = {x: sum(w * g[y] for y, w in P[x].items()) for x in range(M)}
    return all(v == mean for v in g.values())


# ---------------------------------------------------------------------------
# 3. Onde a conjectura vive: o pushforward em ℓ¹(Z_+)
# ---------------------------------------------------------------------------

def finite_section_nilpotency(N: int, d: int = 1) -> Dict:
    """Seção finita [1, N] do operador de pushforward de T (sistema 3n+d):
    grafo n -> T(n) restrito a [1, N], removido o ciclo trivial de 1.

    A seção é NILPOTENTE sse o grafo é acíclico — qualquer ciclo seria um
    ciclo não trivial genuíno de T (um contraexemplo).  Devolve
    {'acyclic', 'index', 'witness', 'cycle'}: index = índice de nilpotência
    (menor t com L^t = 0 na seção) = nº de nós do caminho mais longo.

    ACHADO: para d=1 o espectro de TODA seção finita é {0} (fora de {1,2}),
    com índice ~ c·log N — a terceira face finita do problema com espectro
    trivial.  VALIDAÇÃO do detector: para d=-1 o algoritmo encontra o ciclo
    {5, 7, 10} (a seção NÃO é nilpotente — o espectro acusa o contraexemplo)."""
    # ciclo trivial: órbita de 1
    triv = {1}
    x = T(1, d)
    while x not in triv:
        triv.add(x)
        x = T(x, d)
    depth = {}
    for start in range(1, N + 1):
        if start in triv or start in depth:
            continue
        stack = [start]
        onstack = {start}
        while stack:
            n = stack[-1]
            t = T(n, d)
            if t > N or t in triv:
                depth[n] = 1 + depth.get(t, 0) if t in depth else 1
                stack.pop()
                onstack.discard(n)
            elif t in onstack:                      # ciclo não trivial!
                cyc = []
                i = len(stack) - 1
                while stack[i] != t:
                    cyc.append(stack[i])
                    i -= 1
                cyc.append(t)
                return {"acyclic": False, "index": None,
                        "witness": None, "cycle": sorted(cyc)}
            elif t in depth:
                depth[n] = 1 + depth[t]
                stack.pop()
                onstack.discard(n)
            else:
                stack.append(t)
                onstack.add(t)
    if not depth:
        return {"acyclic": True, "index": 0, "witness": None, "cycle": None}
    witness = max(depth, key=depth.get)
    return {"acyclic": True, "index": depth[witness],
            "witness": witness, "cycle": None}


def power_weight_obstruction(t: int) -> Dict:
    """Prova computável de que NENHUM peso puro w(n) = n^theta torna o
    pushforward uma contração uniforme de ℓ¹_w em t passos, para NENHUM
    theta e NENHUM t fixo.

    Testemunha exata: n = 2^t − 1 ≡ −1 (mod 2^t) tem t passos ímpares
    consecutivos (vetor de paridade todo-1, Terras), logo

        T^t(n)/n = (3^t − 1)/(2^t − 1) > 1   (exato),

    e a família n = 2^t·m − 1 dá razões → (3/2)^t com testemunhas
    arbitrariamente grandes: sup_n (T^t(n)/n)^theta > 1 para theta > 0.
    Para theta <= 0 os pares n = 2^t·m falham (razão 2^{-t·theta} >= 1).
    É a MESMA obstrução do ciclo de média máxima de Karp (`invariants`):
    o ponto periódico 2-ádico −1.  Contração em Z_+ não pode ser uniforme
    — só 'em densidade' (absorption_profile)."""
    n = 2 ** t - 1
    x = n
    parities = []
    for _ in range(t):
        parities.append(x & 1)
        x = T(x)
    ratio = Fraction(x, n)
    return {"t": t, "n": n, "all_odd": all(p == 1 for p in parities),
            "endpoint": x, "ratio": ratio,
            "ratio_matches_formula": ratio == Fraction(3 ** t - 1, 2 ** t - 1),
            "limit_ratio": (1.5) ** t}


def absorption_profile(N: int, stride: int = 20) -> Dict:
    """Contração 'em densidade' em Z_+, medida: evolui a massa uniforme em
    [1, N] pelo pushforward exato de T (órbitas inteiras, sem truncagem) e
    mede m(t) = fração ainda não absorvida no ciclo {1, 2} após t passos.

    Devolve o perfil {t: m(t)} e a taxa efetiva por passo no regime
    exponencial (entre os quantis 90% e 99.9%), com a referência de grandes
    desvios 2^{-(1-H(1/log2 3))} ≈ 0.9661 por passo (`padic`).  Esta taxa é
    o que resta de 'lacuna espectral' na face Z_+ do problema: contração da
    MASSA, não de cada ponto — exatamente a força de um teorema de densidade
    (Terras, Tao) e nada mais."""
    times = [total_stopping_time(n) for n in range(2, N + 1)]
    assert all(s >= 0 for s in times)
    tmax = max(times)
    counts = [0] * (tmax + 1)
    for s in times:
        counts[s] += 1
    total = len(times)
    m: List[float] = []
    rem = total
    for t in range(tmax + 1):
        rem -= counts[t]
        m.append(rem / total)
    profile = {t: m[t] for t in range(0, tmax + 1, stride)}
    t1 = next(t for t, v in enumerate(m) if v <= 0.10)
    t2 = next((t for t, v in enumerate(m) if v <= 0.001), tmax)
    rate = (m[t2] / m[t1]) ** (1.0 / (t2 - t1)) if t2 > t1 and m[t2] > 0 else None
    theta = 1 / math.log2(3)
    H = -theta * math.log2(theta) - (1 - theta) * math.log2(1 - theta)
    return {"tmax": tmax, "profile": profile, "rate": rate,
            "t_10pct": t1, "t_01pct": t2,
            "reference_rate": 2 ** (-(1 - H))}

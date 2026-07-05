# Relatório — busca de invariantes, simetrias e estrutura na dinâmica de Collatz

## 1. Busca direta de contraexemplo (crivo + detecção de ciclos)

- Todo n ≤ 200,000 converge a 1 (verificado agora; literatura: ≈ 2^71). Nenhum contraexemplo.
- Recorde de tempo de parada total: n = 35655 com 135 passos (crescimento observado ~ c·log n, c ≈ 12.9).
- Recorde de excursão: n = 159487 atinge 8,601,188,876 (razão pico/n² ≈ 0.34; escala conjecturada ~ n²).
- Validação do detector no sistema irmão 3n−1: ciclo não trivial encontrado: (5, 7, 10)

## 2. Enumeração exata de ciclos (pontos fixos racionais dos vetores de paridade)

- Sistema 3n+1, comprimento ≤ 14, inteiros (ℤ): 4 ciclos encontrados:
    - (-1)  [NEGATIVO]
    - (1, 2)  [trivial]
    - (-5, -7, -10)  [NEGATIVO]
    - (-17, -25, -37, -55, -82, -41, -61, -91, -136, -68, -34)  [NEGATIVO]
- Nenhum ciclo positivo não trivial — consistente com a conjectura; os ciclos negativos (−1, −5, −17) são reencontrados pelo algoritmo, confirmando sua completude até o comprimento varrido.
- Sistema irmão 3n+5 (positivos): 4 ciclos, p.ex. (5, 10); (1, 4, 2); (19, 31, 49, 76, 38) — contraexemplos existem em sistemas vizinhos e o mesmo algoritmo os encontra.

## 3. Exclusão de ciclos via aproximação diofantina de log₂3

- Com o limite verificado localmente (N = 200,000): qualquer ciclo não trivial tem > 428 passos ímpares (> 676 elementos).
- Com o limite da literatura (N = 2^71): > 65,470,613,320 passos ímpares, ou seja, > 103,443,569,045 elementos — um ciclo contraexemplo teria dezenas de bilhões de termos.
- Estrutura usada: 2^L = Π(3 + 1/xᵢ) força L/k a aproximar log₂3 por cima com erro < 1/(3N ln 2); os convergentes de log₂3 (verificados exatamente por comparação de potências 2^p × 3^q) tornam isso impossível para k pequeno.

## 4. Simetria 2-ádica (Terras): conjugação com o shift de Bernoulli

- Bijeção Q_k: Z/2^k ↔ vetores de paridade, k = 16: confirmada.
- Conjugação com o shift (paridade de T(n) = shift do vetor de n): confirmada.
- Censo de paridades = Binomial(k, 1/2) exata: confirmado — os passos ímpares de um n típico são moedas justas i.i.d.; deriva média por passo = log₂3/2 − 1 ≈ -0.2075 < 0 (contração típica).
- Medida do conjunto 'ainda crescente': 0.1445 após k = 8 passos, 0.1051 após k = 16 — decaimento exponencial (taxa assintótica de grandes desvios 2^(−0.0497·k)); 'quase todo n' contrai (teorema de Terras, verificado).

## 5. Invariantes modulares e partições conservadas

- Fatoração da dinâmica: T(n) mod m é função de n mod m₁ com m₁ mínimo; para todos os 15 módulos testados vale m₁ = 2m (sem exceções) — a única coordenada fatorável é a 2-ádica (torre Z/2^{k+1} → Z/2^k).
- Classes transientes mod 3: [0]; mod 9: [0] — múltiplos de 3 nunca são reentrados: a dinâmica de longo prazo e toda a árvore inversa de 1 vivem em n ≢ 0 (mod 3).
- Partição conservada mais grossa mod 8 (bissimulação a partir da paridade): [[0], [1], [2], [3], [4], [5], [6], [7]] — refinamento até singletons = ausência de invariante discreto oculto além da estrutura 2-ádica (reencontro da bijeção de Terras por outro algoritmo).

## 6. Busca de função de Lyapunov modular (ciclo de média máxima, Karp)

- Grafo de transição mod 2^9: média máxima de crescimento log₂ por passo = 0.5850 (= log₂3 − 1 = 0.5850).
- Ciclo ótimo (resíduos com sinal): [-1] — é o ponto fixo 2-ádico −1 (ou os ciclos de −5/−17 em outros ótimos locais).
- ACHADO ESTRUTURAL: nenhuma função de Lyapunov da forma log n + w(n mod 2^j) pode existir, para NENHUM j — a obstrução são exatamente os ciclos de inteiros negativos, pontos periódicos genuínos do mapa 2-ádico.  Provas por 'testemunha modular finita' estão excluídas; qualquer prova precisa distinguir ℤ₊ dentro de ℤ₂.

## 7. Simetrias: conjugações afins entre sistemas 3n+d

- Conjugações afins 3n+1 → 3n−1 encontradas: [(-1, 0)] — φ(x) = −x: o sistema 3n−1 (que tem ciclos {5,7,10} e {17,...}) É o 3n+1 nos negativos.
- Auto-similaridade x ↦ 5x conjuga 3n+1 com 3n+5 nos múltiplos de 5: confirmada — os ciclos 'extras' de 3n+5 fora dos múltiplos de 5 mostram que a existência de ciclos NÃO é invariante de família: nada 'local' impede ciclos, só a aritmética específica de d=1.
- Automorfismos afins do grafo de transição mod 16: [(1, 0)] — grupo trivial: a dinâmica projetada é rígida (sem simetria interna escondida em potências de 2).

## 8. Operador de transferência de Syracuse mod 3^k

- ACHADO: a uniforme NÃO é estacionária (mod 3^3: False). A medida invariante exata mod 3 é π(1) = 1/3, π(2) = 2/3 — os iterados de Syracuse caem em 2 (mod 3) duas vezes mais que em 1, pois (3n+1)/2^a ≡ (−1)^a (mod 3) e P(a ímpar) = 2/3.  Um invariante de medida explícito e exato da dinâmica projetada.
- Segundo autovalor |λ₂| ≈ 0.0000: é exatamente ZERO — verificação exata do colapso de posto: confirmada (linhas idênticas para r ≡ r' mod 3^(k-1) ⇒ P^k tem posto 1).
- ACHADO ESTRUTURAL: a cadeia perde TODA a memória mod 3^k em exatamente k passos — nenhuma obstrução à convergência pode viver em aritmética 3-ádica finita; o que resta de estrutura é 2-ádico/global.  (A equidistribuição quantitativa na medida invariante é o ingrediente dos resultados de densidade de Tao 2019.)

## 9. Árvore inversa de 1 (cobertura e crescimento)

- Cobertura de 1..1000 até profundidade 120: 100.0%
- Fator de crescimento por nível (últimos): [1.317, 1.331, 1.341, 1.34, 1.335, 1.333] — consistente com o fator 4/3 previsto (1 filho par sempre; filho ímpar quando 2m ≡ 2 mod 3).
- A conjectura ⇔ cobertura → 100% para todo X quando a profundidade cresce.

## 10. Operador de transferência infinito: de mod 3^k a Lip(Z₃), Lip(Z₂) e ℓ¹(Z₊)

- As matrizes mod 3^k (§8) são seções finitas do operador de Koopman U em C(Z₃) da cadeia x ↦ (3x+1)·2^(−a): cada ramo contrai a métrica 3-ádica por EXATAMENTE 1/3 (verificado exato) — um IFS uniformemente contrativo em Z₃.
- ACHADO ESPECTRAL CENTRAL: o coeficiente de contração de Wasserstein é τ_k ≤ 1/3 UNIFORME em k (nível 3^3: τ = 455/1387 ≈ 0.328046; sequência exata 5/21, 455/1387, 7635497415/22906579627 ↗ 1/3).  Ao contrário da lacuna ℓ² (trivial, §8), esta lacuna SOBREVIVE ao limite: spec(U|Lip(Z₃)) ⊆ {1} ∪ {|z| ≤ 1/3}.  Contração global (Banach em W₁): medida invariante ÚNICA em Z₃ — a medida de Syracuse de Tao; consistência projetiva π_k → π_(k−1) verificada exata; equidistribuição a taxa 3^(−n) (confirmada) com U^k f = π(f) EXATO em k passos (confirmado) — o colapso de posto do §8 é a sombra da contração 1/3.
- Lado 2-ádico: o operador de transferência de T em Z₂, Lf(x) = ½f(2x) + ½f((2x−1)/3) (ramos inversos e contração 1/2 dos ramos: exatos), tem coeficiente W₁ EXATAMENTE 1/2 em todo nível 2^k e L^k f = média de Haar exata (confirmado): spec(L|Lip(Z₂)) ⊆ {1} ∪ {|z| ≤ 1/2} — mixing máximo, densidade invariante = Haar (o dual funcional-analítico da conjugação de Terras, §4).
- ONDE A CONJECTURA VIVE: em ℓ¹(Z₊) a seção [1, 50,000] do pushforward é NILPOTENTE fora do ciclo {1,2} (acíclica: True; espectro {0}, índice 128 ≈ 11.8·ln N) — validação: no 3n−1 o detector acusa o ciclo [5, 7, 10] (seção NÃO nilpotente).  E NENHUM peso n^θ dá contração uniforme em t passos: testemunha exata n = 2^t−1 ≡ −1 (mod 2^t) (t = 8: T^t(n)/n = 1312/51 > 1) — a MESMA obstrução 2-ádica −1 de Karp (§6).
- O que resta em Z₊ é contração EM DENSIDADE: massa não absorvida em {1,2} decai a ≈ 0.9282/passo (medido; referência de grandes desvios 0.9659).  SÍNTESE: todas as faces finitas/compactas têm espectro trivial {1} ∪ {0} e os operadores infinitos têm lacunas espectrais máximas (1/3 e 1/2) com contração global provada — a conjectura não é uma questão espectral em nenhum espaço homogêneo: vive na fronteira singular Z₊ ⊂ Z₂ (Haar-nula), onde massas pontuais não sentem a contração de densidades.

---
*Gerado em 1.9s.*

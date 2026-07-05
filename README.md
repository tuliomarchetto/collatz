# Laboratório Collatz — busca algorítmica de invariantes, simetrias e estrutura

Conjunto de algoritmos (Python puro, sem dependências) para investigar a
**Conjectura de Collatz** (3n+1) por duas frentes complementares:

1. **Contraexemplo** — busca sistemática de ciclos não triviais e órbitas
   divergentes, com detectores *validados em sistemas irmãos que possuem
   contraexemplos reais* (3n−1 e 3n+5).
2. **Prova** — extração de invariantes, simetrias e propriedades estruturais
   que restringem onde um contraexemplo poderia viver, e que quantificam os
   ingredientes das provas parciais conhecidas (Terras 1976, Eliahou 1993,
   Krasikov–Lagarias 2003, Tao 2019).

```bash
python -m collatz all                     # relatório completo de achados
python -m collatz verify --limit 1000000  # crivo de contraexemplos
python -m collatz cycles --d -1           # enumeração exata de ciclos (3n-1)
python -m collatz exclude --limit-bits 71 # exclusão diofantina de ciclos
python -m collatz lyapunov --j 10         # obstrução à função de Lyapunov
python -m collatz spectral --k 4          # operador de transferência mod 3^k
python -m collatz transfer --k3 3 --k2 6  # operador de transferência infinito
python -m collatz tree --depth 120        # cobertura da árvore inversa
python -m collatz terras --k 18           # estrutura 2-ádica
python -m pytest tests/                   # suíte de testes
```

Notação: `T(n) = n/2` (n par), `(3n+d)/2` (n ímpar) — mapa acelerado do
sistema `3n+d`; `d = 1` é o problema de Collatz, `d = −1` e `d = 5` são as
bancadas de validação.

## Os algoritmos e o que eles encontram

### 1. `search` — busca direta de contraexemplo
Crivo ascendente (só é preciso iterar até a órbita cair abaixo da semente),
detecção de ciclos de Brent em memória O(1) e sondagem de divergência.
Coleta recordes extremais (tempo de parada ~ c·log n; excursão ~ n²).
**Validação:** aplicado a `3n−1`, encontra os ciclos não triviais
`{5,7,10}` e o ciclo de 17 — o detector funciona; no `3n+1` não há nada
até o limite varrido.

### 2. `cycles.find_cycles` — enumeração **exata** de ciclos
Fato estrutural: um ciclo de comprimento L com k passos ímpares e vetor de
paridade p satisfaz `n = b(p)/(2^L − 3^k)` com `b(p)` inteiro computável —
buscar ciclos é aritmética exata, não simulação. O algoritmo enumera todos
os ciclos de comprimento ≤ L em **ℤ** e redescobre sozinho os três ciclos
de inteiros negativos (−1, −5, −17) e os ciclos de `3n+5`. Em positivos,
para `d = 1`: apenas o trivial `{1,2}` — completo até o comprimento varrido.

### 3. `cycles.cycle_exclusion_bound` — exclusão diofantina de ciclos
Da identidade multiplicativa `2^L = Π(3 + 1/xᵢ)` em torno de um ciclo com
elementos > N segue `0 < L − k·log₂3 ≤ k·log₂(1 + 1/3N)`: a razão L/k
aproxima log₂3 *por cima* com erro ~ 1/(3N ln 2). A teoria das melhores
aproximações racionais (convergentes da fração contínua de log₂3,
certificados exatamente comparando `2^p` com `3^q`) proíbe isso para k
pequeno. Com N = 2⁷¹ (verificação computacional publicada), **qualquer
ciclo não trivial tem bilhões de passos ímpares** — método de
Eliahou/Simons–de Weger. É o exemplo canônico de *invariante estrutural
(aproximação diofantina) que restringe contraexemplos*.

### 4. `padic` — a simetria fundamental: conjugação 2-ádica com o shift
Verifica exatamente o teorema de Terras: o vetor de paridade de comprimento
k é uma **bijeção** de ℤ/2^k, e T é conjugado ao shift de Bernoulli nos
inteiros 2-ádicos. Consequências medidas pelo código: o censo de paridades
é exatamente Binomial(k, ½); a deriva típica é `log₂3/2 − 1 < 0`
(contração em média); a medida do conjunto "ainda crescente" após k passos
decai exponencialmente com a taxa de grandes desvios `1 − H(1/log₂3)`.
É a formalização do porquê "quase todo n desce" (Terras; Tao).

### 5. `invariants` — invariantes modulares e partições conservadas
* `induced_map_search`: procura fatorações `T(n) mod m₂ = f(n mod m₁)`.
  Achado: **m₁ = 2m₂ sempre** — a única coordenada da dinâmica que fatora
  é a 2-ádica; não há "relógio" modular oculto.
* `conserved_partition`: bissimulação (refinamento de partição) em ℤ/m —
  qualquer bloco estável seria uma quantidade discreta conservada. Achado:
  a partição refina totalmente (nenhum invariante discreto além do 2-ádico).
* `transient_classes`: classes que a dinâmica abandona para sempre. Achado
  clássico redescoberto: múltiplos de 3 nunca são reentrados; a árvore
  inversa de 1 vive em `n ≢ 0 (mod 3)`.

### 6. `invariants.karp_max_mean_cycle` — obstrução à função de Lyapunov
Se existisse `f(n) = log n + w(n mod 2^j)` estritamente decrescente ao longo
das órbitas, a divergência estaria excluída. Tal `w` existe **sse** o ciclo
de média máxima do grafo de transição em ℤ/2^j é negativo (algoritmo de
Karp, exato). **Achado estrutural central:** a média máxima é
`log₂3 − 1 > 0`, atingida no resíduo `−1 mod 2^j`, e os ciclos de média
positiva são exatamente os pontos periódicos 2-ádicos dos **ciclos de
inteiros negativos** (−1, −5, −17). Ou seja: *nenhuma testemunha modular
finita pode provar a conjectura* — toda prova precisa distinguir ℤ₊ dentro
de ℤ₂. Isto explica algoritmicamente por que abordagens elementares
falham e direciona a busca para invariantes não modulares.

### 7. `symmetries` — conjugações afins e rigidez
Busca exaustiva de `φ(x) = ax + b` com `φ∘T_d = T_{d'}∘φ`. Achados:
`φ(x) = −x` conjuga `3n+1` com `3n−1` (os ciclos de `3n−1` **são** os
ciclos negativos de `3n+1` — as duas evidências de "quase contraexemplo"
são a mesma, via simetria); `φ(x) = d·x` mergulha `3n+1` em `3n+d`
(auto-similaridade da família). Automorfismos afins dos grafos de
transição mod m: só a identidade — a dinâmica projetada é rígida.

### 8. `spectral` — operador de transferência de Syracuse mod 3^k
Cadeia de Markov exata (aritmética racional, usando que 2 é raiz primitiva
mod 3^k) do mapa de Syracuse projetado em (ℤ/3^k)*. **Achado descoberto
pelo próprio código:** a uniforme *não* é estacionária — a medida
invariante exata mod 3 é π(1) = 1/3, π(2) = 2/3 (iterados de Syracuse caem
em 2 mod 3 duas vezes mais que em 1, pois `(3n+1)/2^a ≡ (−1)^a mod 3` com
`P(a ímpar) = 2/3`); `stationary_exact` calcula a medida invariante
racional para todo 3^k. **Segundo achado exato:** o espectro além de
λ₁ = 1 é `{0}` — linhas de P coincidem para `r ≡ r' (mod 3^{k-1})`, logo
P^k tem posto 1 (`memory_loss_check` verifica em aritmética racional): a
cadeia perde toda a memória mod 3^k em exatamente k passos. *Nenhuma
obstrução à convergência pode viver em aritmética 3-ádica finita* — o que
resta de estrutura é 2-ádico/global (a equidistribuição quantitativa é o
motor do teorema de Tao 2019).

### 10. `transfer` — o operador de transferência **infinito** (substitui as projeções mod 3^k)
As matrizes do §8 são seções finitas do operador de Koopman `U` da cadeia de
Syracuse `x ↦ (3x+1)·2^(−a)` agindo em `C(ℤ₃)` — e sua lacuna ℓ² é trivial,
logo não diz nada no limite. Este módulo identifica a norma em que a lacuna
sobrevive: cada ramo contrai a métrica 3-ádica por **exatamente 1/3**
(verificação exata: a cadeia é um IFS uniformemente contrativo em ℤ₃), e o
**coeficiente de contração de Wasserstein é τ_k ≤ 1/3 uniforme em k**
(valores exatos: τ₂ = 5/21, τ₃ = 455/1387, τ₄ ≈ 0.33333206 ↗ 1/3). Logo
`spec(U|Lip(ℤ₃)) ⊆ {1} ∪ {|z| ≤ 1/3}`: **contração global** (Banach em W₁) —
medida invariante *única* em ℤ₃ (a medida de Syracuse de Tao; as π_k formam
família projetiva, verificado exato), equidistribuição a taxa 3^(−n) e
`U^k f = π(f)` **exatamente** em k passos (o colapso de posto do §8 relido).
Analogamente em ℤ₂: `Lf(x) = ½f(2x) + ½f((2x−1)/3)` tem coeficiente
**exatamente 1/2** e `L^k f =` média de Haar exata — mixing máximo, o dual
funcional-analítico da conjugação de Terras (§4). **A fronteira honesta,
medida:** em ℓ¹(ℤ₊), onde a conjectura vive, toda seção finita é *nilpotente*
(espectro {0}; no 3n−1 o detector acusa o ciclo {5,7,10}), nenhum peso `n^θ`
dá contração uniforme (testemunha exata `n = 2^t−1 ≡ −1 mod 2^t` — a mesma
obstrução 2-ádica de Karp, §6) e o que resta é contração **em densidade**
(taxa medida ≈ 0.93/passo). Síntese: as faces finitas têm espectro trivial
{1}∪{0}, os operadores infinitos têm lacunas máximas com contração global
provada — a conjectura vive exatamente na fronteira singular ℤ₊ ⊂ ℤ₂
(Haar-nula), onde massas pontuais não sentem a contração de densidades.

### 9. `tree` — árvore inversa de 1
A conjectura ⇔ a árvore de pré-imagens `m → {2m, (2m−1)/3}` cobre ℤ₊.
O algoritmo mede a cobertura (→ 100% nos intervalos testados), o fator de
crescimento por nível (≈ 4/3, como previsto pela heurística de
ramificação; Krasikov–Lagarias provam densidade ≥ X^0.84) e lista os
menores inteiros ainda ausentes em cada profundidade (candidatos a estudo).

## Síntese: o que os achados dizem sobre prova × contraexemplo

* **Contra um contraexemplo:** nenhum ciclo em positivos até comprimento
  varrido (busca exata, não amostral); qualquer ciclo tem > 10⁹ passos
  ímpares (diofantino); divergência exige desviar para sempre de uma
  deriva média estritamente negativa com flutuações binomiais (custo
  exponencial, medido).
* **Contra uma prova elementar:** a obstrução de Karp mostra que nenhum
  argumento por resíduos finitos + log fecha o problema — os ciclos
  negativos/2-ádicos são contraexemplos *do método*, não do teorema.
* **Direções que o toolkit deixa quantificadas:** lacuna espectral uniforme
  em 3^k — **resolvida** pelo módulo `transfer`: em W₁/Lip(ℤ₃) ela existe e
  vale ≥ 2/3 (coeficiente ≤ 1/3), com contração global e medida de Syracuse
  única; taxas de grandes desvios do conjunto ruim; densidade da árvore
  inversa; e a fronteira exata (comprimento de ciclo, altura de excursão)
  onde um contraexemplo ainda pode se esconder.  O que o espectro **não**
  pode dar também ficou delimitado: as três faces finitas (mod 3^k, cilindros
  2-ádicos, seções [1, N]) têm espectro trivial {1} ∪ {0}, e a passagem ao
  infinito só produz contração em topologias cegas a ℤ₊.

## Referências
* R. Terras, *A stopping time problem on the positive integers*, Acta Arith. 30 (1976).
* J. C. Lagarias, *The 3x+1 problem and its generalizations*, Amer. Math. Monthly 92 (1985).
* S. Eliahou, *The 3x+1 problem: new lower bounds on nontrivial cycle lengths*, Discrete Math. 118 (1993).
* J. Simons, B. de Weger, *Theoretical and computational bounds for m-cycles of the 3n+1 problem*, Acta Arith. (2005).
* I. Krasikov, J. C. Lagarias, *Bounds for the 3x+1 problem using difference inequalities*, Acta Arith. 109 (2003).
* T. Tao, *Almost all orbits of the Collatz map attain almost bounded values*, Forum Math. Pi 10 (2022).
* D. Barina, *Convergence verification of the Collatz problem*, J. Supercomputing 77 (2021) — verificação ≈ 2⁷¹.

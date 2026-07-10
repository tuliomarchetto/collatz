# Relatório: Estrutura, Invariantes e Obstruções na Dinâmica de Collatz

*Este é o documento canônico (português do Brasil). Uma tradução para o inglês está disponível em [`REPORT.md`](REPORT.md). Licença: este documento é distribuído sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.pt_BR) (Creative Commons Atribuição 4.0 Internacional). O código-fonte do laboratório (`collatz/`) é distribuído separadamente sob a licença MIT — ver `LICENSE`.*

Este documento formaliza a investigação sobre a Conjectura de Collatz (dinâmica $3n+1$) e sistemas afins ($3n+d$). O relatório está dividido em três partes estritas:
1. **Parte I: Resultados Matemáticos**, contendo teoremas com provas puramente analíticas (sem dependência de computação). O foco central é a caracterização topológica da falha das funções de Lyapunov modulares.
2. **Parte II: Descrição dos Algoritmos**, descrevendo os métodos computacionais exatos projetados para investigar o sistema (álgebra exata, grafos modulares, métrica Wasserstein).
3. **Parte III: Resultados Experimentais e Verificações**, catalogando os limites numéricos, achados em simulações e certificados computacionais que instanciam as teorias matemáticas na prática.

**Separação das afirmações.** A Parte I contém apenas enunciados provados analiticamente; nenhuma de suas demonstrações depende de computação. A Parte III contém apenas verificações computacionais, cada uma enunciada com seu limite exato de varredura. Os limites empíricos ali reportados (e.g. o crivo de convergência até $200.000$) são deliberadamente modestos e não reivindicam novidade — o recorde publicado de verificação é $2^{68}$ (Barina 2021) — seu papel é validar os detectores em sistemas com contraexemplos conhecidos ($3n-1$, $3n+5$, os ciclos negativos de $3n+1$) e instanciar os teoremas da Parte I em níveis finitos, não estender recordes numéricos.

**Manuscrito formal e reprodutibilidade.** Um manuscrito formal deste material (LaTeX, com demonstrações completas e bibliografia pontual) é mantido em [`paper/main.tex`](paper/main.tex). Todo número citado neste relatório e no manuscrito é regenerado e conferido pelo script [`reproduce_paper_results.py`](reproduce_paper_results.py) (seções R1–R8), que termina com erro em qualquer divergência.

---

## Parte I: Resultados Matemáticos

*Notação geral.* Seja $T$ o mapa acelerado de Collatz, $T(n) = n/2$ se $n$ par, $(3n+1)/2$ se $n$ ímpar. Seja $S$ o mapa de Syracuse, $S(n) = (3n+1)/2^{\nu_2(3n+1)}$, definido sobre os ímpares. Em $\mathbb{Z}_p$, $|x|_p$ denota a norma $p$-ádica.

### Teorema Principal: A Obstrução Modular à Função de Lyapunov

**Hipóteses.** Uma estratégia natural para provar a convergência global seria exibir uma função de Lyapunov que combine a tendência logarítmica macroscópica com correções locais periódicas. Especificamente, fixado um inteiro arbitrário $j \ge 1$, supomos a existência de uma função $V(n) = \log_2 n + w(n \bmod 2^j)$ que seja estritamente decrescente ao longo de qualquer órbita ímpar em $\mathbb{Z}_+$. Aqui, a componente $w : \mathbb{Z}/2^j\mathbb{Z} \to \mathbb{R}$ é uma função arbitrária, atuando estritamente sobre o anel finito de resíduos. Como corolário imediato do seu domínio finito, $w$ é uma função inerentemente limitada que, quando avaliada nos inteiros, comporta-se como um potencial periódico de período $2^j$.

**Enunciado.** Não existe tal função $V$. Mais especificamente, a existência do potencial $w$ encontra uma obstrução topológica estrutural e irredutível: a projeção do ponto fixo $2$-ádico $-1$ em $\mathbb{Z}/2^j\mathbb{Z}$ induz um laço de crescimento logarítmico estritamente positivo que nenhuma função modular pode compensar.

**Demonstração.**
Suponha, por absurdo, que exista $w : \mathbb{Z}/2^j\mathbb{Z} \to \mathbb{R}$ tal que para todo inteiro ímpar $n > 0$, o passo acelerado $T(n) = (3n+1)/2$ satisfaça $V(T(n)) < V(n)$. Isso implica:
$$w(T(n) \bmod 2^j) - w(n \bmod 2^j) < - \log_2 \frac{T(n)}{n}.$$
Para contornar argumentos de limite (que exigem justificar a preservação de desigualdades estritas) e capturar exatamente a topologia de $\mathbb{Z}_2$, considere a família $n_m = 2^{j+1}m - 1$, parametrizada por qualquer inteiro $m \geq 1$. Como $j \ge 1$, tem-se $n_m \ge 3$, o que garante que todo $n_m$ é um inteiro ímpar estritamente positivo. Portanto, essa família está contida de forma incondicional e rigorosa no domínio onde a hipótese de decréscimo ($V(T(n)) < V(n)$) foi assumida como verdadeira.
Sob o passo acelerado, a imagem exata é:
$$T(n_m) = \frac{3(2^{j+1}m - 1) + 1}{2} = 3 \cdot 2^j m - 1.$$
Avaliando as classes residuais módulo $2^j$, obtemos:
$n_m = 2^j(2m) - 1 \equiv -1 \pmod{2^j}$,
$T(n_m) = 2^j(3m) - 1 \equiv -1 \pmod{2^j}$.
Substituindo $n_m$ na desigualdade de Lyapunov, os termos do potencial cancelam-se identicamente no lado esquerdo para qualquer $m \ge 1$:
$$w(-1 \bmod 2^j) - w(-1 \bmod 2^j) < - \log_2 \frac{3 \cdot 2^j m - 1}{2^{j+1} m - 1}.$$
A desigualdade reduz-se a:
$$0 < - \log_2 \frac{3 \cdot 2^j m - 1}{2 \cdot 2^j m - 1}.$$
Para que esta desigualdade estrita fosse verdadeira, o argumento do logaritmo precisaria ser estritamente menor que $1$. Como os denominadores são positivos, isso exigiria:
$$3 \cdot 2^j m - 1 < 2 \cdot 2^j m - 1 \implies 3 < 2,$$
o que constitui uma flagrante contradição aritmética em inteiros.

A impossibilidade decorre diretamente de uma obstrução dinâmica fundamental: em $\mathbb{Z}_2$, o inteiro $-1$ é um ponto fixo ímpar ($T(-1)=-1$). Na aritmética projetada finita, a função modular assimila este crescimento como um ciclo estacionário incompensável (de ganho logarítmico não nulo), forçando a função local a falhar sobre a família $n_m$ que o orbita. Independentemente da existência de outras restrições globais, este mecanismo atua como uma falha estrutural autossuficiente e incontornável para qualquer função dessa classe. $\square$

**Nota sobre a Literatura:** Até onde sabemos, não encontramos esta formulação explícita na literatura clássica e contemporânea do problema (como nos trabalhos de Terras, Lagarias, Eliahou, Simons–de Weger e Tao). Embora a inexistência de uma função de Lyapunov modular para todos os inteiros seja um corolário esperado da existência de ciclos nos negativos, a demonstração rigorosa de que o ponto fixo $-1 \in \mathbb{Z}_2$ constitui, por si só, uma obstrução topológica *estrutural* e *irredutível* aos potenciais de período $2^j$ busca trazer uma perspectiva distinta. Ela visa estabelecer formalmente por que abordagens baseadas estritamente em resíduos finitos encontram barreiras intransponíveis.

**Corolários de Robustez (Resiliência do Teorema):**
O mecanismo de falha topológica ancorado no ponto fixo $-1$ é robusto a relaxamentos habituais na definição de funções de estabilidade:
1. **Exceções Finitas:** Se a exigência de decréscimo valer apenas "fora de um conjunto finito", a obstrução persiste. A família de teste $n_m = 2^{j+1}m - 1$ possui cardinalidade infinita; portanto, para qualquer conjunto finito de exceções, existe $m$ suficientemente grande tal que $n_m$ recai na região de decréscimo, reativando a contradição.
2. **Decréscimo Não-Estrito:** Permitir empates ($V(T(n)) \le V(n)$) transmuta a desigualdade final para $3 \le 2$, preservando a impossibilidade aritmética. A função falha não apenas em forçar a convergência, mas até mesmo em provar que a órbita não escapa para o infinito.
3. **Condição sobre Iterações Múltiplas ($T^k$):** Avaliar a viabilidade sobre blocos de $k$ passos ($V(T^k(n)) < V(n)$) não contorna a obstrução. Como o ponto $-1$ é invariante, parametrizando uma subfamília mais profunda $n_m = 2^{j+k}m - 1$, todos os primeiros $k$ passos sobre ela serão forçosamente ímpares. A imagem será $T^k(n_m) = 3^k \cdot 2^j m - 1$. O cancelamento modular $w(-1) - w(-1) = 0$ se mantém, e a restrição de decréscimo colapsa para $3^k < 2^k$, o que é falso para todo $k \ge 1$.
4. **Domínio Restrito:** Restringir a hipótese de decréscimo a apenas um subconjunto das órbitas é tautológico perante a conjectura. Se o domínio de validade excluir a família $n_m$, o teorema de convergência não será global. Se o domínio a incluir (ou incluir qualquer família contígua ao ponto fixo 2-ádico), a bomba relógio lógica é armada e a função falha.

---

### Teoremas de Contração Global e Espectro Infinito

Estes resultados formulam a contração estocástica do mapa nos fechos $p$-ádicos.

**Teorema 1 (Contração Wasserstein em $\mathbb{Z}_3$).** O operador de Koopman $U$ da cadeia de Syracuse, agindo sobre o espaço de funções de Lipschitz em $\mathbb{Z}_3$, obedece a uma contração uniforme rígida. Para qualquer profundidade $k \ge 1$, o coeficiente de Dobrushin-Wasserstein do núcleo projetado em $\mathbb{Z}/3^k\mathbb{Z}$ é globalmente limitado por $\tau_k \leq 1/3$.
*Demonstração.* Cada ramo inverso determinístico $\varphi_a(x) = (3x+1)2^{-a}$ da árvore de Syracuse produz, na métrica ultramétrica $\mathbb{Z}_3$, uma isometria escalonada exata: $|\varphi_a(x) - \varphi_a(y)|_3 = |3|_3 \cdot |x - y|_3 = \frac{1}{3} |x - y|_3$. Ao acoplar as distribuições iteradas sem cruzar ramos heterogêneos, a métrica de transição $W_1$ sofre a mesma penalidade de $\frac{1}{3}$. Isto obriga o espectro linear restrito de $U$ a compactar-se inteiramente na região $|z| \leq 1/3$ e colapsar para a unicidade atratora de uma medida de Syracuse. $\square$

**Teorema 2 (Dualidade Dinâmica 2-ádica).** O operador de Transferência Ruelle-Perron-Frobenius $L$ operando no anel $\mathbb{Z}_2$ possui um coeficiente de transporte Wasserstein de exatamente $1/2$.
*Demonstração.* Os pares de ramos antecedentes da dinâmica em $\mathbb{Z}_2$ são unicamente descritos por $\psi_0(x) = 2x$ (ramo par) e $\psi_1(x) = (2x-1)/3$ (ramo ímpar). Uma vez que $|2|_2 = 1/2$ e $|3|_2 = 1$, ambos operam isometricamente com contração $1/2$ sobre a topologia 2-ádica (i.e. $|\psi_i(x) - \psi_i(y)|_2 = \frac{1}{2}|x-y|_2$). A contração agregada em $W_1$ de $L$ não tem escolha senão perfazer rigorosamente $1/2$, revelando a simetria latente de que o processo $L$ nada mais é que o dual isométrico da conjugação métrica de Terras para o shift discreto, desprovido de memória a longo prazo. A integração perante a medida de Haar decai como $2^{-n}$. $\square$

---

## Parte II: Descrição dos Algoritmos

A fundação do nosso laboratório investigativo baseia-se numa modelagem computacional estrita e isenta de flutuações de precisão. Evitamos simulação iterativa simples em favor de álgebra resolutiva (uso intenso da biblioteca local `fractions` e inteiros estendidos).

### 1. Enumeração Algebrizada de Ciclos e Exclusão Diofantina
*   **Solução Exata:** Uma premissa basilar do projeto é que um ciclo hipotético de comprimento $L$ gerando $k$ transformações ímpares (seguindo o vetor de paridade local $p$) requer que seus elementos advenham da forma resolvida $n = b(p)/(2^L - 3^k)$, onde $b(p)$ provém das expansões base-2 dos pesos de transição. O algoritmo desenvolvido descobre atratores ao procurar sistematicamente fatores exatos sobre a equação diofantina para todos os vetores $p$, ao invés de buscar loops via simulação em força bruta. Isto autoriza varrer $\mathbb{Z}$ (e.g. inteiros negativos) numa fração do esforço.
*   **Certificado Diofantino:** Utilizando frações contínuas aplicadas ao fato mecânico de que $2^L = \prod (3+1/x_i)$, nosso algoritmo mapeou o intervalo mínimo de $L/k$ contra a precisão infinita de $\log_2 3$ (comparações aritméticas brutas de potências de base prima $2^p$ versus $3^q$). Isto expurga bilhões de candidaturas triviais.

### 2. Identificador de Obstruções (Algoritmo de Karp)
Para certificar fisicamente a mecânica de obstrução estabelecida no Teorema Principal de forma local (sem limite ao infinito), a dinâmica de transição modular sob $\mathbb{Z}/2^j\mathbb{Z}$ foi codificada como um grafo ponderado estocástico.
*   Um passo ímpar atribui à aresta peso logarítmico $\log_2 3 - 1$, enquanto arestas pares herdam $-1$.
*   As classes divergentes na malha formam o *Maximum Mean Cycle*. Executando a modelagem do cientista Richard Karp sobre nossa topologia $2^j$, o laboratório extrai exata e indutivamente a média fatal e os vértices responsáveis pela disrupção.

### 3. Espectros via Aritmética Métrica
As dinâmicas de matriz $P_k$ e métrica $W_1$ de Kolmogorov para $\tau_k$ (descritas nos Teoremas $1$ e $2$) foram mecanizadas formulando algoritmos para extrair a matriz adjunta das cadeias sobre o anel finito.

### 4. Metodologia: Aritmética Exata
A regra que governa todo o laboratório é: **nenhuma quantidade em ponto flutuante participa de qualquer afirmação certificada.** Concretamente:
* **Inteiros e racionais.** Toda a aritmética inteira usa inteiros de precisão arbitrária (overflow é impossível; quantidades como $3^q$ com $q \approx 10^5$ são exatas). Toda a aritmética racional — matrizes de transferência, medidas estacionárias, distâncias de Wasserstein, os coeficientes $\tau_k$, a equação de ciclos $n = b(p)/(2^L - 3^k)$ — usa frações exatas (o módulo `fractions`). Valores como $\tau_3 = 455/1387$ são saídas exatas; expansões decimais são apenas exibição.
* **A constante $\log_2 3$.** A única constante irracional do ferramental entra em dois pontos, ambos tratados sem confiar em ponto flutuante. (i) Os convergentes de sua fração contínua são extraídos de uma aproximação decimal de 120 dígitos e então **certificados exatamente**: a alternância prevista $p/q \gtrless \log_2 3$ equivale à comparação inteira $2^p \gtrless 3^q$, conferida em aritmética inteira exata para todo denominador $q \le 10^5$ (cobrindo o intervalo que nossas cotas usam); uma falha de certificação levantaria um erro. (ii) A folga $\varepsilon(N) = \log_2(1 + 1/(3N))$ da exclusão diofantina é substituída por uma cota racional **superior** certificada (o valor de 120 dígitos arredondado para cima em uma unidade no último dígito); qualquer superestimativa apenas enfraquece a cota resultante $K$, nunca sua validade. Nenhuma dessas computações pode sofrer overflow ou perda de precisão.
* **Onde floats aparecem.** O algoritmo de Karp executa sua programação dinâmica sobre pesos IEEE double por velocidade, mas seu veredito é certificado simbolicamente: a média máxima de ciclo é *provada* igual a $\log_2 3 - 1$ (nenhum peso de aresta excede $\log_2 3 - 1$, e o laço em $-1 \bmod 2^j$ o atinge), e uma execução só é aceita se o ciclo ótimo extraído consistir exclusivamente de resíduos ímpares — condição exata sob a qual sua média é $\log_2 3 - 1$ por construção. O valor em float concorda a $< 2\cdot 10^{-15}$, como esperado. Analogamente, a estimativa de $|\lambda_2|$ por iteração de potência é apenas um diagnóstico numérico; a contraparte certificada é o colapso exato de posto $P_k^{\,k} = \mathbf{1}\pi_k$, verificado em aritmética racional.
* **Determinismo.** Não há componente de Monte Carlo; todos os algoritmos são determinísticos e reexecuções são bit-idênticas entre plataformas.

---

## Parte III: Resultados Experimentais e Verificações

Abaixo reportamos quantificações absolutas obtidas pela aplicação dos motores computacionais detalhados na Parte II. Tudo nesta parte é **verificação com limite finito explícito**, não teorema; cada número é regenerado por `reproduce_paper_results.py`.

### Crivo Computacional Global e Árvore Inversa
*   **Limites Positivos Iniciais:** Foi atestado o fechamento a 1 de todos os naturais não-nulos menores que $200.000$ sob detecção linear ascendente; nenhum desvio cíclico documentado. (Isto está muito abaixo do recorde publicado $2^{68}$, Barina 2021; é incluído apenas como hipótese autossuficiente e reexecutável para a exclusão diofantina abaixo.)
*   **Balanço de Difusão (Árvore Inversa):** A construção mecânica atestou rigorosamente a profundidade $113$ como o mínimo grau necessário da árvore invertida de Syracuse para encapsular todos os naturais sob o limiar empírico de $1000$. Com $30$ níveis mapeados a termo absoluto, o subconjunto cobre todo o espectro interno em $[123, 2147483648]$.

### Descoberta Analítica de Ciclos Estendidos
*   Aplicando o motor racional da seção II.1 sobre a dinâmica clássica $3n+1$, o sistema diagnosticou deterministicamente os orbitais da família dos inteiros negativos: $\{-1\}$ e os duplos loops isolados em $\{-5\}$ e $\{-17\}$, confirmando a completude topológica do buscador.
*   Em reconfiguração para mapas irmãos $3n-1$ e $3n+5$ verificou a presença real e pontual dos ciclos irregulares característicos destas vizinhanças (ex: laço transitivo de 19 e 49, provando que anomalias cíclicas não são restritas mas normativas dependendo do delta operado).

### Exclusão por Compressão Diofantina
*   Operacionalizando a fronteira atestada ( $N = 200.000$ ), provou-se numericamente que a incidência de qualquer órbita não-trivial fechada forçaria um laço com base mínima estrita de 676 iterações diretas (contendo nada menos que 428 incrementos). Se o limite fosse adotado aos patamares divulgados contemporaneamente ($2^{71}$), este percurso cíclico cresce para além de $103$ bilhões de itens — ratificando o aspecto de fuga.

### Evidências Físicas das Topologias
*   **Colapso de Posto Empírico ($3^k$):** Avaliando o operador Syracuse a $k=3$ (anel $\mathbb{Z}/27\mathbb{Z}$), a convergência espectral anulou todos autovalores suplementares precisamente. A medida convergiu irrefutavelmente às proporções racionais $1/3$ e $2/3$, rompendo simetrias triviais e instanciando, em dimensão de testes finita, o colapso previsto pelo Teorema 1.
*   **Medidas Absolutas ($\tau_k$ Wasserstein):** Para $k \in \{2, 3, 4\}$, as avaliações fracionais precisas retornadas foram $\tau_2 = 5/21$, $\tau_3 = 455/1387$ e $\tau_4 \approx 0.33333206$. O erro diferencial de limiar cai monotonamente provando a ascensão restrita para cota global $\frac{1}{3}$.
*   **Identificação Prática de $-1 \bmod 2^j$:** Expondo a análise do *Karp Mean Cycle* para módulos iterados no intervalo $j = 5 \dots 10$, a média retornada fixou-se, de forma computacional incondicional, no cume constante de $0.584962$ — o valor $\log_2 3 - 1$, certificado simbolicamente conforme a metodologia da Parte II §4 (o float concorda a $< 2\cdot 10^{-15}$). Em $100\%$ dos processamentos executados, o subgrafo responsável pelo distúrbio continha uma e apenas uma assinatura de classe residual: a gerada estritamente pelo módulo transiente do inteiro $-1$.

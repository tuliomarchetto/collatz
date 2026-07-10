Para que este projeto transcenda o status de um "repositório brilhante de código" e seja aceito como uma **publicação científica válida** (em periódicos como *Mathematics of Computation*, *Journal of Number Theory* ou repositórios como o *arXiv*), ele precisa passar por um refinamento focado em **formalismo, reprodutibilidade e documentação rigorosa**. 

Aqui estão as principais melhorias e passos necessários:

### 1. Transição para Formato Acadêmico Formal (LaTeX)
O arquivo `RELATORIO.md` é excelente para um repositório, mas revistas científicas exigem manuscritos formais.
* **O que fazer:** Escrever o documento em **LaTeX** seguindo o rigor matemático clássico (com seções claras para *Abstract, Introduction, Definitions, Lemmas, Theorems e Proofs*).
* **Bibliografia Exata:** O relatório menciona vagamente "Terras, Lagarias, Eliahou, Simons–de Weger e Tao". Cientificamente, você precisa de citações formais pontuais (ex: listar o artigo de Tao de 2019 sobre resultados parciais, o artigo de Terras de 1976 sobre a distribuição 2-ádica, etc.) para ancorar seu trabalho na literatura existente.

### 2. Reprodutibilidade Computacional Inquestionável
Revistas de matemática rigorosa são extremamente céticas com provas baseadas em computação. Qualquer revisor exigirá que seu código seja fácil de rodar e valide perfeitamente os achados.
* **Limpeza dos Scripts Soltos:** Vi que o repositório tem arquivos como `scratch.py`, `scratch2.py` e `scratch3.py`. Para a submissão, agrupe esses experimentos em um único script de interface clara, como `reproduce_paper_results.py` ou `generate_tables.py`, que cuspa exatamente os números que estarão no seu artigo em LaTeX.
* **Ambiente Controlado:** Notei mais cedo que faltou a dependência do `pytest` no ambiente para rodar os testes. Um projeto científico de software precisa de um arquivo `requirements.txt`, um `pyproject.toml` ou um `Makefile` que garanta que qualquer cientista consiga instalar e rodar os testes sem erros de ambiente.
* **Integração Contínua (CI):** Usar o GitHub Actions para rodar a suíte do `/tests` automaticamente prova que seu laboratório computacional é funcional em máquinas neutras.

### 3. Defesa do Rigor Numérico (Aritmética Exata)
Você menciona no relatório que usou "álgebra exata e isenta de flutuações de precisão" (via `fractions` e inteiros estendidos). Isso é fantástico, mas **precisa ser detalhado na metodologia do artigo**. 
* **O que fazer:** Dedique um parágrafo no artigo matemático para explicar que as aproximações de $\log_2(3)$ no Algoritmo de Karp e no Coeficiente de Wasserstein ($\tau_k \le 1/3$) não sofrem de estouro de ponto flutuante (*float overflow/precision loss*). Deixe claro que as provas computacionais operam em estruturas exatas em Python.

### 4. Clareza entre "Teorema" vs. "Verificação"
É essencial que o artigo separe claramente o que é uma prova matemática absoluta do que é uma verificação empírica:
* A prova de que **não existe função de Lyapunov modular baseada no resíduo -1** é um achado topológico/analítico puro. A computação do Algoritmo de Karp é apenas a "Validação Experimental" desse fato. 
* O projeto deve focar seu "peso de novidade" nas provas teóricas da Parte I. Os limites empíricos (como verificar até 200.000) não são novos (a literatura já checou até $2^{68}$ ou mais), então a computação do seu projeto serve para *comprovar a estrutura teórica* (como a árvore inversa), e não para tentar quebrar o recorde numérico.
---

## Status (2026-07-10) — todos os itens implementados

1. **LaTeX formal** → `paper/main.tex` (amsart: Abstract, Introduction, Definições, Lemas, Teoremas e Provas completas; 18 pp., compila sem erros) + `paper/references.bib` com citações pontuais (Terras 1976, Lagarias 1985, Eliahou 1993, Krasikov–Lagarias 2003, Simons–de Weger 2005, Tao 2022, Barina 2021, Karp 1978, Khinchin 1964, Villani 2009, Wirsching 1998). Compilar com `make paper`.
2. **Reprodutibilidade** → `scratch*.py` removidos e consolidados em `reproduce_paper_results.py` (regenera e *confere* todo número citado no artigo/relatório; sai com erro em divergência; ~2 s). Ambiente controlado: `pyproject.toml`, `requirements.txt`, `Makefile` (o `pytest` agora importa o pacote sem instalação). CI: `.github/workflows/ci.yml` roda a suíte (66 testes) em Linux/macOS, CPython 3.9–3.13, mais o script de reprodução.
3. **Rigor numérico** → seção "Methodology: exact arithmetic" no artigo (§6) e "Metodologia: Aritmética Exata" na Parte II §4 de `RELATORIO.md`/`REPORT.md`: convergentes de log₂3 certificados por comparação inteira 2^p vs 3^q, folga ε(N) por cota racional superior certificada, veredito de Karp certificado simbolicamente (floats só como diagnóstico).
4. **Teorema vs. Verificação** → separação explícita no artigo (§1.2, §7, §8) e no relatório (preâmbulo "Separação das afirmações" + rótulos na Parte III); o peso de novidade fica nas provas da Parte I; os limites empíricos são declarados como verificações modestas (recorde da literatura: 2^68, Barina).

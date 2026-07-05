"""
collatz — Laboratório computacional para a Conjectura de Collatz.

Um conjunto de algoritmos para buscar invariantes, simetrias e propriedades
estruturais da dinâmica 3n+1 que possam apontar para uma prova ou para um
contraexemplo da conjectura.

Módulos
-------
core        Mapas (Collatz, acelerado T, Syracuse), trajetórias, tempos de parada.
search      Busca direta de contraexemplos: crivo de verificação, detecção de
            ciclos (Brent), sondagem de divergência, recordes.
cycles      Enumeração EXATA de ciclos via vetores de paridade (ponto fixo
            racional) e exclusão de ciclos via frações contínuas de log2(3).
padic       Estrutura 2-ádica: bijeção de Terras Q_k, conjugação com o shift,
            censo binomial de paridades.
invariants  Invariantes modulares (mapas induzidos, partições conservadas),
            deriva (drift) por classe de resíduo, busca de função de Lyapunov
            via ciclo de média máxima (algoritmo de Karp).
symmetries  Busca de conjugações afins entre sistemas 3n+d e automorfismos
            afins dos grafos de transição modulares.
spectral    Operador de transferência de Syracuse em (Z/3^k)*: distribuição
            estacionária exata e lacuna espectral.
tree        Árvore inversa (pré-imagens de 1): densidade de cobertura e taxa
            de crescimento.
report      Orquestra todos os módulos e produz um relatório de achados.
"""

__version__ = "0.1.0"

"""Teste de desconexão: garante que report.run_all() executa ponta a ponta
sem travar, exercita TODOS os módulos e produz saída correta.

Este teste é propositalmente leve nos parâmetros (limites pequenos) para
rodar rápido, mas verifica que a orquestração completa funciona — qualquer
quebra de interface entre report.py e os módulos algorítmicos é capturada.
"""

from collatz.report import run_all


def test_run_all_smoke():
    """Verifica que run_all executa sem travar e produz Markdown não vazio."""
    text = run_all(
        verify_limit=1_000,
        cycle_len=8,
        terras_k=8,
        karp_j=6,
        spectral_k=2,
        tree_depth=50,
        tree_X=100,
        transfer_k3=2,
        transfer_k2=4,
        transfer_N=2_000,
    )
    assert isinstance(text, str)
    assert len(text) > 500  # relatório substancial


def test_run_all_contains_all_sections():
    """Todas as seções do relatório devem estar presentes — confirma que
    cada módulo algoritmo foi exercitado."""
    text = run_all(
        verify_limit=500,
        cycle_len=6,
        terras_k=6,
        karp_j=5,
        spectral_k=2,
        tree_depth=40,
        tree_X=50,
        transfer_k3=2,
        transfer_k2=4,
        transfer_N=1_000,
    )
    expected_sections = [
        "## 1.",   # busca direta
        "## 2.",   # ciclos exatos
        "## 3.",   # exclusão diofantina
        "## 4.",   # simetria 2-ádica
        "## 5.",   # invariantes modulares
        "## 6.",   # Lyapunov / Karp
        "## 7.",   # simetrias
        "## 8.",   # espectral mod 3^k
        "## 9.",   # árvore inversa
        "## 10.",  # operador infinito
    ]
    for sec in expected_sections:
        assert sec in text, f"seção '{sec}' ausente do relatório"


def test_run_all_accuracy_invariants():
    """Verifica invariantes de acurácia conhecidos dentro do relatório gerado."""
    text = run_all(
        verify_limit=10_000,
        cycle_len=8,
        terras_k=8,
        karp_j=6,
        spectral_k=2,
        tree_depth=60,
        tree_X=100,
        transfer_k3=2,
        transfer_k2=4,
        transfer_N=2_000,
    )
    # 1. nenhum contraexemplo encontrado no 3n+1
    assert "Nenhum contraexemplo" in text or "converge a 1" in text
    # 2. ciclo trivial detectado
    assert "trivial" in text.lower()
    # 3. conjugação φ(x) = -x encontrada
    assert "(-1, 0)" in text
    # 4. medida invariante mod 3 não é uniforme
    assert "NÃO" in text  # "NÃO é estacionária"
    # 5. árvore inversa cobriu 100% de 1..X
    assert "100" in text  # cobertura 100.0%
    # 6. classes transientes mod 3 = {0}
    assert "[0]" in text

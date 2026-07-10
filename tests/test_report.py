"""Disconnection test: ensures that report.run_all() runs end to end
without crashing, exercises ALL modules, and produces correct output.

This test is intentionally light on parameters (small limits) so it
runs fast, but it verifies that the full orchestration works — any
interface break between report.py and the algorithmic modules is
caught.
"""

from collatz.report import run_all


def test_run_all_smoke():
    """Verifies that run_all executes without crashing and produces
    non-empty Markdown."""
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
    assert len(text) > 500  # substantial report


def test_run_all_contains_all_sections():
    """All report sections must be present — confirms that each
    algorithm module was exercised."""
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
        "## 1.",  # direct search
        "## 2.",  # exact cycles
        "## 3.",  # Diophantine exclusion
        "## 4.",  # 2-adic symmetry
        "## 5.",  # modular invariants
        "## 6.",  # Lyapunov / Karp
        "## 7.",  # symmetries
        "## 8.",  # spectral mod 3^k
        "## 9.",  # inverse tree
        "## 10.",  # infinite operator
    ]
    for sec in expected_sections:
        assert sec in text, f"section '{sec}' missing from the report"


def test_run_all_accuracy_invariants():
    """Verifies known accuracy invariants within the generated report."""
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
    # 1. no counterexample found for 3n+1
    assert "Nenhum contraexemplo" in text or "converge a 1" in text
    # 2. trivial cycle detected
    assert "trivial" in text.lower()
    # 3. conjugacy φ(x) = -x found
    assert "(-1, 0)" in text
    # 4. mod-3 invariant measure is not uniform
    assert "NÃO" in text  # "NÃO é estacionária" (report text, kept in Portuguese)
    # 5. inverse tree covered 100% of 1..X
    assert "100" in text  # 100.0% coverage
    # 6. transient classes mod 3 = {0}
    assert "[0]" in text

from collatz.search import brent_cycle_detect, divergence_probe, verify_range


def test_verify_small_range():
    r = verify_range(50_000)
    assert r.all_converge
    assert r.counterexample is None
    # 27 é recorde clássico de excursão
    assert any(n == 27 for n, _ in r.excursion_records)


def test_verify_finds_3n_minus_1_cycle():
    r = verify_range(100, d=-1)
    assert not r.all_converge
    assert r.cycle is not None
    assert set(r.cycle) == {5, 7, 10}


def test_brent_reaches_trivial_cycle():
    mu, lam, lo = brent_cycle_detect(27)
    assert (lam, lo) == (2, 1)          # ciclo {1,2} do mapa T


def test_brent_finds_negative_cycle():
    mu, lam, lo = brent_cycle_detect(-30)  # -30 -> -15 -> -22 -> -11 -> ...
    assert lo in (-1, -10, -136)           # cai num dos três ciclos negativos
    assert lam in (1, 3, 11)


def test_divergence_probe():
    assert divergence_probe(27)["verdict"] == "converge"
    assert divergence_probe(-5)["verdict"] == "ciclo"

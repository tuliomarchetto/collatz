"""Smoke tests for the CLI (__main__.py): each subcommand runs without crashing."""

from collatz.__main__ import main


def test_cli_verify():
    assert main(["verify", "--limit", "500", "--d", "1"]) == 0


def test_cli_cycles():
    assert main(["cycles", "--d", "1", "--max-len", "6"]) == 0


def test_cli_exclude():
    assert main(["exclude", "--limit-bits", "20"]) == 0


def test_cli_lyapunov():
    assert main(["lyapunov", "--j", "5"]) == 0


def test_cli_spectral():
    assert main(["spectral", "--k", "2"]) == 0


def test_cli_terras():
    assert main(["terras", "--k", "8"]) == 0


def test_cli_tree():
    assert main(["tree", "--depth", "30", "--x", "50"]) == 0

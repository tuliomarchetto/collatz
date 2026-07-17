# Reproducibility entry points for the Collatz laboratory.
#
#   make install     — install the package and test dependencies
#   make test        — run the full test suite
#   make reproduce   — regenerate every number quoted in the paper/report
#   make report      — regenerate the integrated findings report (Portuguese)
#   make paper       — compile the LaTeX manuscript (requires latexmk)
#   make note        — compile the 2-page extraction notes (PT and EN)

PYTHON ?= python3

.PHONY: install test reproduce report paper note clean

install:
	@echo "Creating virtual environment and installing..."
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -e ".[test]"
	@echo "Done. Virtual environment created at .venv/"

test:
	@if [ -d ".venv" ]; then .venv/bin/pytest tests/ -q; else $(PYTHON) -m pytest tests/ -q; fi

reproduce:
	$(PYTHON) reproduce_paper_results.py

report:
	$(PYTHON) -m collatz all

paper:
	cd paper && tectonic main.tex

note:
	cd note && tectonic nota-obstrucao-lyapunov-pt.tex && tectonic lyapunov-obstruction-en.tex

clean:
	rm -rf build dist *.egg-info collatz/__pycache__ tests/__pycache__ .pytest_cache
	cd paper 2>/dev/null && latexmk -C main.tex 2>/dev/null || true

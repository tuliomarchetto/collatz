# Reproducibility entry points for the Collatz laboratory.
#
#   make install     — install the package and test dependencies
#   make test        — run the full test suite
#   make reproduce   — regenerate every number quoted in the paper/report
#   make report      — regenerate the integrated findings report (Portuguese)
#   make paper       — compile the LaTeX manuscript (requires latexmk)

PYTHON ?= python3

.PHONY: install test reproduce report paper clean

install:
	$(PYTHON) -m pip install -e ".[test]"

test:
	$(PYTHON) -m pytest tests/ -q

reproduce:
	$(PYTHON) reproduce_paper_results.py

report:
	$(PYTHON) -m collatz all

paper:
	cd paper && tectonic main.tex

clean:
	rm -rf build dist *.egg-info collatz/__pycache__ tests/__pycache__ .pytest_cache
	cd paper 2>/dev/null && latexmk -C main.tex 2>/dev/null || true

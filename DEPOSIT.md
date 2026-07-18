# G9 — Deposit checklist (Zenodo DOI + arXiv)

*Prepared under Tier 2 G9. The actual upload requires the author's Zenodo and
arXiv accounts; this file freezes what to deposit and where the DOI is wired.*

## What gets frozen

Archive **one tagged git state** that contains, at minimum:

| Path | Role |
|------|------|
| `collatz/` | pure-stdlib laboratory |
| `tests/` | pytest suite |
| `reproduce_paper_results.py` | R1–R9 certificate script |
| `paper/main.tex`, `paper/references.bib`, `paper/residue_graph_j4.tex`, `paper/make_residue_graph_figure.py` | manuscript + generated figure sources |
| `REPORT.md`, `RELATORIO.md` | bilingual formal report |
| `README.md`, `LICENSE`, `CITATION.cff`, `pyproject.toml` | packaging / citation |
| `LITERATURE_REVIEW.md` | bibliographic log |

Optional but recommended: the built `paper/main.pdf` (or rebuild on deposit via
`make paper`) and a short `RELEASE_NOTES.md` listing the git tag SHA.

## Steps at submission (or acceptance)

1. **Tag the repository.**
   ```bash
   git tag -a v1.0.0-submission -m "Frozen state for journal / arXiv submission"
   git push origin v1.0.0-submission
   ```
2. **Zenodo.** Connect the GitHub repo (or upload a zip of the tag). Request a
   DOI. Prefer "Concept DOI" + version DOI; cite the version DOI in the paper.
3. **Fill `CITATION.cff`.** Uncomment / set
   ```yaml
   identifiers:
     - type: doi
       value: 10.5281/zenodo.XXXXXXXX
   ```
   and bump `version` / `date-released` to match the deposit.
4. **Update the paper.** In `paper/main.tex`, section *Data and code
   availability*, replace the placeholder sentence with the concrete DOI
   (and arXiv identifier once issued). Mirror the same sentence in
   `REPORT.md` / `RELATORIO.md` if they quote the availability statement.
5. **arXiv.** Deposit `paper/main.tex` (+ bib, figure sources, and any
   generated TikZ the build needs) under primary `math.NT`, cross-list
   `math.DS`. Use the Experimental Mathematics positioning from G3. After
   the identifier appears (e.g. `arXiv:26XX.XXXXX`), add it to
   `CITATION.cff` as a second identifier and to the paper front matter.
6. **Cross-link.** README badge or one-line "Cite this" block pointing at
   Zenodo + arXiv; keep GitHub the live development URL.

Files involved: `CITATION.cff` (this repository root), `DEPOSIT.md` (this
checklist), `paper/main.tex` §Data and code availability.

## What this deposit is *not*

- Not a claim of novelty beyond what the manuscript already scopes.
- Not a substitute for the journal's own data policy; Experimental
  Mathematics (T&F) is format-free at submission — the Zenodo DOI is the
  citable artifact for the code + reports.

## Status

- [x] `CITATION.cff` scaffold committed
- [x] Data-and-code availability section mentions Zenodo / arXiv path
- [ ] Tag + Zenodo upload (author action at submission)
- [ ] arXiv upload (author action at submission)
- [ ] DOI wired into `main.tex` / `CITATION.cff` / reports

# AGENTS.md

Guidance for Codex (and any AI agent) working in this repository.

## Purpose of this project

This is a **scientific research project** investigating the Collatz Conjecture
(3n+1) and affine sibling systems (3n+d), combining:
- exact computational algorithms (`collatz/`), and
- a formal mathematical report (`RELATORIO.md` / `REPORT.md`) intended for
  publication in a scientific journal.

Treat this codebase with the rigor expected of a paper under peer review, not
a typical software project.

## Language policy

- **Code, comments, and docstrings: always English.** Every `.py` file,
  every `#` comment, every docstring, every CLI help/print string must be
  written in English — regardless of the language used in the conversation
  with the user.
- **The report exists in two languages, kept in sync:**
  - `RELATORIO.md` — canonical, Brazilian Portuguese.
  - `REPORT.md` — English translation.
  Whenever one is edited with a substantive change (new theorem, new
  finding, corrected claim, updated numeric result), the other **must** be
  updated to match in the same turn. Do not let them drift apart.
- Never introduce Portuguese into `collatz/` or `tests/` source, and never
  introduce code-style shortcuts (variable names, log messages, etc.) in
  Portuguese.

## Scientific standard — non-negotiable

- **Every mathematical claim must be proved, not asserted.** If a change
  adds or modifies a theorem, invariant, bound, or structural claim in the
  report, it must include a complete, checkable proof (or an exact
  reference to the established literature it relies on, e.g. Terras 1976,
  Eliahou 1993, Krasikov–Lagarias 2003, Tao 2019, Barina 2021).
- **Every computational finding must be exact or explicitly labeled as
  numerical/heuristic.** This project favors exact arithmetic (`fractions`,
  arbitrary-precision integers, closed-form solutions) over floating-point
  simulation. If a result is empirical (e.g. "verified up to N"), say so
  explicitly and state the limit — never present a swept range as a proof
  of the general case.
- **No hand-waving.** Do not write proof sketches, "it can be shown that",
  or unjustified leaps as if they were complete. If a step is genuinely
  open or conjectural, label it as such.
- **Clarity for humans is a hard requirement, not a nice-to-have.** A
  theorem or algorithm description is not done when it is technically
  correct — it is done when a mathematician outside this project can read
  it and follow every step. Prefer explicit notation, define every symbol
  on first use, and avoid unnecessary abstraction.
- **Reproducibility.** Any new algorithm or numerical claim added to the
  report should be backed by code in `collatz/` (or a documented, rerunnable
  procedure) so a reviewer can independently verify it — do not report
  numbers that cannot be regenerated.

## Practical implications

- When adding a new finding to the toolkit, update `README.md`'s "algorithms
  and what they find" section, and add a corresponding, mathematically
  justified entry to `RELATORIO.md`/`REPORT.md` if it is report-worthy.
- When touching `collatz/report.py`, remember: the strings built inside
  `run_all()` are the actual Portuguese-language report body mirrored in
  `RELATORIO.md` — keep them in Portuguese; only comments/docstrings in that
  file are English.
- Prefer exact rational/integer arithmetic over floats whenever a claim in
  the report depends on the result.

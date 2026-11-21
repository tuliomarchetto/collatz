# Collatz research audit using Lacuna

## Repair status (working tree)

The findings below describe the original audited commit. Repairs have now been applied without a commit or push:

- Fixed all four utility issue classes. The ten exact audit cases now have zero discrepancies.
- Added 13 utility regressions and 11 certificate/scope tests; full suite now passes 128 tests.
- Corrected the exact-boundary walk definition and supremum proof, allowing even terminal vertices.
- Removed invalid uniform-gap proofs; explicitly marked the unproved bounds and dependent converse conditional/conjectural rather than claiming to close the open argument.
- Corrected unrestricted non-strict potential claims and hitting-time sign; synchronized REPORT.md and RELATORIO.md with paper/main.tex and versioned historical REVIEW.md assurances.
- Added integer-only cylinder descent certificates, independently checked for every binary word of lengths 1–7. They distinguish coefficient contraction from actual descent and do not prove global rule coverage.
- Retired the former unconditional boolean theorem certificate; calling it now raises an explicit NotImplementedError.

Integration verification: 128 passed in 96.89 seconds; all quoted numerical results reproduced exactly again (10.5 seconds); git diff --check passed. Lacuna's real library parser now reports 91.20% line coverage (previously 90.36%); the combined branch-aware score rounds to 89%. Remaining sub-90%-line files are __main__.py, core.py and density.py. Evidence: gap-test-results.log, gap-reproduction.log, lacuna-python-analysis.json and research-edge-audit.json.

Remaining open: the length-free uniform gap, its reverse characterization, global coefficient stopping-rule coverage/descent, and a quantitative stochastic-to-deterministic bridge. The revised LaTeX source has structural checks but has not been PDF-compiled; no TeX engine is installed. The previously checked Lean arithmetic core is unchanged and does not certify the newly repaired walk theorem.

## Scope and verified baseline

Reviewed Collatz commit `0fbb610e524101d1ad9ab413b61b223e57636e5c` and installed Lacuna 0.6.2 from commit `88a8d18`. This is a computational audit and research-direction review, not a proof of Collatz or an exhaustive peer review.[1][2]

- Installed the editable Python package in `.venv`, pytest 8.4.2, pytest-cov 7.1.0 and coverage 7.10.7. Python is 3.9.6.
- `make install` initially failed because the system venv bundled pip 21.2.4, which cannot perform this editable pyproject installation. Upgrading pip inside the venv resolved it.
- Full test suite: 104 passed in 95.35 seconds (`test-audit.log`).
- Full `reproduce_paper_results.py`, without `--quick`: exit 0, all quoted results reproduced exactly (`reproduction-audit.log`; 10.5 seconds).
- Installed elan and Lean 4.24.0. The default pure-stdlib companion builds successfully (`lean-audit.log`). The optional mathlib real/logarithm formalization was not enabled or checked.
- Manuscripts and research source code remain unchanged. No commits or remote writes were made.

## Important Lacuna limitation

The unmodified `lacuna analyze` command produced 0% coverage, no gaps and exit 1 without executing the Python tests. That result in `lacuna-analysis.json` is INVALID for this checkout, not evidence of zero coverage. `src/lib/coverage/gaps.ts:60,181-195` recognizes only JS/TS extensions during test discovery, and its testable-code recognizer at lines 65-95 is JS-oriented. Python runner support does not currently make the entire discovery pipeline Python-aware.[1]

To actually use Lacuna on this project, `lacuna-python-audit.mjs` imports the unmodified built `parseLcov` and `extractGaps` functions. pytest-cov supplies the real Python LCOV. This bypasses discovery and content filtering without modifying Lacuna or translating Python to JS. Run:

```sh
cd /Users/tulio/Projects/collatz
.venv/bin/python -m pytest --cov=collatz --cov-branch --cov-report=lcov:coverage/lcov.info --cov-report=json:coverage/coverage.json --cov-report=term-missing -q
node lacuna-python-audit.mjs
```

The library result is `lacuna-python-analysis.json`: 90.36% line coverage and 96.69% function coverage. Coverage.py's combined statement/branch score rounds to 88%; these are different metrics, not contradictory measurements. Lacuna's LCOV parser does not measure branch coverage. No LLM generation was used and no code was sent to a model provider.

## Critical mathematical findings from the independent review

These findings take priority over improving test coverage. The parent independently read the cited manuscript passages and executed the finite witnesses. Passing reproduction and Lean arithmetic checks do not validate these later theorems.

1. **The exact-boundary theorem is false with its current walk definition.** `paper/main.tex:547` requires every vertex, including the endpoint, to be odd, while the theorem at line 561 requires descent for every constrained odd source even if its image is even. Define a schedule only on `n_j = 2^(2j)-1`, with `sigma(n_j)=2j+1`, and infinity elsewhere. Its endpoints are `(3^(2j)-1)/2`, which are even. Thus there are no nonempty walks in the defined odd-only graph and Lambda=0. Yet the one-block ratios `(3^(2j)-1)/(2*(2^(2j)-1))` tend to infinity. A bounded correction cannot compensate these ratios: descent would require every log-ratio to be at most its finite oscillation. Executed first ratios: 4/3, 8/3, 52/9, 656/51, 2684/93. Allow arbitrary positive terminal vertices, constrain only the sources, define empty walks on all positive integers, and reprove the statement. The code already permits terminal even endpoints (`stopping.py:868-890`).

2. **The uniform-gap proof contains invalid steps and an acknowledged missing infinite argument.** At line 417 the manuscript equates `(2/3)m+(2/3)m` with `m`; it is `4m/3`. At lines 437-439 it substitutes a lower bound for `2^k` into a positive term as though it were an upper bound. Lines 474-488 accept an infinite family via finite checks through k<=40 while explicitly acknowledging that a length-free closure is open. Line 527 also asserts an admissibility inequality that fails for n=7,L=6: its parity is 111010, a=4, q=0,m0=11, but 7 < 32/3. These are proof defects, not demonstrated counterexamples to the uniform bound itself. Treat the affected lemmas and downstream characterization direction as conditional until repaired, and audit every dependent assertion in both report languages.

3. **Unrestricted corrections mix strict and non-strict descent.** The requirement at line 241 is non-strict. Without boundedness, `w(n)=-log2(n)` makes V identically zero for every schedule, regardless of cycles, contradicting the unrestricted-class iff assertion at line 329. The proposed potential `-epsilon * total_stopping_time` at line 246 also has its sign reversed: remaining stopping time decreases, so its negative increases. Separate strict and non-strict results and state exception sets explicitly.

4. **Residual-rule classification needs a narrower statement.** Excluding unbounded expansion is not the same as proving every surviving schedule has nonpositive coefficient gain. Separate coefficient contraction, actual affine descent, schedule coverage, and cumulative gain. For an admissible contracting word, actual descent is exactly `b <= (2^L-3^a)*n`; this supplies a concrete exact-cylinder research program rather than an inference from coefficient labels alone.

The existing modest claims about randomized transfer operators should remain model-specific. A deterministic bridge would need an explicit sampled integer ensemble, horizon, dependence error and exceptional mass. Also version the referee/novelty reviews: assurances about earlier theorem inventories do not cover the present stopping-time package.

No mathematical manuscript edits were made. Any repair must keep REPORT.md and RELATORIO.md synchronized under AGENTS.md.

## Priority 1: fix verified boundary and density errors

The separate executable `research-edge-audit.py` produces `research-edge-audit.json`. Ten checks include eight contract discrepancies across the following issue classes; these are small exact reproductions, not speculative concerns.

1. **Total-stopping-time budget is off by one.** `core.py:103-110` and `density.py:169-176` check for arrival only before each iteration. Seed 2 reaches 1 in exactly one accelerated step, but `max_steps=1` returns -1 / None. Seed 1 with zero budget also returns failure although its total stopping time is zero. Fix endpoint checking and add boundary tests in both modules. This can misclassify finite-budget empirical probes; the full paper reproduction nevertheless passed.

2. **Residue classes are not normalized.** `density.py:132-143` starts at the supplied residue rather than its canonical representative modulo the modulus. For residues -1, 2 and 5 modulo 3, up to 10, all three should return 189/671. Actual results are 140/671, 189/671 and 819/7381. Normalize residue modulo the positive modulus, with zero represented by the first positive multiple. Add invariance tests under `r -> r + k*m`.

3. **Set density counts duplicates.** `density.py:115-129` describes the density of a set but iterates its input sequence directly. `[1,1]` with n=1 returns 2 rather than 1. Either deduplicate or explicitly reject duplicate inputs and document the restriction. Add the invariant that a set's partial density is in [0,1].

4. **Trajectory's repeat contract differs from implementation.** `core.py:48-63` promises termination at a locally repeated value, but checks only return to the starting seed. In the sibling system d=-1, seed 20 enters the cycle 10 -> 5 -> 7 -> 10. The function continues to its cap instead of stopping on that first repeat. Either track seen values or narrow the docstring; add a transient-into-cycle regression test.

These findings do not invalidate the main no-go theorems. They identify robustness gaps in laboratory utilities and explicitly empirical probes.

## Priority 2: test the certificate and failure paths, not just headline values

At a per-file 90% line threshold Lacuna identifies four files:

| File | Line coverage | Suggested tests |
|---|---:|---|
| `collatz/stopping.py` | 88.64% | `block_gamma_certificate` is entirely unexecuted (664-677); test exact threshold equality, strict failure, and rejected domains. Exercise coefficient-rule cap exhaustion (819,827,850-851) and verify it is never called a counterexample. |
| `collatz/density.py` | 84.15% | Residue normalization, duplicate invariance, zero/negative domains, and the unexecuted `bad_set_table`. |
| `collatz/core.py` | 84.38% | Budget endpoints, zero seed valuation errors, invalid Syracuse inputs, bounded samples from `orbit`, transient cycle entry. |
| `collatz/__main__.py` | 66.67% | Lightweight subprocess tests for density, transfer and stopping CLI routes; check that exact/empirical labels and exit codes survive end-to-end. |

Do not chase a coverage percentage by itself. Independent exact oracles and semantic invariants matter more. The current 104 tests all pass despite the concrete discrepancies above.

## Priority 3: sharpen the research program

The following are proposed investigations, not new theorems:

- Treat finite residue/Markov contraction as a limitation result unless a quantitative bridge to deterministic positive-integer orbits is supplied. The existing README already warns about this gap. A useful next experiment should measure the missing joint dependence on parity, valuation and real size rather than simply compute larger finite transfer matrices.
- Focus on the residual coefficient stopping rule and bounded cumulative expansion. Larger finite sweeps cannot prove global boundedness. Record seed, stopping budget, exact block endpoint, and whether the rule was unresolved; distinguish failure to finish from genuine expansion.
- Build a claim-to-evidence manifest mapping each theorem/computational table to its assumptions, exact check, independent oracle and formalization status. The reproduction script is strong evidence of consistency but reuses the same implementation and is not an independent proof checker.
- Extend Lean only where it adds new coverage: the real/logarithmic statement, block robustness, or stopping-time theorem. The successful default build checks the arithmetic core, not the entire manuscript. Keep that distinction explicit.

## Installation/security notes

Lacuna was built locally with `npm ci`, `npm run build`, and linked as `lacuna`. The pinned installation reports 9 dependency advisories (6 moderate, 3 high), with 5 in production dependencies (2 moderate, 3 high). An attempted non-force `npm audit fix` unexpectedly expanded the dependency tree and worsened the audit; its lockfile changes were reverted and the exact original lockfile was reinstalled and rebuilt. No breaking dependency upgrades were retained. Use this installation for trusted local analysis; it is not security-cleared for untrusted repositories.

Lean runs within the project's `lean/` directory using `$HOME/.elan/bin/lake build`. No global default Lean toolchain or shell profile change was made. LaTeX/PDF compilation tools were not needed for executing this research and were not installed.

## Evidence artifacts

- `test-audit.log`: full suite and branch-aware coverage summary.
- `reproduction-audit.log`: full, non-quick manuscript numerical reproduction.
- `lean-audit.log`: default formal companion build.
- `coverage/coverage.json`, `coverage/lcov.info`: machine-readable Python coverage.
- `lacuna-analysis.json`: invalid upstream CLI result, retained for diagnosis.
- `lacuna-python-analysis.json`: valid Lacuna library analysis.
- `lacuna-python-audit.mjs`: rerunnable bridge using Lacuna's real library.
- `research-edge-audit.py`, `research-edge-audit.json`: exact issue reproducers.

## Sources

[1] https://github.com/Octagon-simon/lacuna/tree/88a8d18
[2] https://github.com/tuliomarchetto/collatz/tree/0fbb610e524101d1ad9ab413b61b223e57636e5c

# Lean 4 formalization of the modular obstruction

Machine-checked packaging of **Theorem `thm:main`** from `paper/main.tex`
(also the two-page note `note/lyapunov-obstruction-en.tex`):

> For every level \(j \ge 1\), no function
> \(V(n) = \log_2 n + w(n \bmod 2^j)\) is strictly decreasing at every
> positive odd integer under the accelerated Collatz map.

This is Tier-3 goal **G10** of `todo/todo.md`. The formalization converts
the paper's carefully written packaging into a *formally verified*
arithmetic certificate.

## Status

| Milestone | Status |
|-----------|--------|
| M0. Project scaffold | **done** |
| M1. Arithmetic core of `thm:main` builds with pure Lean 4 (no mathlib) | **done** (`lake build` green) |
| M2. Real/`logb` form (`Modular.lean`) with mathlib | optional; source present, disabled by default |
| M3. `cor:robust` non-strict / blocks of \(k\) | open |
| M4. `thm:stopping` variable-depth | open (large) |
| M5. CI gate + paper one-line mention | after M1 is tagged |

## Build (verified)

Requires Lean 4.24.0 (via [elan](https://github.com/leanprover/elan)).

```bash
# install elan once, then:
cd lean
lake build          # pure-stdlib arithmetic core — no network needed
```

The default `lakefile.toml` does **not** pull mathlib. The arithmetic
theorems below are the full content of the paper's proof of `thm:main`
(the contradiction is essentially \(3 < 2\)).

Optional Real form:

1. Uncomment the mathlib `[[require]]` block in `lakefile.toml`.
2. Add `import CollatzObstruction.Modular` to `CollatzObstruction.lean`.
3. `lake update && lake exe cache get && lake build`.

## What is proved (`lake build`)

In namespace `CollatzObstruction`:

| Theorem | Content |
|---------|---------|
| `accelT_family` | \(T(2^{j+1}m-1) = 3\cdot 2^j m - 1\) |
| `family_residue` | \(n \equiv T(n) \equiv -1 \pmod{2^j}\) |
| `family_expands` | \(n < T(n)\) on the family |
| `modular_obstruction_arith` | packages the four arithmetic facts |
| `modular_obstruction_integer_form` | residues cancel + size grows, all \(j,m\) |
| `family_unbounded` | family escapes every finite bound (`cor:robust`(1) arithmetic) |

## Layout

```
lean/
  lakefile.toml
  lean-toolchain          # leanprover/lean4:v4.24.0
  CollatzObstruction.lean
  CollatzObstruction/
    Basic.lean            # accelT, family, closed form, residues, expansion
    Arith.lean            # modular_obstruction_arith / integer_form
    Modular.lean          # optional Real/logb form (needs mathlib)
  README.md
```

## Relation to the paper

- The manuscript remains the human-readable source of record.
- This directory is an optional machine-checked companion.
- Do **not** claim Lean verification in the abstract until CI runs
  `lake build` green on every PR; a Discussion one-liner is fine once tagged.

## Roadmap honesty

M3–M4 (`thm:stopping`, `thm:exactboundary`) need prefix codes, Terras
bijection, and bounded oscillation — a multi-week project of its own.
M0–M1 already deliver the credibility win advertised for G10: the
fixed-depth modular no-go is machine-checked arithmetic.

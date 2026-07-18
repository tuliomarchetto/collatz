/-
Copyright (c) 2026 Tulio Marchetto. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Tulio Marchetto

Machine-checked packaging of the modular Lyapunov obstruction
(paper/main.tex, Theorem thm:main / note/lyapunov-obstruction-en.tex).

The pure-arithmetic core needs no mathlib and is the default build target.
The optional Real/log form lives in CollatzObstruction/Modular.lean and
requires mathlib (see lakefile.toml and README.md).
-/
import CollatzObstruction.Basic
import CollatzObstruction.Arith

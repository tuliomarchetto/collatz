/-
Copyright (c) 2026 Tulio Marchetto. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Tulio Marchetto

Real/log form of Theorem thm:main. **Requires mathlib.**

Enable by uncommenting the mathlib `require` in `lakefile.toml` and adding
`import CollatzObstruction.Modular` to `CollatzObstruction.lean`, then:

    lake update && lake exe cache get && lake build
-/
import Mathlib.Analysis.SpecialFunctions.Log.Base
import Mathlib.Data.Real.Basic
import CollatzObstruction.Arith

namespace CollatzObstruction

open Real

/-- A modular Lyapunov function of level `j` (paper, Definition def:lyap). -/
def IsModularLyapunov (j : Nat) (w : Nat → ℝ) : Prop :=
  ∀ n : Nat, 0 < n → n % 2 = 1 →
    logb 2 (accelT n) + w (accelT n % 2 ^ j) <
      logb 2 n + w (n % 2 ^ j)

lemma family_w_cancel (j m : Nat) (hm : 1 ≤ m) (w : Nat → ℝ) :
    w (accelT (family j m) % 2 ^ j) = w (family j m % 2 ^ j) := by
  have hr := family_residue j m hm
  rw [hr.1, hr.2]

/-- **Theorem thm:main (modular obstruction), Real form.** -/
theorem modular_obstruction (j : Nat) (w : Nat → ℝ) :
    ¬ IsModularLyapunov j w := by
  intro hV
  set n := family j 1
  set t := accelT n
  have hcore := modular_obstruction_arith j 1 (by decide)
  have hnpos : 0 < n := by simpa [n] using hcore.1
  have hnodd : n % 2 = 1 := by simpa [n] using hcore.2.1
  have hlt : n < t := by simpa [n, t] using hcore.2.2.2.2.2
  have hdec := hV n hnpos hnodd
  have hw : w (t % 2 ^ j) = w (n % 2 ^ j) := by
    simpa [n, t] using family_w_cancel j 1 (by decide) w
  rw [show accelT n = t from rfl, hw] at hdec
  have hlog : logb 2 (t : ℝ) < logb 2 (n : ℝ) := by linarith
  have hlog' : logb 2 (n : ℝ) < logb 2 (t : ℝ) := by
    refine (logb_lt_logb_iff (by norm_num : (1 : ℝ) < 2)
      (by exact_mod_cast hnpos)).mpr ?_
    exact_mod_cast hlt
  exact lt_irrefl _ (hlog.trans hlog')

end CollatzObstruction

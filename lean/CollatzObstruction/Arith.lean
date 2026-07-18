/-
Copyright (c) 2026 Tulio Marchetto. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Tulio Marchetto

Pure-arithmetic content of Theorem thm:main (paper/main.tex).
No mathlib dependency.
-/
import CollatzObstruction.Basic

namespace CollatzObstruction

/-- Arithmetic core of the modular obstruction (thm:main).

For every level `j` and every index `m ≥ 1`, the seed
`n = family j m = 2^{j+1} m − 1` is a positive odd integer whose
accelerated image has the same residue mod `2ʲ` and is strictly larger.
Consequently any correction depending only on the residue mod `2ʲ`
cancels along `n → T(n)`, while the size grows — so no modular
Lyapunov function of level `j` can strictly decrease at every positive
odd integer.
-/
theorem modular_obstruction_arith (j m : Nat) (hm : 1 ≤ m) :
    let n := family j m
    let t := accelT n
    0 < n ∧ n % 2 = 1 ∧
    t = 3 * 2 ^ j * m - 1 ∧
    n % 2 ^ j = 2 ^ j - 1 ∧
    t % 2 ^ j = 2 ^ j - 1 ∧
    n < t := by
  intro n t
  refine ⟨family_pos j m hm, family_odd j m hm, ?_, ?_, ?_, ?_⟩
  · simp [n, t, accelT_family j m hm]
  · exact (family_residue j m hm).1
  · simpa [n, t] using (family_residue j m hm).2
  · simpa [n, t] using family_expands j m hm

/-- Special case: pure Mersenne seed `n = 2^{j+1} − 1`. -/
theorem modular_obstruction_mersenne (j : Nat) :
    let n := family j 1
    let t := accelT n
    0 < n ∧ n % 2 = 1 ∧
    n % 2 ^ j = 2 ^ j - 1 ∧
    t % 2 ^ j = 2 ^ j - 1 ∧
    n < t := by
  have h := modular_obstruction_arith j 1 (by decide)
  exact ⟨h.1, h.2.1, h.2.2.2.1, h.2.2.2.2.1, h.2.2.2.2.2⟩

/-- The witness family is unbounded (escapes every finite bound). -/
theorem family_unbounded (j B : Nat) :
    ∃ m : Nat, 1 ≤ m ∧ B < family j m := by
  refine ⟨B + 1, by omega, ?_⟩
  have h := family_add_one j (B + 1) (by omega)
  have h2 : 2 ≤ 2 ^ (j + 1) := two_le_two_pow_succ j
  have : 2 * (B + 1) ≤ 2 ^ (j + 1) * (B + 1) :=
    Nat.mul_le_mul_right (B + 1) h2
  omega

theorem family_escapes_bound (j B : Nat) :
    ∃ m : Nat, 1 ≤ m ∧ B < family j m :=
  family_unbounded j B

/-- **Integer form of thm:main.**

For every `j` and every `m ≥ 1`, writing `n = family j m` and
`t = accelT n`, one has `n % 2^j = t % 2^j` and `n < t`.
Any modular correction therefore cancels while the size grows.
-/
theorem modular_obstruction_integer_form (j : Nat) :
    ∀ m : Nat, 1 ≤ m →
      family j m % 2 ^ j = accelT (family j m) % 2 ^ j ∧
      family j m < accelT (family j m) := by
  intro m hm
  constructor
  · have hr := family_residue j m hm
    exact hr.1.trans hr.2.symm
  · exact family_expands j m hm

end CollatzObstruction

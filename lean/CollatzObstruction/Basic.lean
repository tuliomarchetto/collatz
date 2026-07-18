/-
Copyright (c) 2026 Tulio Marchetto. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Tulio Marchetto

Accelerated Collatz map and the Mersenne-type family used by thm:main.
Pure Lean 4 standard library — no mathlib dependency.
-/

namespace CollatzObstruction

/-- Accelerated Collatz map on natural numbers. -/
def accelT (n : Nat) : Nat :=
  if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

theorem accelT_odd {n : Nat} (h : n % 2 = 1) : accelT n = (3 * n + 1) / 2 := by
  simp [accelT, h]

/-- Test family of Theorem thm:main: `nₘ = 2^{j+1} m − 1`. -/
def family (j m : Nat) : Nat := 2 ^ (j + 1) * m - 1

theorem one_le_two_pow (k : Nat) : 1 ≤ 2 ^ k := by
  induction k with
  | zero => decide
  | succ k ih =>
    calc 1 ≤ 2 ^ k := ih
      _ ≤ 2 * 2 ^ k := Nat.le_mul_of_pos_left (2 ^ k) (by decide)
      _ = 2 ^ (k + 1) := by rw [Nat.pow_succ, Nat.mul_comm]

theorem two_pow_pos (k : Nat) : 0 < 2 ^ k :=
  Nat.lt_of_lt_of_le (by decide : 0 < 1) (one_le_two_pow k)

theorem two_pow_succ (j : Nat) : 2 ^ (j + 1) = 2 * 2 ^ j := by
  rw [Nat.pow_succ, Nat.mul_comm]

theorem two_le_two_pow_succ (j : Nat) : 2 ≤ 2 ^ (j + 1) := by
  calc 2 = 2 ^ 1 := rfl
    _ ≤ 2 ^ (j + 1) := Nat.pow_le_pow_right (by decide) (Nat.le_add_left 1 j)

theorem mul_two_pow_comm (j m : Nat) :
    2 * 2 ^ j * m = 2 ^ j * (2 * m) := by
  calc 2 * 2 ^ j * m = 2 * (2 ^ j * m) := by rw [Nat.mul_assoc]
    _ = (2 ^ j * m) * 2 := Nat.mul_comm _ _
    _ = 2 ^ j * (m * 2) := by rw [Nat.mul_assoc]
    _ = 2 ^ j * (2 * m) := by rw [Nat.mul_comm m 2]

theorem mul_three_pow_comm (j m : Nat) :
    3 * 2 ^ j * m = 2 ^ j * (3 * m) := by
  calc 3 * 2 ^ j * m = 3 * (2 ^ j * m) := by rw [Nat.mul_assoc]
    _ = (2 ^ j * m) * 3 := Nat.mul_comm _ _
    _ = 2 ^ j * (m * 3) := by rw [Nat.mul_assoc]
    _ = 2 ^ j * (3 * m) := by rw [Nat.mul_comm m 3]

theorem one_le_three_mul_two_pow (j m : Nat) (hm : 1 ≤ m) :
    1 ≤ 3 * 2 ^ j * m := by
  have h2 : 1 ≤ 2 ^ j := one_le_two_pow j
  have h3 : 1 ≤ 3 * 2 ^ j := by
    calc 1 ≤ 3 := by decide
      _ = 3 * 1 := by decide
      _ ≤ 3 * 2 ^ j := Nat.mul_le_mul_left 3 h2
  exact Nat.le_trans h3 (Nat.le_mul_of_pos_right _ hm)

theorem family_add_one (j m : Nat) (hm : 1 ≤ m) :
    family j m + 1 = 2 ^ (j + 1) * m := by
  have hge : 1 ≤ 2 ^ (j + 1) * m :=
    Nat.le_trans (one_le_two_pow (j + 1)) (Nat.le_mul_of_pos_right _ hm)
  exact Nat.sub_add_cancel hge

theorem family_pos (j m : Nat) (hm : 1 ≤ m) : 0 < family j m := by
  have h := family_add_one j m hm
  have h2 : 2 ≤ 2 ^ (j + 1) * m :=
    Nat.le_trans (two_le_two_pow_succ j) (Nat.le_mul_of_pos_right _ hm)
  have : 1 ≤ family j m := by
    have : 2 ≤ family j m + 1 := by rw [h]; exact h2
    exact Nat.le_of_succ_le_succ this
  exact this

theorem family_odd (j m : Nat) (hm : 1 ≤ m) : family j m % 2 = 1 := by
  have h := family_add_one j m hm
  have heven : (family j m + 1) % 2 = 0 := by
    rw [h, two_pow_succ, Nat.mul_assoc, Nat.mul_mod_right]
  omega

/-- 3 * family + 1 = 2 * (3 * 2^j * m - 1). -/
theorem three_family_plus_one (j m : Nat) (hm : 1 ≤ m) :
    3 * family j m + 1 = 2 * (3 * 2 ^ j * m - 1) := by
  have hge1 : 1 ≤ 2 ^ (j + 1) * m :=
    Nat.le_trans (one_le_two_pow (j + 1)) (Nat.le_mul_of_pos_right _ hm)
  have hge2 : 1 ≤ 3 * 2 ^ j * m := one_le_three_mul_two_pow j m hm
  -- Unfold family to 2^{j+1}*m - 1
  simp only [family]
  -- Rewrite 2^{j+1} = 2*2^j
  have h2 := two_pow_succ j
  rw [h2]
  -- Goal: 3 * (2*2^j*m - 1) + 1 = 2 * (3*2^j*m - 1)
  have ha : 1 ≤ 2 * 2 ^ j * m := by
    rw [← h2]; exact hge1
  -- 3 * (2*2^j*m - 1) = 3*(2*2^j*m) - 3
  have hL1 : 3 * (2 * 2 ^ j * m - 1) = 3 * (2 * 2 ^ j * m) - 3 := by
    rw [Nat.mul_sub_left_distrib, Nat.mul_one]
  have h3le : 3 ≤ 3 * (2 * 2 ^ j * m) := by
    calc 3 = 3 * 1 := by decide
      _ ≤ 3 * (2 * 2 ^ j * m) := Nat.mul_le_mul_left 3 ha
  -- LHS = 3*(2*2^j*m) - 3 + 1 = 3*(2*2^j*m) - 2
  have hL : 3 * (2 * 2 ^ j * m - 1) + 1 = 3 * (2 * 2 ^ j * m) - 2 := by
    rw [hL1]
    have : 3 * (2 * 2 ^ j * m) - 3 + 1 = 3 * (2 * 2 ^ j * m) - 2 := by
      omega
    exact this
  -- RHS = 2*(3*2^j*m) - 2
  have hR : 2 * (3 * 2 ^ j * m - 1) = 2 * (3 * 2 ^ j * m) - 2 := by
    rw [Nat.mul_sub_left_distrib, Nat.mul_one]
  -- 3 * (2 * 2^j * m) = 2 * (3 * 2^j * m)
  have hEq : 3 * (2 * 2 ^ j * m) = 2 * (3 * 2 ^ j * m) := by
    -- 3 * 2 * 2^j * m = 2 * 3 * 2^j * m
    calc 3 * (2 * 2 ^ j * m) = 3 * 2 * (2 ^ j * m) := by
          simp only [Nat.mul_assoc]
      _ = 2 * 3 * (2 ^ j * m) := by rw [Nat.mul_comm 3 2]
      _ = 2 * (3 * (2 ^ j * m)) := by simp only [Nat.mul_assoc]
      _ = 2 * (3 * 2 ^ j * m) := by simp only [Nat.mul_assoc]
  -- Finish
  rw [hL, hR, hEq]

theorem accelT_family (j m : Nat) (hm : 1 ≤ m) :
    accelT (family j m) = 3 * 2 ^ j * m - 1 := by
  rw [accelT_odd (family_odd j m hm), three_family_plus_one j m hm]
  exact Nat.mul_div_right _ (by decide : 0 < 2)

/-- `(B * Q - 1) % B = B - 1` when `B ≥ 1`, `Q ≥ 1`. -/
theorem mul_sub_one_mod (B Q : Nat) (hB : 1 ≤ B) (hQ : 1 ≤ Q) :
    (B * Q - 1) % B = B - 1 := by
  have hge : 1 ≤ B * Q :=
    Nat.le_trans hB (Nat.le_mul_of_pos_right B hQ)
  have hsplit : B * Q = B * (Q - 1) + B := by
    have hq : Q = Q - 1 + 1 := (Nat.sub_add_cancel hQ).symm
    calc B * Q = B * (Q - 1 + 1) := by rw [← hq]
      _ = B * (Q - 1) + B * 1 := Nat.mul_add _ _ _
      _ = B * (Q - 1) + B := by rw [Nat.mul_one]
  have hform : B * Q - 1 = B * (Q - 1) + (B - 1) := by
    have : B * Q - 1 = B * (Q - 1) + B - 1 := by rw [hsplit]
    rw [this, Nat.add_sub_assoc hB]
  rw [hform]
  have hmod0 : (B * (Q - 1)) % B = 0 := Nat.mul_mod_right B (Q - 1)
  rw [Nat.add_mod, hmod0, Nat.zero_add, Nat.mod_mod, Nat.mod_eq_of_lt]
  exact Nat.sub_lt (Nat.lt_of_lt_of_le (by decide : 0 < 1) hB) (by decide : 0 < 1)

theorem family_as_mul (j m : Nat) (hm : 1 ≤ m) :
    family j m = 2 ^ j * (2 * m) - 1 := by
  have h := family_add_one j m hm
  have heq : 2 ^ (j + 1) * m = 2 ^ j * (2 * m) := by
    rw [two_pow_succ, mul_two_pow_comm]
  have : family j m + 1 = 2 ^ j * (2 * m) := by rw [h, heq]
  exact Nat.eq_sub_of_add_eq this

theorem accelT_family_as_mul (j m : Nat) (hm : 1 ≤ m) :
    accelT (family j m) = 2 ^ j * (3 * m) - 1 := by
  rw [accelT_family j m hm, mul_three_pow_comm]

theorem family_residue (j m : Nat) (hm : 1 ≤ m) :
    family j m % 2 ^ j = 2 ^ j - 1 ∧
    accelT (family j m) % 2 ^ j = 2 ^ j - 1 := by
  constructor
  · rw [family_as_mul j m hm]
    exact mul_sub_one_mod (2 ^ j) (2 * m) (one_le_two_pow j) (by omega)
  · rw [accelT_family_as_mul j m hm]
    exact mul_sub_one_mod (2 ^ j) (3 * m) (one_le_two_pow j) (by omega)

theorem family_expands (j m : Nat) (hm : 1 ≤ m) :
    family j m < accelT (family j m) := by
  rw [accelT_family j m hm]
  have hL := family_add_one j m hm
  have hR : 1 ≤ 3 * 2 ^ j * m := one_le_three_mul_two_pow j m hm
  have hx : 0 < 2 ^ j * m := Nat.mul_pos (two_pow_pos j) (by omega)
  have hcmp : 2 ^ (j + 1) * m < 3 * 2 ^ j * m := by
    rw [two_pow_succ]
    have step : 2 * (2 ^ j * m) < 3 * (2 ^ j * m) :=
      Nat.mul_lt_mul_of_pos_right (by decide : 2 < 3) hx
    calc 2 * 2 ^ j * m = 2 * (2 ^ j * m) := by rw [Nat.mul_assoc]
      _ < 3 * (2 ^ j * m) := step
      _ = 3 * 2 ^ j * m := by rw [Nat.mul_assoc]
  have : family j m + 1 < (3 * 2 ^ j * m - 1) + 1 := by
    rw [hL, Nat.sub_add_cancel hR]
    exact hcmp
  exact Nat.lt_of_succ_lt_succ this

end CollatzObstruction

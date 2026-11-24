/-
Gaps and Totals — the finite algebraic core.

Paper: *Gaps and Totals: an operator-first theory of transport invariants* (in preparation).
This file proves the redistribution theorems of §3 in the corrected form:

* `redistribution_traceless`: the redistribution operator `F(Ω,Π) = ΠΩQ + QΩΠ` is traceless.
* `redistribution_block12` / `redistribution_block21`: the off-diagonal blocks of `F` are the
  off-diagonal blocks of `Ω`, so `F = 0` forces each of them to vanish.
* `redistribution_zero_iff_commute`: `F(Ω,Π) = 0 ↔ ΩΠ = ΠΩ`. No self-adjointness is needed
  for the equivalence; it is a ring identity plus the idempotence of `Π`.
* `half_commutator_norm`: for self-adjoint `Ω`, `‖[Ω,Π]‖²_F = 2‖ΠΩQ‖²_F`, i.e.
  `½‖[Ω,Π]‖²_F = ‖ΠΩQ‖²_F` — the quantum metric is half the squared commutator norm.

What is *not* here is in `LIMITATIONS.md`: the analytic statements (Kato's projector bound,
Puiseux exponents at an exceptional point, spectral flow) are not formalised, and the
shape-sphere spectrum is certified by the gate `scripts/gates/g01_shape_spectrum.py`, not by
the kernel.
-/
import Mathlib

namespace GapsAndTotals

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The complement of an idempotent is idempotent. -/
theorem idem_one_sub {P : Matrix n n ℝ} (hP : P * P = P) : (1 - P) * (1 - P) = 1 - P := by
  have h : (1 - P) * (1 - P) = 1 - P - P + P * P := by noncomm_ring
  rw [h, hP]
  abel


/-- The redistribution operator `F(Ω,Π) = ΠΩQ + QΩΠ`, `Q = 1 - Π`. -/
def redist (P X : Matrix n n ℝ) : Matrix n n ℝ := P * X * (1 - P) + (1 - P) * X * P

/-- `Π (1 - Π) = 0`. -/
theorem mul_one_sub (P : Matrix n n ℝ) (hP : P * P = P) : P * (1 - P) = 0 := by
  rw [mul_sub, mul_one, hP, sub_self]

/-- `(1 - Π) Π = 0`. -/
theorem one_sub_mul (P : Matrix n n ℝ) (hP : P * P = P) : (1 - P) * P = 0 := by
  rw [sub_mul, one_mul, hP, sub_self]

/-- `Π Ω Q` is traceless. -/
theorem trace_block12 (P X : Matrix n n ℝ) (hP : P * P = P) : trace (P * X * (1 - P)) = 0 := by
  rw [trace_mul_comm (P * X) (1 - P)]
  have h0 : (1 - P) * (P * X) = 0 := by
    rw [← mul_assoc, one_sub_mul P hP, zero_mul]
  rw [h0, trace_zero]

/-- `Q Ω Π` is traceless. -/
theorem trace_block21 (P X : Matrix n n ℝ) (hP : P * P = P) : trace ((1 - P) * X * P) = 0 := by
  rw [trace_mul_comm ((1 - P) * X) P]
  have h0 : P * ((1 - P) * X) = 0 := by
    rw [← mul_assoc, mul_one_sub P hP, zero_mul]
  rw [h0, trace_zero]

/-- **Theorem 1.** The redistribution operator is traceless. -/
theorem redistribution_traceless (P X : Matrix n n ℝ) (hP : P * P = P) :
    trace (redist P X) = 0 := by
  rw [redist, trace_add, trace_block12 P X hP, trace_block21 P X hP, add_zero]

/-- The `(1,2)` block of `F` is the `(1,2)` block of `Ω`. -/
theorem redistribution_block12 (P X : Matrix n n ℝ) (hP : P * P = P) :
    P * redist P X * (1 - P) = P * X * (1 - P) := by
  have hQ : (1 - P) * (1 - P) = 1 - P := idem_one_sub hP
  have hPQ : P * (1 - P) = 0 := mul_one_sub P hP
  have e1 : P * (P * X * (1 - P)) * (1 - P) = P * X * (1 - P) := by
    calc P * (P * X * (1 - P)) * (1 - P)
        = P * P * (X * ((1 - P) * (1 - P))) := by noncomm_ring
      _ = P * P * (X * (1 - P)) := by rw [hQ]
      _ = P * (X * (1 - P)) := by rw [hP]
      _ = P * X * (1 - P) := by noncomm_ring
  have e2 : P * ((1 - P) * X * P) * (1 - P) = 0 := by
    calc P * ((1 - P) * X * P) * (1 - P)
        = (P * (1 - P)) * X * (P * (1 - P)) := by noncomm_ring
      _ = 0 := by rw [hPQ]; simp
  rw [redist, mul_add, add_mul, e1, e2, add_zero]

/-- The `(2,1)` block of `F` is the `(2,1)` block of `Ω`. -/
theorem redistribution_block21 (P X : Matrix n n ℝ) (hP : P * P = P) :
    (1 - P) * redist P X * P = (1 - P) * X * P := by
  have hQ : (1 - P) * (1 - P) = 1 - P := idem_one_sub hP
  have hQP : (1 - P) * P = 0 := one_sub_mul P hP
  have e1 : (1 - P) * (P * X * (1 - P)) * P = 0 := by
    calc (1 - P) * (P * X * (1 - P)) * P
        = ((1 - P) * P) * X * ((1 - P) * P) := by noncomm_ring
      _ = 0 := by rw [hQP]; simp
  have e2 : (1 - P) * ((1 - P) * X * P) * P = (1 - P) * X * P := by
    calc (1 - P) * ((1 - P) * X * P) * P
        = (1 - P) * (1 - P) * (X * (P * P)) := by noncomm_ring
      _ = (1 - P) * (X * (P * P)) := by rw [hQ]
      _ = (1 - P) * (X * P) := by rw [hP]
      _ = (1 - P) * X * P := by noncomm_ring
  rw [redist, mul_add, add_mul, e1, e2, zero_add]

/-- The block decomposition `Ω = ΠΩΠ + ΠΩQ + QΩΠ + QΩQ`. -/
theorem block_decomposition (P X : Matrix n n ℝ) :
    P * X * P + P * X * (1 - P) + (1 - P) * X * P + (1 - P) * X * (1 - P) = X := by
  have h : P * X * P + P * X * (1 - P) + (1 - P) * X * P + (1 - P) * X * (1 - P)
      = (P + (1 - P)) * X * (P + (1 - P)) := by noncomm_ring
  rw [h, add_sub_cancel]
  simp

/-- **Theorem 2.** `F(Ω,Π) = 0` iff `Ω` commutes with `Π`. -/
theorem redistribution_zero_iff_commute (P X : Matrix n n ℝ) (hP : P * P = P) :
    redist P X = 0 ↔ X * P = P * X := by
  have hQ0 : (1 - P) * P = 0 := one_sub_mul P hP
  constructor
  · intro h
    have h12 : P * X * (1 - P) = 0 := by
      have := redistribution_block12 P X hP
      rw [h] at this
      simpa using this.symm
    have h21 : (1 - P) * X * P = 0 := by
      have := redistribution_block21 P X hP
      rw [h] at this
      simpa using this.symm
    have hX : X = P * X * P + (1 - P) * X * (1 - P) := by
      have hd := block_decomposition P X
      rw [h12, h21] at hd
      simp at hd
      exact hd.symm
    have hz : (1 - P) * X * (1 - P) * P = 0 := by
      calc (1 - P) * X * (1 - P) * P = (1 - P) * X * ((1 - P) * P) := by noncomm_ring
        _ = 0 := by rw [hQ0, mul_zero]
    have hz' : P * ((1 - P) * X * (1 - P)) = 0 := by
      calc P * ((1 - P) * X * (1 - P)) = (P * (1 - P)) * X * (1 - P) := by noncomm_ring
        _ = 0 := by rw [mul_one_sub P hP]; simp
    have hPP : P * X * P * P = P * X * P := by rw [mul_assoc, hP]
    have hXP : X * P = P * X * P := by
      calc X * P = (P * X * P + (1 - P) * X * (1 - P)) * P := by conv_lhs => rw [hX]
        _ = P * X * P * P + (1 - P) * X * (1 - P) * P := by rw [add_mul]
        _ = P * X * P * P := by rw [hz, add_zero]
        _ = P * X * P := hPP
    have hPX : P * X = P * X * P := by
      calc P * X = P * (P * X * P + (1 - P) * X * (1 - P)) := by conv_lhs => rw [hX]
        _ = P * (P * X * P) + P * ((1 - P) * X * (1 - P)) := by rw [mul_add]
        _ = P * (P * X * P) := by rw [hz', add_zero]
        _ = P * P * X * P := by noncomm_ring
        _ = P * X * P := by rw [hP]
    rw [hXP, hPX, hPP]
  · intro h
    have h12 : P * X * (1 - P) = 0 := by
      rw [← h, mul_assoc, mul_one_sub P hP, mul_zero]
    have h21 : (1 - P) * X * P = 0 := by
      rw [mul_assoc, h, ← mul_assoc, hQ0, zero_mul]
    rw [redist, h12, h21, add_zero]


/-! ## Theorem 3: the norm identities

For self-adjoint `Ω` and an orthogonal projector `Π`, the redistribution operator satisfies
`‖F‖²_F = 2‖ΠΩQ‖²_F = ½‖[Ω,Π]‖²_F`.  The proof is that `A = ΠΩQ` is square-zero, its
transpose is `QΩΠ`, and the commutator is their difference. -/

/-- Frobenius norm squared. -/
def frob (X : Matrix n n ℝ) : ℝ := trace (X * Xᵀ)

/-- `(Π Ω Q)² = 0`. -/
theorem block12_sq (P X : Matrix n n ℝ) (hP : P * P = P) :
    (P * X * (1 - P)) * (P * X * (1 - P)) = 0 := by
  have hQP : (1 - P) * P = 0 := one_sub_mul P hP
  calc (P * X * (1 - P)) * (P * X * (1 - P))
      = P * X * ((1 - P) * P) * X * (1 - P) := by noncomm_ring
    _ = 0 := by rw [hQP]; simp

/-- `(Q Ω Π)² = 0`. -/
theorem block21_sq (P X : Matrix n n ℝ) (hP : P * P = P) :
    ((1 - P) * X * P) * ((1 - P) * X * P) = 0 := by
  have hPQ : P * (1 - P) = 0 := mul_one_sub P hP
  calc ((1 - P) * X * P) * ((1 - P) * X * P)
      = (1 - P) * X * (P * (1 - P)) * X * P := by noncomm_ring
    _ = 0 := by rw [hPQ]; simp

/-- For self-adjoint `Ω` and orthogonal `Π`, the two off-diagonal blocks are transposes. -/
theorem block_transpose (P X : Matrix n n ℝ) (hPt : Pᵀ = P) (hXt : Xᵀ = X) :
    (1 - P) * X * P = (P * X * (1 - P))ᵀ := by
  have hQ : (1 - P)ᵀ = 1 - P := by rw [transpose_sub, transpose_one, hPt]
  rw [transpose_mul, transpose_mul, hQ]
  simp only [hPt, hXt]
  noncomm_ring

/-- An abstract form of Theorem 3a: `‖A + Aᵀ‖²_F = 2‖A‖²_F` for square-zero `A`. -/
theorem frob_add_transpose (A : Matrix n n ℝ) (hA : A * A = 0) :
    trace ((A + Aᵀ) * (A + Aᵀ)ᵀ) = 2 * trace (A * Aᵀ) := by
  have hsym : (A + Aᵀ)ᵀ = A + Aᵀ := by rw [transpose_add, transpose_transpose]; abel
  rw [hsym]
  have expand : (A + Aᵀ) * (A + Aᵀ) = A * A + A * Aᵀ + Aᵀ * A + Aᵀ * Aᵀ := by
    noncomm_ring
  rw [expand, trace_add, trace_add, trace_add]
  have h2 : Aᵀ * Aᵀ = (A * A)ᵀ := by rw [transpose_mul]
  have h3 : trace (Aᵀ * A) = trace (A * Aᵀ) := trace_mul_comm Aᵀ A
  rw [h2, hA, transpose_zero, trace_zero, h3]
  simp
  ring

/-- An abstract form of Theorem 3c: `‖Aᵀ − A‖²_F = 2‖A‖²_F` for square-zero `A`. -/
theorem frob_transpose_sub (A : Matrix n n ℝ) (hA : A * A = 0) :
    trace ((Aᵀ - A) * (Aᵀ - A)ᵀ) = 2 * trace (A * Aᵀ) := by
  have hsym : (Aᵀ - A)ᵀ = A - Aᵀ := by rw [transpose_sub, transpose_transpose]
  rw [hsym]
  have expand : (Aᵀ - A) * (A - Aᵀ) = Aᵀ * A - Aᵀ * Aᵀ - (A * A - A * Aᵀ) := by
    noncomm_ring
  rw [expand]
  have h2 : Aᵀ * Aᵀ = (A * A)ᵀ := by rw [transpose_mul]
  rw [h2, hA, transpose_zero]
  have h3 : trace (Aᵀ * A) = trace (A * Aᵀ) := trace_mul_comm Aᵀ A
  rw [trace_sub, trace_sub, h3]
  simp
  ring

/-- **Theorem 3a.** `‖F‖²_F = 2‖ΠΩQ‖²_F` for self-adjoint `Ω`. -/
theorem redistribution_norm (P X : Matrix n n ℝ) (hP : P * P = P) (hPt : Pᵀ = P)
    (hXt : Xᵀ = X) :
    frob (redist P X) = 2 * frob (P * X * (1 - P)) := by
  have hA := block12_sq P X hP
  have hBA : (1 - P) * X * P = (P * X * (1 - P))ᵀ := block_transpose P X hPt hXt
  have hF : redist P X = P * X * (1 - P) + (P * X * (1 - P))ᵀ := by
    rw [redist, hBA]
  rw [hF, frob, frob]
  exact frob_add_transpose _ hA

/-- **Theorem 3b.** The commutator `[Ω,Π]` is skew for self-adjoint `Ω` and orthogonal `Π`. -/
theorem commutator_skew (P X : Matrix n n ℝ) (hPt : Pᵀ = P) (hXt : Xᵀ = X) :
    (X * P - P * X)ᵀ = -(X * P - P * X) := by
  rw [transpose_sub, transpose_mul, transpose_mul, hPt, hXt]
  abel

/-- **Theorem 3c.** `½‖[Ω,Π]‖²_F = ‖ΠΩQ‖²_F` for self-adjoint `Ω`. -/
theorem half_commutator_norm (P X : Matrix n n ℝ) (hP : P * P = P) (hPt : Pᵀ = P)
    (hXt : Xᵀ = X) :
    frob (X * P - P * X) = 2 * frob (P * X * (1 - P)) := by
  have hA := block12_sq P X hP
  have hBA : (1 - P) * X * P = (P * X * (1 - P))ᵀ := block_transpose P X hPt hXt
  have hcomm : X * P - P * X = (P * X * (1 - P))ᵀ - P * X * (1 - P) := by
    rw [← hBA]; noncomm_ring
  rw [hcomm, frob, frob]
  exact frob_transpose_sub _ hA

end GapsAndTotals

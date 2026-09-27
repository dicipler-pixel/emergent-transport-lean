/-
Directional Transport Geometry of Admissible Channels — the emergent-transport-geometry paper
(Jeromie Beasley, DOI 10.5281/zenodo.21089303): the exact finite results, with the
projector–metric correspondence in its corrected (daggered) form.

* Proposition 2 (first-order cancellation): for symmetric `R` and skew `E`, `Tr(RE) = 0`, so the
  first variation of the regularised trace-log vanishes at the normal baseline.
* Lemma 6 / Corollary 4.2: for a projector `Π`, the commutator `[X, Π]` is off-diagonal:
  `Π[X,Π]Π = 0` and `(1−Π)[X,Π](1−Π) = 0`.
* Theorem 7, corrected: for the rank-one projector `Πₙ` onto the `n`-th basis vector,
  `Tr(Πₙ Eᵀ (1−Πₙ) E) = Σ_{m≠n} E_{mn}²`, the total off-diagonal transition weight. For skew `E`
  the undaggered form `Tr(Πₙ E (1−Πₙ) E)` is its negative, so the printed `½ Tr(ΠEQE)` has the
  wrong sign and factor; the daggered form is the one that equals the metric.
* Proposition 3 / Theorem 13 (gauge invariance): `Tr(UΠUᵀ · UVUᵀ · UWUᵀ) = Tr(ΠVW)` for
  orthogonal `U`.
* Theorem 14 (persistence): `Tr(Π₁Π₂) = ‖Π₂Π₁‖²_F ≥ 0` for orthogonal projectors, and for rank one
  `Tr(P_u P_v) = (u·v)² = cos²θ`.
-/
import Mathlib

namespace EmergentTransport

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ## Proposition 2: first-order cancellation -/

/-- **Proposition 2.** A symmetric matrix times a skew matrix is traceless: `Tr(RE) = 0`. Applied
to `R = R₀(z−η)²` (symmetric for self-adjoint `H₀`), the first variation of `Tr log(H + ηI)`
vanishes pointwise on the contour. -/
theorem trace_sym_skew (R E : Matrix n n ℝ) (hR : Rᵀ = R) (hE : Eᵀ = -E) : trace (R * E) = 0 := by
  have h : trace (R * E) = -trace (R * E) := by
    calc trace (R * E) = trace ((R * E)ᵀ) := (trace_transpose _).symm
      _ = trace (Eᵀ * Rᵀ) := by rw [transpose_mul]
      _ = trace (-E * R) := by rw [hE, hR]
      _ = -trace (R * E) := by rw [neg_mul, trace_neg, trace_mul_comm]
  linarith

/-! ## Lemma 6: commutators with a projector are off-diagonal -/

/-- **Lemma 6 / Corollary 4.2.** For a projector `Π`, the commutator `[X, Π]` has no diagonal
blocks: `Π[X,Π]Π = 0` and `(1−Π)[X,Π](1−Π) = 0`. -/
theorem commutator_offdiag {R : Type*} [Ring R] (P X : R) (hP : P * P = P) :
    P * (X * P - P * X) * P = 0 ∧ (1 - P) * (X * P - P * X) * (1 - P) = 0 := by
  constructor
  · have : P * (X * P - P * X) * P = P * X * (P * P) - (P * P) * X * P := by noncomm_ring
    rw [this, hP, sub_self]
  · have hPQ : P * (1 - P) = 0 := by rw [mul_sub, mul_one, hP, sub_self]
    have hQP : (1 - P) * P = 0 := by rw [sub_mul, one_mul, hP, sub_self]
    calc (1 - P) * (X * P - P * X) * (1 - P)
        = (1 - P) * X * (P * (1 - P)) - ((1 - P) * P) * X * (1 - P) := by noncomm_ring
      _ = 0 := by rw [hPQ, hQP]; noncomm_ring

/-! ## Theorem 7, corrected: the daggered projector–metric correspondence -/

/-- The rank-one projector onto the `k`-th basis vector. -/
def proj (k : n) : Matrix n n ℝ := of fun i j => if i = k ∧ j = k then 1 else 0

theorem trace_proj_mul (k : n) (X : Matrix n n ℝ) : trace (proj k * X) = X k k := by
  simp [trace, proj, mul_apply, ite_and, Finset.sum_ite_eq', Finset.sum_ite_eq]

theorem proj_mul_apply (k : n) (X : Matrix n n ℝ) (i j : n) :
    (Xᵀ * proj k * X) i j = X k i * X k j := by
  simp [mul_apply, proj, ite_and, Finset.sum_ite_eq', Finset.sum_ite_eq, transpose_apply]

/-- **Theorem 7, corrected.** `Tr(Πₙ Eᵀ (1−Πₙ) E) = Σ_{m≠n} E_{mn}²`: the daggered trace is the
total off-diagonal transition weight into channel `n`. -/
theorem metric_correspondence (k : n) (E : Matrix n n ℝ) :
    trace (proj k * Eᵀ * (1 - proj k) * E) = ∑ m ∈ Finset.univ.erase k, E m k ^ 2 := by
  rw [mul_assoc, mul_assoc, trace_proj_mul, ← mul_assoc, mul_sub, mul_one, sub_mul,
    Matrix.sub_apply, proj_mul_apply, mul_apply]
  simp only [transpose_apply]
  rw [← Finset.add_sum_erase _ _ (Finset.mem_univ k)]
  simp only [sq]
  ring

/-- **Theorem 7, the sign.** For skew `E`, the undaggered trace `Tr(Πₙ E (1−Πₙ) E)` is the
negative of the daggered one: the printed form reports `−Σ E_{mn}²`. -/
theorem undaggered_sign (k : n) (E : Matrix n n ℝ) (hE : Eᵀ = -E) :
    trace (proj k * E * (1 - proj k) * E) = -trace (proj k * Eᵀ * (1 - proj k) * E) := by
  rw [hE]
  simp only [mul_neg, neg_mul, trace_neg, neg_neg]

/-- **Theorem 7 as a commutator norm.** For an orthogonal projector `Π` and skew `E`, the
commutator `[E, Π]` is symmetric and `‖[E,Π]‖²_F = Tr([E,Π][E,Π]ᵀ) = 2 Tr(Π Eᵀ (1−Π) E)`. So the
correct form of the correspondence is `½‖[E,Π]‖²_F = Tr(ΠEᵀ(1−Π)E)`: the factor ½ belongs to the
squared commutator norm, the same `½‖[·,·]‖²` shape as the connection energy of the block
transport operator (`⅛‖[H,H†]‖² = ½‖[D,A]‖²`), with `Π` in the role of the obstruction field
and `E` in the role of the transport. -/
theorem half_commutator_norm (P E : Matrix n n ℝ) (hP : Pᵀ = P) (hPP : P * P = P)
    (hE : Eᵀ = -E) :
    trace ((E * P - P * E) * (E * P - P * E)ᵀ) = 2 * trace (P * Eᵀ * (1 - P) * E) := by
  have hC : (E * P - P * E)ᵀ = E * P - P * E := by
    rw [transpose_sub, transpose_mul, transpose_mul, hP, hE]
    noncomm_ring
  have hexp : (E * P - P * E) * (E * P - P * E) = E * P * E * P - E * P * E - P * E * E * P
      + P * E * P * E := by
    calc (E * P - P * E) * (E * P - P * E)
        = E * P * E * P - E * (P * P) * E - P * E * E * P + P * E * P * E := by noncomm_ring
      _ = _ := by rw [hPP]
  have hrhs : P * Eᵀ * (1 - P) * E = -(P * E * E) + P * E * P * E := by
    rw [hE]; noncomm_ring
  have h1 : trace (E * P * E * P) = trace (P * E * P * E) := by
    rw [trace_mul_comm (E * P * E) P]; simp only [mul_assoc]
  have h2 : trace (E * P * E) = trace (P * E * E) := by
    rw [mul_assoc E P E, trace_mul_comm E (P * E)]
  have h3 : trace (P * E * E * P) = trace (P * E * E) := by
    rw [trace_mul_comm (P * E * E) P]
    simp only [← mul_assoc, hPP]
  rw [hC, hexp, hrhs]
  simp only [trace_sub, trace_add, trace_neg]
  linarith [h1, h2, h3]

/-! ## Proposition 3: gauge invariance -/

/-- **Proposition 3 / Theorem 13.** For orthogonal `U`,
`Tr(UΠUᵀ · UVUᵀ · UWUᵀ) = Tr(ΠVW)`. -/
theorem gauge_invariance (U P V W : Matrix n n ℝ) (hU : Uᵀ * U = 1) :
    trace ((U * P * Uᵀ) * (U * V * Uᵀ) * (U * W * Uᵀ)) = trace (P * V * W) := by
  have e : (U * P * Uᵀ) * (U * V * Uᵀ) * (U * W * Uᵀ) = U * (P * V * W) * Uᵀ := by
    simp only [mul_assoc]
    rw [← mul_assoc Uᵀ U, hU, one_mul, ← mul_assoc Uᵀ U, hU, one_mul]
  rw [e, trace_mul_comm, ← mul_assoc, hU, one_mul]

/-! ## Theorem 14: persistence is a squared norm -/

/-- **Theorem 14.** For orthogonal projectors, `Tr(Π₁Π₂) = Tr((Π₂Π₁)ᵀ(Π₂Π₁)) = ‖Π₂Π₁‖²_F`. -/
theorem persistence_frobenius (P1 P2 : Matrix n n ℝ) (h1 : P1ᵀ = P1) (h2 : P2ᵀ = P2)
    (hP1 : P1 * P1 = P1) (hP2 : P2 * P2 = P2) :
    trace (P1 * P2) = trace ((P2 * P1)ᵀ * (P2 * P1)) := by
  rw [transpose_mul, h1, h2]
  have : P1 * P2 * (P2 * P1) = P1 * (P2 * P2) * P1 := by noncomm_ring
  rw [this, hP2, trace_mul_comm (P1 * P2) P1, ← mul_assoc, hP1]

/-- **Theorem 14, positivity.** The persistence overlap `C = Tr(Π₁Π₂)` is nonnegative. -/
theorem persistence_nonneg (P1 P2 : Matrix n n ℝ) (h1 : P1ᵀ = P1) (h2 : P2ᵀ = P2)
    (hP1 : P1 * P1 = P1) (hP2 : P2 * P2 = P2) : 0 ≤ trace (P1 * P2) := by
  rw [persistence_frobenius P1 P2 h1 h2 hP1 hP2]
  simp only [trace, diag, mul_apply, transpose_apply]
  exact Finset.sum_nonneg fun i _ => Finset.sum_nonneg fun j _ => mul_self_nonneg _

/-- **Theorem 14, rank one.** For unit vectors, `Tr(P_u P_v) = (u·v)² = cos²θ`. -/
theorem persistence_rank_one (u v : n → ℝ) :
    trace (vecMulVec u u * vecMulVec v v) = (u ⬝ᵥ v) ^ 2 := by
  simp only [trace, diag, mul_apply, vecMulVec_apply, dotProduct, sq, Finset.sum_mul,
    Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

end EmergentTransport

# What is not proved here

Lean proves exactly the statements written, under exactly the hypotheses written.

## `EmergentTransport/Basic.lean` (paper of 29 June 2026)

* Theorem 8 (the ledger's second-order expansion) is not formalized. The correct coefficient
  is `−½ Tr(RERE)`, with product weights `1/((λₙ+η)(λₘ+η))`, not gap-squared weights. The
  gap-squared weights belong to the separate fidelity-susceptibility object.
* Theorems 1–3 (the Jacobi spine, the collinear horizon, curvature-induced exceptional points),
  Theorem 4 (Kakeya directional support sets), Theorem 9 (Seeley–DeWitt compatibility),
  Lemma 10, the gluing Theorem 15 and the Kato-type continuity statements (Prop. 4, Thm. 17)
  are not formalized.
* Proposition 2 is proved as the pointwise identity `Tr(RE) = 0` for real matrices with `R`
  symmetric, that is, at a self-adjoint baseline. The complex contour version and the
  contour-integral derivative are not formalized.
* Theorem 14 is proved as `Tr(Π₁Π₂) = ‖Π₂Π₁‖²_F ≥ 0` and, for rank one, `(u·v)²`. The
  principal-angle form `Σ cos²θᵢ` for higher-rank projectors is not formalized.

## `EmergentTransport/GapsAndTotals.lean` (paper in preparation, *Gaps and Totals*)

Proved (18 theorems): the redistribution operator `F(Ω,Π) = ΠΩQ + QΩΠ` is traceless; its two
off-diagonal blocks are those of `Ω`; `F = 0 ↔ ΩΠ = ΠΩ`; `Ω = ΠΩΠ + ΠΩQ + QΩΠ + QΩQ`; the
`(1,2)` and `(2,1)` blocks are square-zero; for self-adjoint `Ω` they are transposes of each
other; `‖F‖²_F = 2‖ΠΩQ‖²_F` and `½‖[Ω,Π]‖²_F = ‖ΠΩQ‖²_F`; and `[Ω,Π]` is skew. The norm
identities require `Ω` self-adjoint and `Π` orthogonal — without those hypotheses they are
false, and `FalseControls/norm_needs_selfadjoint.lean` records a counterexample.

**Not formalized in that file, and why.**

* Kato's analytic bound on the Riesz projector (`‖Ṗ‖ ≤ ‖Ȧ‖/γ`), the Puiseux exponents
  `|t|^{1/2}` of eigenvectors at an exceptional point, the analyticity of a cluster projector
  through an interior degeneracy, and spectral flow as a winding number: these are analytic
  statements about families, not finite algebraic identities, and they are stated in the paper
  with proofs and graded `[T]`, not `[L]`. Do not read their absence here as a claim.
* The quantum geometric tensor `Q_μν = Tr(∂_μP ∂_νP)` and the curvature bound
  `|Im Q_μν| ≤ 2√(g_μμ g_νν)` need a differentiable family; the finite algebraic core
  (`g(Ẋ,Ẋ) = 2‖ΠẊQ‖²_F ≥ 0` for a projector-compatible variation) is what the kernel checks.
* The shape-sphere spectrum of §7 is certified by `scripts/gates/g01_shape_spectrum.py`
  (19 assertions, machine precision) and by two independent charts, not by the kernel.
  Formalizing it would need the Fubini–Study chart and square roots; the gate is the proof of
  record for that section, and it is graded `[V]`, not `[T]`.
* The per-pair capacity identity `‖∇d_ij‖² = 1/m_i + 1/m_j − d_ij²` is proved on paper
  (`notes/`, swarm direction D7) and verified by gate `g01`(g) for `N ≤ 8` with unequal
  masses; it is not formalized.

## A correction recorded rather than erased

The corpus's three-body paper states that the shape→distance differential has spectrum
`σ_min = cos²ϑ`, `σ_max = 1`. Gate `g01` shows that `σ_max²` is not constant and equals
`1.5` at the equilateral shapes, so the statement cannot be rescaled into truth. What holds is
`σ₁² + σ₂² = 3` identically, rank drop exactly on the collinear locus, `det = 9/4` exactly at
the equilateral shapes, a linear isotropic cone of slope 3, and eigen-line holonomy `−1`. The
gate keeps both the claim and the measurement.

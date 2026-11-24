# Proofs and checks from swarm `smwtveb8o` (8 directions, all solved)

Copied from `.ultramath/smwtveb8o/m*/results/swarm/` on the day the swarm ended, so that the
`[T]` proofs and the `[V]` checks cited by the paper live in the repository rather than in the
swarm's own directory. The `.ultramath/` originals are untouched.

Every report carried at least one correction to the task's statement. The corrections are
recorded in `notes/02_PLAN.md` (Theorem list v2) and summarised below; the *superseded*
statement is kept, not deleted.

| dir | member | file | result | correction found |
| :-- | :-- | :-- | :-- | :-- |
| D1 | m2 | `D1_m2.md` | redistribution: trace, blocks, `F=0 ↔ [Ω,Π]=0`, non-normal example | `‖F‖² = ‖[Ω,Π]‖²`, not `½‖[Ω,Π]‖²` |
| D2 | m7 | `D2_m7.md` | QGT: Hermiticity, PSD, closedness, Chern periods, Riesz counterexample | `Tr(∂P∂P)` is real; the QGT is `Tr(P∂P∂P)` |
| D3 | m1 | `D3_m1.md` | sharp metric–curvature bound, equality cases, rank `k` failure of constant 2 | constant 2 belongs to the curvature, not to `Im Q` |
| D4 | m5 | `D4_m5.md` | Weyl, Riesz `C¹` with sharp `π/2γ` and `1/γ`, sharpness families | `‖Ṗ‖_F = √2‖v̇⊥‖`; the identity holds in *operator* norm |
| D5 | m4 | `D5_m4.md` | exceptional point: Puiseux `±t^{1/2}`, total Riesz projector, coupled resolvent | eigenvectors *coalesce* like `\|t\|^{1/2}`; derivatives diverge like `\|t\|^{-1/2}` |
| D6 | m8 | `D6_m8.md` | winding `∈ ℤ`, homotopy classification, `exp(iγ₋)=(-1)^w` | spectral flow ≠ winding |
| D7 | m6 | `D7_m6.md` | per-pair capacity `‖∇d_ij‖² = 1/m_i + 1/m_j − d_ij²` | literal statement needs the non-collision hypothesis |
| D8 | m3 | `D8_m3.md` | `tr = 3`, `det = 12A²/(d₁²d₂²d₃²)`, linear isotropic cone, collision non-extension | the gap closes linearly, not quadratically |

Checked by me before acceptance: D7 and D8 re-derived with independent implementations
(SVD projection; Hopf vs Cartesian chart); D1 verified in Lean
(`EmergentTransport/GapsAndTotals.lean`) and by a 2×2 counterexample; D3/D2 verified by the
Cauchy–Schwarz argument on `Z_μ = (1−P)∂_μv`; D5 by the explicit `2×2` Jordan family; D6 by
the two counterexamples and the `c ≡ 0` Berry identity. The companion `.py` files are the
members' own deterministic checks and are re-runnable as they stand.

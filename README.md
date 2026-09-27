<div align="center">

# Intrinsic Emergent Transport Geometry: Emergent Metrics from Spectral Projector Hierarchies — Lean proofs

[![Lean proof check](https://github.com/dicipler-pixel/emergent-transport-lean/actions/workflows/build.yml/badge.svg)](https://github.com/dicipler-pixel/emergent-transport-lean/actions/workflows/build.yml)
![Lean](https://img.shields.io/badge/Lean-v4.34.1-blue)
![Theorems](https://img.shields.io/badge/theorems-11-2EA043)
![sorry](https://img.shields.io/badge/sorry-0-2EA043)
![Code: MIT](https://img.shields.io/badge/code-MIT-lightgrey)
![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey)
[![Paper DOI](https://img.shields.io/badge/paper-10.5281%2Fzenodo.21089303-blue)](https://doi.org/10.5281/zenodo.21089303)

Jeromie Beasley

</div>

---

## The idea in one line

Transport lives on projectors, not vectors. A commutator with a projector is always
off-diagonal, the first variation of the trace-log ledger cancels at a normal baseline, the
projector–metric correspondence holds in its daggered form, and the overlap between two
subspaces is a squared norm, `Σ cos²θᵢ`.

## What is proved

| Paper | Result | Theorem |
| :--- | :--- | :--- |
| Prop. 2 | A symmetric matrix times a skew matrix is traceless, so the first variation of `Tr log(H + ηI)` vanishes at the normal baseline | `trace_sym_skew` |
| Lemma 6, Cor. 4.2 | For a projector `Π`, `Π[X,Π]Π = 0` and `(1−Π)[X,Π](1−Π) = 0` | `commutator_offdiag` |
| Theorem 7 | `Tr(Πₙ Eᵀ (1−Πₙ) E) = Σ_{m≠n} E_{mn}²`; for skew `E` the undaggered trace is its negative | `trace_proj_mul`, `proj_mul_apply`, `metric_correspondence`, `undaggered_sign` |
| Theorem 7 | For any orthogonal projector and skew `E`: `½‖[E,Π]‖²_F = Tr(ΠEᵀ(1−Π)E)`, the same `½‖commutator‖²` shape as the connection energy of [*Non-normality is connection energy*](https://github.com/dicipler-pixel/-connection-energy-lean) | `half_commutator_norm` |
| Prop. 3, Thm. 13 | `Tr(UΠUᵀ · UVUᵀ · UWUᵀ) = Tr(ΠVW)` for orthogonal `U` | `gauge_invariance` |
| Theorem 14 | `Tr(Π₁Π₂) = ‖Π₂Π₁‖²_F ≥ 0`, and for rank one `Tr(P_uP_v) = (u·v)²` | `persistence_frobenius`, `persistence_nonneg`, `persistence_rank_one` |

Theorem 7 is proved in its corrected form. The daggered trace `Tr(ΠEᵀ(1−Π)E)` equals the
off-diagonal weight. The form `½ Tr(ΠE(1−Π)E)` has the opposite sign for skew `E` and carries an
extra factor ½. The metric–curvature inequality of Theorem 12 is proved in
[iqgt-grassmannian-lean](https://github.com/dicipler-pixel/iqgt-grassmannian-lean). The file is
[`EmergentTransport/Basic.lean`](EmergentTransport/Basic.lean). What is not proved is in
[`LIMITATIONS.md`](LIMITATIONS.md).

## How it is checked

Every push runs [the proof check](.github/workflows/build.yml): build against Lean v4.34.1 and
Mathlib v4.34.1, independent replay in Lean's kernel checker, an axiom audit (only `propext`,
`Classical.choice`, `Quot.sound`), and three deliberately false statements that must fail.

## The paper

*Intrinsic Emergent Transport Geometry: Emergent Metrics from Spectral Projector Hierarchies*, Jeromie Beasley. DOI
[10.5281/zenodo.21089303](https://doi.org/10.5281/zenodo.21089303) (always opens the newest version).

## Licence

Copyright (c) 2026 Jeromie Beasley. Code and proofs: [MIT](LICENSE). Written text:
[CC BY 4.0](LICENSE-CC-BY-4.0.md). See [`LICENSING.md`](LICENSING.md). Citation metadata is in
[`CITATION.cff`](CITATION.cff); how AI tools were used is stated in [`AI_USE.md`](AI_USE.md).

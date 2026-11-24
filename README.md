<div align="center">

# Intrinsic Emergent Transport Geometry: Emergent Metrics from Spectral Projector Hierarchies — Lean proofs

[![Lean proof check](https://github.com/dicipler-pixel/emergent-transport-lean/actions/workflows/build.yml/badge.svg)](https://github.com/dicipler-pixel/emergent-transport-lean/actions/workflows/build.yml)
![Lean](https://img.shields.io/badge/Lean-v4.34.1-blue)
![Theorems](https://img.shields.io/badge/theorems-29-2EA043)
![sorry](https://img.shields.io/badge/sorry-0-2EA043)
![Code: MIT](https://img.shields.io/badge/code-MIT-lightgrey)
![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey)
[![Paper DOI](https://img.shields.io/badge/paper-10.5281%2Fzenodo.21089303-blue)](https://doi.org/10.5281/zenodo.21089303)

Jeromie Beasley

</div>

---

## The idea in one line

Transport lives on projectors, not vectors. A commutator with a projector is always
off-diagonal, the first variation of the trace-log ledger cancels at a self-adjoint baseline,
the projector–metric correspondence holds in its daggered form, and the overlap between two
subspaces is a squared norm, `‖Π₂Π₁‖²_F` (for two lines, `cos²θ`).

## What is proved

Paper labels follow the 29 June 2026 edition named in [`PROVENANCE.md`](PROVENANCE.md); the
version behind the DOI may number them differently.

| Paper | Result | Theorem |
| :--- | :--- | :--- |
| Prop. 2 | A symmetric matrix times a skew matrix is traceless, so the first variation of `Tr log(H + ηI)` vanishes at a self-adjoint (symmetric) baseline | `trace_sym_skew` |
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
`Classical.choice`, `Quot.sound`), and six deliberately false statements that must fail.

## The finite core of *Gaps and Totals* (in preparation)

[`EmergentTransport/GapsAndTotals.lean`](EmergentTransport/GapsAndTotals.lean) proves the
redistribution theorems of the second paper: with `Π` an orthogonal projector, `Q = 1 − Π`
and `F(Ω,Π) = ΠΩQ + QΩΠ`,

| Result | Statement | Theorem |
| :--- | :--- | :--- |
| Thm 1 | `Tr F = 0`: the redistribution operator is traceless | `redistribution_traceless` |
| — | the `(1,2)` and `(2,1)` blocks of `F` are those of `Ω` | `redistribution_block12`, `redistribution_block21` |
| Thm 2 | `F = 0 ↔ ΩΠ = ΠΩ` (no self-adjointness needed) | `redistribution_zero_iff_commute` |
| — | block decomposition `Ω = ΠΩΠ + ΠΩQ + QΩΠ + QΩQ` | `block_decomposition` |
| Thm 3a | for self-adjoint `Ω`: `‖F‖²_F = 2‖ΠΩQ‖²_F` | `redistribution_norm` |
| Thm 3b | for self-adjoint `Ω`: `[Ω,Π]` is skew | `commutator_skew` |
| Thm 3c | for self-adjoint `Ω`: `½‖[Ω,Π]‖²_F = ‖ΠΩQ‖²_F` | `half_commutator_norm` |

The two norm identities **need** `Ω` self-adjoint; `FalseControls/norm_needs_selfadjoint.lean`
exhibits the failure. What is *not* formalized there — Kato's projectors bound, Puiseux
exponents at an exceptional point, spectral flow, the shape-sphere spectrum — is listed in
[`LIMITATIONS.md`](LIMITATIONS.md), with the gate that certifies each instead.

## The papers

**In preparation — the framework's statement.** *Gaps and Totals: an operator-first theory of
transport invariants, with the shape sphere solved exactly.* Draft in
[`paper/main.pdf`](paper/main.pdf) (18 pp.), source in `paper/`, ledger in
[`paper/MANIFEST.md`](paper/MANIFEST.md) and `paper/main.tex` \S C. Its finite algebraic core is
`EmergentTransport/GapsAndTotals.lean`; its numerical claims come from
`scripts/gates/g01_shape_spectrum.py` (20 assertions) and `g02_gap_hierarchy.py` (13).

**Published edition — the Lean companion's source.** *Intrinsic Emergent Transport Geometry:
Emergent Metrics from Spectral Projector Hierarchies*, Jeromie Beasley. DOI
[10.5281/zenodo.21089303](https://doi.org/10.5281/zenodo.21089303) (always opens the newest version).

## Licence

Copyright (c) 2026 Jeromie Beasley. Code and proofs: [MIT](LICENSE). Written text:
[CC BY 4.0](LICENSE-CC-BY-4.0.md). See [`LICENSING.md`](LICENSING.md). Citation metadata is in
[`CITATION.cff`](CITATION.cff); how AI tools were used is stated in [`AI_USE.md`](AI_USE.md).

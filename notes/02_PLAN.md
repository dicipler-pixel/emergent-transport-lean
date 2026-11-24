# Plan — the new paper

Working title:

> **Gaps and Totals: an operator-first theory of transport invariants, with the shape sphere
> solved exactly**

Short name in the repo: `gaps-and-totals`. Status: specification, not draft.

---

## The thesis, in three sentences

A transport invariant is only as stable as the gap that protects it, and that gap — not the
degree of derivation — is what orders the hierarchy of subspaces, projectors and integers.
What a transport cannot forget is a **total**: for the `N`-body distance map the total
squared capacity is exactly `N(N−2)` for every configuration, so the shape only decides how
the total is distributed. One geometry can be solved completely — the equal-mass planar shape
sphere — and there the distribution is an isotropic cone of slope 3, rank-dropping exactly
where the gap is largest.

Everything in the paper must be a consequence of one of those three sentences, or be marked
`[H]`.

## Why this and not an eleventh coat

The corpus's own best moments (paper 10's honest conjectures, paper 4's interlacing theorem,
paper 1's Lean core) share a property: they are *narrow enough to be wrong*. The new paper
keeps that property — three claims, each with a constant or a closed form — and drops the
breadth. Ten applications become one exact example plus a graded appendix.

## Reader-facing promises (what the abstract may claim)

1. A theorem for each level of the hierarchy, with an explicit constant: eigenvalues
   (Lipschitz), eigenvectors (rate `1/γ_int`), cluster projectors (rate `1/γ_ext`, analytic
   through interior exceptional points), integers (locally constant, spectral flow = winding).
2. The correction of the hierarchy principle: a *rank-one* projector is not more stable than
   an eigenvector — the gain belongs to clusters, and the protecting gap must be named.
3. The redistribution theorem: `F(Ω,Π) = PΩQ + QΩP` is trace-free, vanishes iff `[Ω,Π]=0`
   for self-adjoint `Ω`, and `‖F‖²_F = 2‖PΩQ‖²_F = ½‖[Ω,P]‖²_F`.
4. The quantum geometric tensor of a projector family is `Q_μν = Tr(∂_μP ∂_νP)`; its real part
   is the metric, its imaginary part the Berry curvature, and `|Im Q_μν| ≤ 2√(g_μμ g_νν)`.
5. The capacity sum rule `Σ_{i<j}|∇d_ij|² = (N−1)Σ1/m_i − Σd_ij²` (hence `N(N−2)`).
6. The exact three-body spectrum: sum rule, `det = 0` on the collinear equator, `det = 9/4` at
   the equilateral shapes, linear isotropic cone of slope 3, holonomy `−1`.
7. Refraction as the geodesic equation of `ĝ = R·g`, with the variational hypothesis stated.
8. A grade ledger, a Lean kernel, gates, and a section titled "What would prove this wrong".

The abstract may **not** claim: a derivation of `Λ`; that the framework has been validated by
published data; that the hierarchy principle holds as originally stated; that `σ_max = 1`.

## Structure and length

| § | content | theorems | artefacts |
| :-- | :-- | :-- | :-- |
| 1 | What this is; the one idea; what is new; what is not claimed | — | — |
| 2 | Setting, notation table, conventions (`[T]/[V]/[C]/[D]/[H]`) | Def 1–6 | — |
| 3 | Redistribution: what moves between blocks | Thm 1–3 | gate `g02`, Lean |
| 4 | Projector geometry: the quantum geometric tensor and the curvature bound | Thm 4–6 | gate `g03`, Lean |
| 5 | The gap hierarchy: eigenvalues, eigenvectors, clusters, integers | Thm 7–11 | gates `g04`–`g06`, Lean |
| 6 | Totals: the capacity sum rule | Thm 12–13 | gate `g01`(f) |
| 7 | The shape sphere solved exactly | Thm 14–17 | gate `g01` |
| 8 | Refraction as conformal geodesics | Thm 18 | gate `g07` |
| 9 | What this does not do (graded physics applications, in one place) | — | — |
| 10 | What would prove this wrong | — | — |
| 11 | Open problems (numbered, each with a reason it is open) | — | — |
| A | Proofs of the imported lemmas (self-containedness) | — | — |
| B | The grade ledger, claim by claim | — | `paper/LEDGER.md` |
| C | Reproduction: how to re-run the kernel and the gates | — | `paper/MANIFEST.md` |

Target 26–32 pages, of which §3–§8 is about 14.

## Theorem list, with provenance and status

`S` = stated, `P` = proof drafted, `L` = Lean-checked, `G` = gate passes, `C` = corrected
during review. A theorem is not allowed into the paper below `P`, and nothing enters the
abstract below `L` or `G`.

| # | statement | source | status |
| :-- | :-- | :-- | :-- |
| 1 | `F(Ω,Π)` trace-free; block decomposition | paper 3 | P (D1) |
| 2 | self-adjoint: `F=0 ⟺ [Ω,Π]=0 ⟺` reducing | paper 3 | P (D1) |
| 3 | `‖F‖²_F = 2‖PΩQ‖²_F = ½‖[Ω,Π]‖²_F = 2Tr(PΩQΩ)` | paper 1/3 | L (partly), G `g02` |
| 4 | `Q_μν = Tr(∂_μP∂_νP)` Hermitian; `Re` PSD | paper 3 | P (D2) |
| 5 | `Im Q` = Berry curvature with the stated factor | paper 3 | P (D2) |
| 6 | `\|Im Q_μν\| ≤ 2√(g_μμ g_νν)`, sharp | paper 3 (as `\|Ω(V,W)\| ≤ …`) | P (D3) |
| 7 | Weyl: `\|λ_i(A)−λ_i(A')\| ≤ ‖A−A'‖` | classical | to prove/cite |
| 8 | cluster projector: `‖P_I(A)−P_I(A')\| ≤ (‖δ‖/γ)/(1−‖δ‖/γ)` | Kato `[C]` | to state with proof |
| 9 | rank-one: `‖Ṗ‖_F = ‖v̇⊥‖`; no stability gain | **new (correction R2)** | P (D4) |
| 10 | EP: `\|t\|^{1/2}` eigenvectors, analytic cluster projector | paper 3/5 | P (D5) |
| 11 | spectral flow = winding of `a+ib` | paper 3 (currency) | P (D6) |
| 12 | per-pair capacity: `‖∇_shape d_ij‖² = 1/m_i + 1/m_j − d_ij²` at unit inertia, zero centre of mass, off the collision locus | **new** (swarm D7, m6) | P (proof checked), G `g01`(g) |
| 13 | capacity sum rule `Σ_{i<j}‖∇d_ij‖² = (N−1)Σ1/m_i − Σd_ij²`, hence `N(N−2)` | **new** | P (corollary of 12), G `g01`(f) |
| 13b | `Σ_{i<j}m_im_j\|r_i−r_j\|² = (Σm)·I` at zero centre of mass | classical | P (swarm D7) |
| 14 | `σ₁²+σ₂² = 3` | **new (corrects paper 5)** | G `g01`(a) |
| 15 | `det = 0` collinear, `= 9/4` equilateral, max | **new (corrects paper 5)** | G `g01`(b,c) |
| 16 | linear isotropic cone, slope 3, holonomy `−1` | **new (corrects paper 5)** | G `g01`(d,e) |
| 17 | biaxial reading = cone tilt under mass breaking | **conjecture** | gate `g08` to settle |
| 18 | Snell from `ĝ = R·g`, `n = √R` | paper 3/5, sharpened | P (D9) |

Theorem 17 is the only conjecture in the theorem list. If the gate cannot settle it, it moves
to §11 with the gate output attached.

## Editorial rules (binding)

1. **One claim per section**, and every section ends with a sentence saying what would
   falsify its claim.
2. **Self-contained.** Every imported result is restated with proof in Appendix A. Companion
   papers appear as `[C]` context only, never as a dependency.
3. **Numbers come from gates.** No number enters the prose by hand. `paper/LEDGER.md` maps
   each numeral to a gate id and a JSON key.
4. **Grades.** `[T]` theorem, `[V]` gate-verified with the gate named, `[C]` cited with
   hypotheses, `[D]` data under a stated protocol, `[H]` hypothesis. A mixed chain is graded
   by its weakest link, and the link is named.
5. **Two figures maximum**, both read from gate JSON: (i) the two-sheet structure on the
   shape sphere with the collinear equator and the isotropic cone; (ii) the gap hierarchy as
   a log-log stability plot (`1/γ_int` vs `1/γ_ext` vs constant).
6. **No unproved adjective.** "Universal", "emergent", "intrinsic", "exact" only where a
   theorem or a definition licenses it.
7. **Version-pinned DOI** in `CITATION.cff`; `MANIFEST.md` hashes paper, Lean, gates.

## Verification

* **Lean** (`EmergentTransport/GapsAndTotals.lean`): the finite algebraic core — Theorems
  1–3, 4–6 (matrix identities), 9 (rank one), 13, 14 for `n=3`. Axiom audit; three new false
  controls; hashes. Target: `sorry`-free, `verify.py` green.
* **Gates** (`scripts/gates/`): `g01` shape sphere (done, 14 assertions), `g02`
  redistribution, `g03` QGT and the curvature bound, `g04` projector stability rates, `g05`
  EP Puiseux exponents and cluster analyticity, `g06` spectral flow, `g07` Snell from a
  conformal geodesic, `g08` cone tilt under mass breaking.
* **Independence.** Every gate written by one route and checked by a second where cheap: `g01`
  already agrees between Hopf and Cartesian charts.

## Build order (slow, in this order)

1. `g02`–`g07` and the swarm proofs land → freeze the theorem list. **Now.**
2. Lean core for Theorems 1–6, 9, 13, 14. Kernel green before prose.
3. §3–§5 written against the Lean names, not from memory.
4. §6–§8 written against the gates.
5. §1, §9–§11 last: the introduction is a summary of what exists, never a promise.
6. Ledger, manifest, README, LIMITATIONS. Then the abstract, written last.

## Explicitly out of scope

Cosmology (paper 8) beyond one graded paragraph; the psychophysical colour-space reading
(no theorem, no gate); the ⁸⁷Rb and heat-engine material beyond a graded `[D]` paragraph
noting it is a consistency check on published data; the Ramanujan/Catalan arithmetic
(paper 7) beyond a citation; the figure-eight choreography beyond one `[V]` remark; any claim
that the framework "explains" a physical system.

---

# Theorem list v2 — frozen after the first swarm (corrections recorded, not erased)

Seven directions returned proofs; every one of them carried a correction to the version above.
The corrections are the valuable part, so they are kept with the statement they changed.

| # | v1 statement | v2 statement (frozen) | why it changed |
| :-- | :-- | :-- | :-- |
| 3 | `‖F‖² = 2‖ΠΩQ‖² = ½‖[Ω,Π]‖²` | `‖F‖²_F = 2‖ΠΩQ‖²_F = ‖[Ω,Π]‖²_F`, and separately `½‖[Ω,Π]‖²_F = ‖ΠΩQ‖²_F` | v1 mixed two identities; `Π=diag(1,0)`, `Ω=σ_x` gives `‖F‖²=2`, `½‖[Ω,Π]‖²=1` |
| 4 | `Q_μν := Tr(∂_μP∂_νP)` is the QGT | `Q_μν := Tr(P∂_μP∂_νP)` is the QGT; `Tr(∂_μP∂_νP) = 2 Re Q` | `Tr(∂P∂P)` is **real** for Hermitian `P`, so its imaginary part cannot be curvature. Two members found this independently |
| 5 | `Im Q` = Berry curvature | curvature 2-form `= −2 Im Q`; `Q` Hermitian and PSD for orthogonal `P`, **not** for Riesz projectors (`Re Q` goes negative — counterexample in `D2_m7.md`) | factor and domain |
| 6 | `\|Im Q_μν\| ≤ 2√(g_μμ g_νν)` | `\|Im Q_μν\| ≤ √(g_μμ g_νν)`, sharp (Cauchy–Schwarz on `Z_μ=(1−P)∂_μv`); curvature `≤ 2√(g_μμ g_νν)` | the constant 2 belongs to the curvature, not to `Im Q` |
| 10 | eigenvectors blow up like `\|t\|^{1/2}` at an EP | unit eigenvectors **coalesce** at distance `2\|t\|^{1/2}`; derivatives and `κ₂(V)` diverge like `\|t\|^{-1/2}` | coalescence rate confused with divergence rate |
| 10b | block-diagonal 4×4 family gives a projector bound | block-diagonal ⇒ the cluster projector is **constant** (bound 0, trivial); the theorem must be stated for the **coupled** family, and the coupled derivative bound is `[V]`, not `[T]`, until proved | the v1 hypothesis made the claim vacuous |
| 11 | spectral flow = winding | **false**. `H=cos t σ₁+sin t σ₂` has `w=1` and spectral flow 0; `H=σ₃` has `w` undefined. True: `w(a+ib) ∈ ℤ` when `a+ib ≠ 0` on the loop, and it is the obstruction to a gapped trivialisation; for `c≡0`, `exp(iγ₋) = (−1)^w` | the integer is not a crossing count |
| 14 | `σ₁²+σ₂² = 3` | unchanged — and now proved by a cleaner route: `‖∇d_a‖² = 2 − d_a²` per distance, sum `6 − 3` | no square roots differentiated |
| 15 | `det = 0` collinear, `= 9/4` equilateral | unchanged, plus the closed form `det M = 12A²/(d₁²d₂²d₃²) = 3·16A²/(4xyz)` (Heron) | new, gate `g01`(h), 81 shapes to `1.5e−9` |
| 16 | quadratic closing | `(σ₁²−σ₂²)² = 9ρ² + O(ρ³)`, `σ₁²−σ₂² = 3ρ + O(ρ²)`: the gap closes **linearly**, its square quadratically | the v1 wording was wrong, and so was the corpus's |
| 16b | — | `det M` has **no continuous extension** to a collision (limits 0 and 2 at the 23-collision), so the two sheets live on the *regular* part, not on the closed sphere | new; changes the domain statement of §7 |
| 12 | — | per-pair capacity `‖∇d_ij‖² = 1/m_i + 1/m_j − d_ij²` at unit inertia | new, and it is what makes the sum rule a corollary |

**A corollary that the swarm produced by accident, and it is the best thing in the section.**
Direction D6 gives `exp(iγ₋) = (−1)^w` for the two-level family; gate `g01`(e) measures
holonomy `−1` around the equilateral shape. So the integer level of the gap hierarchy and the
shape-sphere cone are the same object seen twice. That link belongs in §5 and §7.

**Verification status.** `python3 scripts/verify.py --direct`: 29 theorems, axioms
`{propext, Classical.choice, Quot.sound}`, 6 false controls rejected. Gate `g01`: 20
assertions. The `[L]` column now covers Theorems 1–3 only; the analytic theorems (7–11) are
`[T]` on paper, the shape-sphere ones `[V]` by gate, and `LIMITATIONS.md` says exactly that.

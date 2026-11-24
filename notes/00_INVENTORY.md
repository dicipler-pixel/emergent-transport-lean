# Inventory of the corpus — ten preprints, one program

Source: `attachments/install-all-the-skills-5gge/Publication date.txt` (a search-results
export, 37,830 bytes). All ten records are by **Jeromie Beasley**, Open Access, preprint,
publication dates 23 June – 27 September 2026. Counts are the platform's view counts as
displayed; they are not citations and say nothing about correctness.

Read this file as a **ledger**, not a summary: for each paper, what it *actually proves*
(as opposed to what it names), what is load-bearing for anything else, and what would
break if the claim were false.

Convention used throughout the notes:
`[T]` theorem (proved), `[V]` verified by a named computation, `[D]` data reported under a
stated protocol, `[C]` cited from the literature, `[H]` hypothesis or interpretation.

---

## 1. Intrinsic Emergent Transport Geometry (30 Jun 2026, v1 · 9,836)

**Thesis.** Transport lives on projector bundles, not on vectors or trajectories; metrics,
curvature, persistence and directional organisation are reconstructed from the continuous
evolution of admissible subspaces.

**What it proves** — five finite-dimensional identities, all of which are formalised in
this repository (`EmergentTransport/Basic.lean`, 11 theorems, 3 false controls, axiom audit):

| result | statement | status |
| :-- | :-- | :-- |
| Prop. 2 | `Tr(RE) = 0` for symmetric `R`, skew `E`; first variation of the trace-log vanishes at a self-adjoint baseline | `[T]` Lean `trace_sym_skew` |
| Lemma 6 | `Π[X,Π]Π = 0` and `(1−Π)[X,Π](1−Π) = 0` | `[T]` Lean `commutator_offdiag` |
| Thm 7 | `Tr(ΠₙEᵀ(1−Πₙ)E) = Σ_{m≠n}E_{mn}²`; the undaggered printed form has the wrong sign for skew `E` | `[T]` Lean `metric_correspondence`, `undaggered_sign` |
| Thm 7′ | `½‖[E,Π]‖²_F = Tr(ΠEᵀ(1−Π)E)` | `[T]` Lean `half_commutator_norm` |
| Prop. 3 | `Tr(UΠUᵀ·UVUᵀ·UWUᵀ) = Tr(ΠVW)` for orthogonal `U` (gauge invariance) | `[T]` Lean `gauge_invariance` |
| Thm 14 | `Tr(Π₁Π₂) = ‖Π₂Π₁‖²_F ≥ 0`; rank one `= (u·v)²` | `[T]` Lean `persistence_*` |

**Load-bearing.** This is the only paper in the corpus with a kernel-checked core, and the
only one whose central identities survive a hostile reading unmodified. Everything else in
the corpus that says "the metric is the projector's off-diagonal weight" is quoting this.

**Named but not proved.** "The Hierarchy Principle of Structural Persistence" — the claim
that invariants form a hierarchy from fragile eigenvectors to stable projectors to global
spectral invariants. It is stated as a principle; no inequality is attached to it. See
review R2: as stated it is *false* at the first level, and repairable at a cost.

**Not formalised** (per `LIMITATIONS.md`, honestly listed): the ledger's second-order
expansion with weights `−½Tr(RERE)`; Theorems 1–4, 8, 9, Lemma 10, Thm 15, Thm 17; the
complex contour version of Prop. 2; the principal-angle form of Thm 14.

**Verdict.** Survives. Foundation stone. The one thing to fix is the *edition* problem
(below, R7).

---

## 2. The 5D Spectral Anatomy of Four-Body Obstructions (23 Jun 2026, v1 · 349)

**Thesis.** After translation, rotation and scale, four bodies in 3D live on a 5-dimensional
stratified shape manifold `Σ₄` (trace-one PSD symmetric 3×3 matrices, stratified by
collisions). Build an intrinsic transport operator `A_intr` on `TΣ₄`, study its spectrum and
pseudospectrum; binary collision hypersurfaces act as refraction interfaces; the collinear
horizon is generically semi-simple; defectiveness is confined to higher-codimension strata.

**Load-bearing.** The explicit 5×5 operator and the stratification. Note the arithmetic:
four bodies in three dimensions is exactly the **square case** `N = d+1`, so paper 4's
theorem (strictly real spectrum in the regular interior, defectiveness only on `det G = 0`)
is *the* proof of this paper's central structural claim. The two papers were written a
month apart and the dependency is not stated. It should be.

**Named but not proved.** "Reflective Closure of Transport": admissible evolution is the
projection onto the tangent Grassmannian, and the projection defect induces a backreaction
that drives obstruction/refraction/non-normality. The projection-defect part is algebra
(paper 1's Lemma 6 + the off-diagonal block); the *backreaction* part — that the defect
*drives* anything — is `[H]` and should be graded so.

**At risk.** "The six binary collision hypersurfaces act as geometric refraction interfaces"
is an interpretation supported by the behaviour of singular values near them, not a derived
law. Refraction needs a variational principle (see paper 5 / review R4).

**Verdict.** Subsists, but as a *special case* of paper 4 rather than an extension of the
program. Fold into the new paper as the `d = 3` instance of the square-case theorem.

---

## 3. Universal Projector Geometry from Electrical Measurements (27 Sep 2026, v4 · 23,853)

**Thesis.** Coordinate-free geometric structure from *measured* covariance operators:
spectral decomposition → rank-*k* projectors → points on the Grassmannian; structural
transition `Ω`; redistribution `F(Ω,Π)` as the central object; invariants (principal angles,
transport capacity, quantum metric, chirality, persistence, rigidity, effective transport
dimension); the bound `|Ω(V,W)| ≤ 2√(C(V)C(W))·sin θ_G`; the refraction law
`R₁sin²θ₁ = R₂sin²θ₂`; a topological continuation on the A-polynomial of the figure-eight
knot complement with the Levine–Tristram signature as the self-adjoint ancestor of the
winding; an 8-channel flux-tunable transmon heat engine with explicit estimators; a
reanalysis of published ⁸⁷Rb Bloch-state tomography reproducing `C = −0.999` against
`−1.00 ± 0.02`.

**Load-bearing.** Three things, in order of value:
1. **The five-grade ledger** and the rule that a mixed chain is graded by its weakest link.
   This is the corpus's best invention and should be the new paper's first editorial rule.
2. **The independence protocol** — split archived shots into disjoint prediction and
   measurement halves so the interface-refraction test is falsifiable *on the instrument's
   own data*. This is the only genuinely *falsifiable* apparatus in the corpus.
3. `F(Ω,Π)` and the compatibility criterion (now a theorem — see D1 of the swarm).

**At risk.**
- The ⁸⁷Rb result is a **consistency check on somebody else's published data**: a known
  estimator reproducing a known Chern number from a known lattice. It is evidence that the
  estimator is implemented correctly, not that the framework's distinctive claims hold.
  Any abstract sentence that lets a reader hear "validated" is an overclaim. Keep it, grade
  it `[D]`, and say plainly what it does and does not discriminate.
- The bound as written is not a statement until `C(·)` is defined. `C` is used for transport
  capacity, for the persistence overlap, and for the "boundary census" in paper 10. Three
  different objects, one symbol. (Review R3.)
- The figure-eight/A-polynomial continuation is *imported* mathematics (A-polynomial, Culler–
  Shalen; Levine–Tristram; see `[C]`). The framework's contribution there is the reading,
  not the topology. Say so.

**Verdict.** The methodological flagship. Repair the `C(·)` ambiguity and the "validated"
register; keep the protocol; move the physics to its own graded section.

---

## 4. The Square Case: Gram Reduction and Spectral Transport for N = d+1 Bodies (9 Aug 2026, v1 · 428)

**Thesis.** When `N = d+1` the mass-weighted Jacobi configuration matrix `X` is `d×d`, so
`G = XᵀX` is an unconstrained PSD form and its trace-one slice *is* shape space; `det G` is
the orientation variable, giving a double cover branched over `det G = 0`. The transport
operator on symmetric-traceless perturbations splits into an **eigenvalue sector** and an
**eigenframe sector**; the eigenframe spectrum is exactly the pairwise sums of the
eigenvalues of a commuting tensor `T`; the eigenvalue sector is a rank-one modification of a
diagonal matrix, so a secular equation with positive weights forces **strict interlacing**;
hence the spectrum is real in the regular interior even when the operator is non-normal; a
diagonal similarity to a symmetric rank-one update gives an independent proof and identifies
the self-adjoint inner product; the similarity degenerates exactly at `det G = 0`, which is
where a genuine Jordan block can appear. Then: the Koszul–Vinberg volume structure on the
cone of positive-definite symmetric matrices, `log` of the characteristic function
proportional to `log` of the simplex volume, the dual coordinate `G⁻¹` forced
kinematically, and closed-form geodesics.

**Load-bearing.** This is the most substantial mathematics in the corpus: real theorems,
stated hypotheses, an explicit statement of the regime where the construction *must* be
replaced (`N−1 > d`; the `d=3, N=5` case analysed far enough to isolate the support-moving
sector as the open part), and a recorded **correction** (coincident boundary pins are
semi-simple, not defective) rather than a silent fix. Everything in papers 2 and 5 that is
true is a corollary of this.

**At risk.**
- The paper's central object `A_intr` is not defined in the abstract. The theorem is only as
  strong as that definition, and the definition has to be pinned in the new paper with a
  formula, not a description.
- "Strict interlacing" for a *rank-one modification with positive weights* is Cauchy
  interlacing plus a sign condition — true and classical, but the hypotheses (positive
  weights, simple spectrum of the diagonal part) must be explicit, since the *weak*
  interlacing is all that holds without them.
- The Koszul–Vinberg claims are delicate (the characteristic function, the cubic form as
  connection data, the geodesic formula). They need either a worked example verified
  numerically or demotion. `[T]` only where checked.

**Verdict.** The best paper in the corpus. The new paper should *contain* its main theorem
(eigenframe/eigenvalue splitting, interlacing, boundary-only defectiveness) in corrected and
self-contained form.

---

## 5. The Three-Body Problem, Operator-First (24 Aug 2026, v3 · 25,496)

**Thesis.** On the equal-mass planar shape sphere `S²`, the Gram operator of the differential
of the map from shape to the three mutual distances has exact spectrum
`σ_min = cos²ϑ`, `σ_max = 1`, independent of longitude. Two kinds of degeneracy are
qualitatively different: at syzygy the operator loses rank while its gap is *maximal*; at the
equilateral configuration it stays invertible while the gap *closes*, quadratically, with
trivial `+1` holonomy and integer line-field index, the global obstruction being the Euler
characteristic of the sphere rather than a Berry phase. The shape sphere read as a
birefringent medium (uniaxial for equal masses, biaxial when the mass symmetry breaks, with a
genuine conical intersection and `−1` holonomy). Along the figure-eight choreography the
metric layer collapses at the six syzygy crossings while a contour count and a shifted
trace-log record stay numerically invariant — provided the branch condition (log analytic on
and inside the contour) is imposed as part of the construction. Rigidity `R = σ_min^{-2} =
sec⁴ϑ`. Rank `dΦ = N−2` for collinear `N`-body configurations, checked for `N = 3..8`.
Transient amplification along the figure-eight not captured by linear stability eigenvalues.

**Load-bearing.** The *dichotomy* — rank drop with maximal gap, versus gap closing with full
rank — is correct, and it is the cleanest structural statement in the corpus. The
collinear rank formula `N−2` is checkable and is the seed of the new capacity sum rule.

**Found by this review (see `01_REVIEW.md` §R5).** The exact spectrum as stated does **not**
reproduce. With the Kendall round metric on the shape sphere and Euclidean mutual distances,
the two squared singular values satisfy `σ₁² + σ₂² = 3` **identically**; `σ_max²` ranges over
`[1.5, 3]`, so no constant rescaling can give `σ_max = 1`. What is exactly true is the
*sum rule*, and the two degenerate loci (rank drop exactly on the collinear equator, maximum
`det M = 9/4` exactly at the two equilateral shapes, quadratic gap closing). The rigidity law
`R = sec⁴ϑ` inherits the error.

**At risk.** Everything downstream of `σ_min = cos²ϑ`: the rigidity law, the "uniaxial/biaxial"
assignment of optic axes, and the numeric exponents. The qualitative reading (two sheets, an
optic axis where they meet, a conical intersection when the masses differ) is likely to
survive with corrected numbers, but it has to be recomputed.

**Verdict.** Needs repair at its centre, but the repair is *better* than the original: a
conserved total is a stronger statement than a coordinate formula. This is the new paper's
worked example.

---

## 6. Five-Dimensional Non-Normal Stability Operator … Zero-Precursor Filamentary Fractures (25 Sep 2026, v3 · 18,248)

**Thesis.** A minimal 5-dimensional operator from shape/shear/interface sectors, with a
localised gradient-driven coupling that produces non-normality with a stable point spectrum;
a minimality result under three sector hypotheses; resolvent estimates putting the
pseudospectral radius of the defective `2×2` interface subsystem at `√(ε·coupling)` to
leading order; the exact transient envelope of an interface Jordan block with the threshold
"transient growth iff coupling/decay > 2", with peak time and peak gain; invariant-subspace
lifting to the full operator; a Dunford–Taylor/Riesz lift to the Grassmannian giving a
transport-metric + Berry-curvature decomposition; a square-root law for conical rank
collapse; a zeta-regularised log-determinant ledger whose leading heat-trace coefficient
matches Laplace–Beltrami under a stated lower-order hypothesis; a linearised Navier–Stokes
realisation with the interface coupling identified as background vorticity.

**Load-bearing.** The finite-dimensional core is correct and testable: a `2×2` Jordan block's
exact transient envelope, its `√ε` pseudospectral radius, and the lifting argument are all
standard-but-worth-writing-down, and the "coupling/decay > 2" threshold is clean algebra.
**This paper is the best template in the corpus for how to make a non-normal claim
falsifiable**: three stated observational tests, and the astrophysical reading explicitly
demoted to "possible effective description … not an established explanation".

**At risk.** The heat-trace/log-det correspondence is the weakest link: it needs the
lower-order hypothesis (stated, to the author's credit) and even then the identification is
a modelling statement, not a spectral one. The continuum lift (`[H]`).

**Verdict.** Keep, as the "non-normal, finite-dimensional, honestly bounded" companion. Its
transient-envelope lemma belongs in the new paper's gap-hierarchy section as the example of
what a *defective* cluster does to a bound.

---

## 7. What Transport Keeps (6 Sep 2026, v1 · 4,128)

**Thesis.** "Subspaces Before Space", with the Ramanujan Challenge's exact proofs as an
arithmetic calibration: a Gram-matrix selection criterion; the possible outcomes of tied
modal growth; conserved dual pairings with a finite readout-error bound; an independent
reproduction of the official Catalan initial-data cancellation; a reconstruction of the
two-parameter conservative matrix field with exact plaquette identity, determinant
factorisation and an algebraic eigenline-curvature certificate; band-resolved curvature
asymptotics (outer bands `n⁻²` with leading coefficients `±5√2/16`, middle band `n⁻³` with
`9/8`); a kernel-and-output criterion for numerator selection; seven CMF trajectories
(84 certified samples) against primitive-integer denominator growth; rank-one stress
composition; an exact projective-direction capacity census; fixed-spectrum optical response;
interior–exterior boundary elimination; Catalan's weighted rail integral with a controlled
remainder.

**Load-bearing.** The asymptotics are sharp, finite, and checkable — the kind of result that
can be *wrong* and therefore means something. The "capacity census" is the ancestor of the
new paper's capacity sum rule. The dual-pairing conservation is the arithmetic shadow of the
same phenomenon the new paper proves geometrically.

**At risk.** Density. Ten independent threads in one paper means no thread gets the space to
be *checked*. Also: "conserved dual pairing" and "projective-direction capacity" are named
before they are defined, and the definitions arrive late.

**Verdict.** Keep — but split. The new paper takes the *conservation* theme and one exact
capacity statement; the arithmetic certification stays where it belongs.

---

## 8. Foundational Operator Field Theory on Stratified Manifolds (9 Aug 2026, v4 · 36,359)

**Thesis.** Spacetime geometry as a downstream representation of non-normal transport on
stratified configuration spaces; the vacuum as an isotropic operator equilibrium
`K₀ = −ΛI`; a finite-rank projection governed by Bekenstein–Hawking entropy bounds,
`N ~ (M_p·R_universe)²`, putting the master operator in the trace-class/Fredholm-determinant
domain; a "derived" `Λ ~ 10⁻¹²² M_p⁴`; a Frobenius spectral-stress gradient flow
`dK/dt = −2[…]`; a "Total Spectral Reflection Theorem" with scale-invariant universality
mapping cosmic supervoids onto 2D topological-insulator edge transport.

**Load-bearing.** The *architecture* — operator first, geometry downstream, background
independence as a design constraint — is the program's founding move. That is worth stating
once, in the introduction of the new paper, as a stance (`[H]`), in two paragraphs.

**At risk — the most exposed paper in the corpus.**
1. **The Λ claim is circular as presented.** `N` is *chosen* by the Bekenstein–Hawking bound
   so that the sum converges; `Λ` is then read out of the regularised sum. The order of
   magnitude is an input (through `N` and the cutoff), not an output. Either prove that the
   scheme is insensitive to `N` (a stability theorem), or grade the whole thing `[H]` and
   stop calling it a derivation.
2. **"Total Spectral Reflection Theorem"** is a statement about a modelled interface with a
   prescribed contrast. "Scale-invariant universality" is a mapping between two *models*.
   Both are legitimate; neither is a theorem about supervoids.
3. **The abstract contains a malformed formula**: `dK/dt = -2[(K, K†, K†)` — an unclosed
   expression with a stray cross. Whatever the intended flow is, the abstract as archived is
   not self-consistent. This is a copy-editing failure of the kind that makes a reader
   distrust the rest, and it is fixable.

**Verdict.** Retire or repair. Do not build on it. The new paper should say, in one
paragraph, *why* the program does not need a cosmological claim to be interesting — the
conservation theorem and the exact shape-sphere geometry are stronger evidence for the
program than a numerological coincidence could be.

---

## 9. Spectral Stability Across Obstruction Interfaces (24 Jun 2026, v2 · 7,610)

**Thesis.** `H_N(ε) = A + D₀ + εE` on `N` copies of `ℝ²`; `A` symmetric from centred finite
differences with the symplectic `J`, `D₀` a diagonal multiplication operator of
position-dependent Hessians, `εE` a controlled non-normal perturbation. `[H_N,H_Nᵀ]` scales
linearly in `ε` and is spatially localised where the Hessian gradient is largest. Bounds on
the `ε`-pseudospectrum with vertical bulges of height `O(√ε)`; resolvent estimates via the
Kreiss matrix theorem; interface stability via Schur complements; a regularised trace-log via
Dunford calculus; numerics to `N = 128`.

**Load-bearing.** The cleanest *realisation* in the corpus: a concrete, computable family in
which every abstract object has a matrix. The `O(√ε)` bulge and the Schur-complement gluing
are true and elementary. The `N = 128` experiments are a genuine gate.

**At risk.** "Effective inertia tensors" is underdefined (it is the Schur complement; say so).
The continuum-limit statement is `[H]`. The title promises "gluing dynamics"; the content is
static Schur complements.

**Verdict.** Keep as the lattice realisation, folded into the new paper's numeric gates.

---

## 10. The Price of a Direction (13 Aug 2026, v1 · 19 pp, CC BY 4.0)

**Thesis.** A direction is not free: carrying it as a resolvable channel through a region
costs one unit of that region's boundary-trackable census. Five computational gates, listed
in full, writing machine-readable output that the figures read directly.
`[T]` the angle–channel dictionary: two directions at angle `θ` are distinct trackable
channels at threshold `ε` iff `sin²θ ≥ ε`, so resolving `δ`-separated directions requires
census depth `2log(1/sin δ)`, and `μ` simultaneous directions require `μ` channels rather
than `log μ` bits. `[T]` a finite-cutoff dimension deficit `n − d ≤ log C₀/log(1/a)` with
`C₀` calibrated to absorb the tube-counting normalisation. `[V]` aperture prediction
`πR/w = 12.57` against a measured effective-rank plateau of 13; cell prediction `2k̄r = 8.17`
against a measured 8, flat across seven orders of magnitude of threshold. `[V]` overflow:
forty threaded directions coarse-grain to the capacity's worth of channels. `[V]` the
interior wall (crowding concentrates the wall's spectral stress; the crossing's share rises
from 7% to 60%). `[V]` a ratio-gate onset with fitted exponent `0.15` against 1 for a
product gate. `[C]` Wang–Zahl (Kakeya sets in `ℝ³` have Hausdorff and Minkowski dimension 3)
used once, as an input for support sets satisfying the classical straight-segment hypotheses.
`[H]` universality of the geometric capacity law; the concentration alternative; dimensional
extension of the census coefficient.

**Load-bearing.** This is the corpus's **methodological high point** and the only paper whose
abstract contains a genuine, checkable, non-trivial little theorem (the `sin²θ ≥ ε`
dictionary) *and* a full statement of what is conjectural. The "price of a direction" is the
most quotable idea in the ten.

**At risk.** `C₀` is fitted ("calibrated to absorb the tube-counting normalisation"), so the
dimension-deficit bound is *not* an a priori theorem; the paper says this and must keep
saying it, because a reader will otherwise take a bound with a fitted constant as a Kakeya
theorem. The measured capacities (`13` vs `12.57`, `8` vs `8.17`) are *agreements to within
one unit* of formulas that contain a fitted normalisation — that is consistency, not
prediction.

**Verdict.** Keep as the second pillar. Its honest-conjecture section is the model for the
new paper's "what would refute this".

---

## Dependency map

```
                    (8) operator-field stance  [H, background]
                                    |
                        (1) projector algebra  [T, Lean]  <---- (9) lattice realisation [T/V]
                          /            |            \
             (3) redistribution    (10) angle–     (7) conserved pairings
              + protocol [T/C]      channel [T]      + CMF asymptotics [V]
                    |                  |
                    |            capacity census  <---- (5) three-body spectrum [T, needs repair]
                    |                  |                        |
                    |            (NEW) capacity sum rule <------+
                    |                  |
              (4) square case [T] ---> (2) four-body 5D
                    |
              (6) non-normal 5D transient envelope [T]
```

Two arrows are the ones the corpus does not currently draw:
* (4) → (2): the square-case theorem **is** the proof of the four-body paper's central claim.
* (5) → (NEW): the conserved total replaces the per-shape spectral formula, and it survives.

## What is *not* in the corpus

No paper states a conservation law for transport capacity. No paper states the gap hierarchy
as an inequality with a constant. No paper proves the refraction law from a variational
principle. No paper states what would refute its central claim, except paper 10. Those four
gaps are the new paper.

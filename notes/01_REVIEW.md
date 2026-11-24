# Review — what the corpus is actually claiming, and what survives

Companion to `00_INVENTORY.md`. Findings are numbered `R…`; the gate that produces each
number is named so the number can be re-derived rather than believed.

---

## The one idea, stripped of vocabulary

Ten abstracts, one structure. Every paper in the corpus studies the same object:

> **a family of subspaces carried along a path, together with the gap that decides what can
> be resolved at the end of the path.**

Everything else is a consequence of where that gap is placed:

| where the gap sits | what the papers call it | papers |
| :-- | :-- | :-- |
| in the spectrum | Riesz projector, spectral cluster, exceptional point | 1, 3, 4, 5, 6 |
| between two subspaces | principal angle, persistence, capacity | 1, 10 |
| in the pseudospectrum | non-normality, transient growth, Kreiss bound | 6, 9 |
| at an interface | refraction, gluing, Schur complement | 2, 6, 9 |
| in the readout | numerator selection, kernel-and-output criterion | 7 |

That is a coherent research programme, and it is *not* what the abstracts say. The abstracts
say "emergent metric", "reflective closure", "hierarchy principle", "universal geometry",
"total spectral reflection". Those are names for a programme. A paper is better than its
programme only when it states one inequality and proves it.

**This is the first editorial decision for the new paper: one thesis, and the thesis is the
gap.** Everything that cannot be derived from the gap statement moves into a graded
section or out.

---

## What to keep (do not lose these in the rewrite)

**P1. The five-grade ledger, with the weakest link named.** `[T]/[V]/[C]/[D]/[H]` and
"where a chain mixes grades, the weakest link is named" (paper 3) is the best thing in the
corpus. It is unusual, it is honest, and it makes the work auditable by a stranger. Keep it
verbatim as the paper's first convention.

**P2. Self-containment by appendix.** Paper 10 restates every imported companion result
*with proof* in Appendix B, so that "companion citations are context, never dependencies."
That is the correct editorial answer to a ten-paper series, and it is the reason paper 10 is
readable on its own. The new paper must do the same.

**P3. Gates that write machine-readable output, which the figures read.** Paper 10 again.
A figure that reads a gate's JSON cannot drift away from the number in the text. This
repository now does the same (`scripts/gates/`, `results/gates/*.json`).

**P4. The false-control discipline.** `FalseControls/` contains three statements that are
deliberately false; the verification fails unless the kernel *rejects* them, and rejects them
for a mathematical reason rather than a typo. A checker that accepts everything passes an
axiom audit. This is the right way to show the kernel can say no, and almost nobody does it.

**P5. Recording a correction instead of erasing it.** Paper 4 keeps the corrected prediction
about coincident boundary pins in the verification record. Keep that habit: the new paper's
gate `g01` records a correction of paper 5's central formula, with the number that refutes it.

---

## R1. Vocabulary outruns theorem

**Symptom.** Named principles that carry no inequality:

| name | paper | what is actually proved |
| :-- | :-- | :-- |
| Hierarchy Principle of Structural Persistence | 1 | nothing; the finite identities are separate |
| Reflective Closure of Transport | 2 | the projection-defect algebra (paper 1, Lemma 6) |
| Total Spectral Reflection Theorem | 8 | a statement about a modelled interface with prescribed contrast |
| Universal Projector Geometry | 3 | the covariance→projector map and `F(Ω,Π)` |
| birefringent shape manifold | 5 | a two-sheet singular-value structure |

**Repair.** In the new paper each named structure must appear either as (i) a theorem with a
constant, (ii) a definition, or (iii) an `[H]` in the hypothesis section. No fourth option.
Concretely: the "hierarchy principle" becomes Theorem 4–6 with explicit Lipschitz constants
(and is *corrected* on the way — see R2).

## R2. The hierarchy principle is false at its first level

**Claim (paper 1, and the framing of papers 3 and 5).** Fragile descriptors such as
individual eigenvectors are replaced by more stable invariants: Riesz projector bundles,
Grassmannian continuation, global spectral invariants.

**Why it fails as stated.** For a *simple* isolated eigenvalue the rank-one Riesz projector
is, up to a phase, the eigenvector: `P = vv*` and `‖Ṗ‖_F = ‖v̇⊥‖`. A rank-one projector
therefore inherits exactly the eigenvector's instability — it is not a more stable object at
the same level. Anyone who tries to "stabilise" by passing to the rank-one projector gets
nothing. The stability gain appears at a *different* place: a projector over a **cluster**
is protected by the gap that separates the cluster from the rest, so it survives the closure
of gaps *inside* the cluster — which is precisely where eigenvectors diverge.

**The repair is the paper.** The hierarchy is not ordered by "how derived" an object is; it
is ordered by **the gap that protects it**:

| level | invariant | protected by | failure mode |
| :-- | :-- | :-- | :-- |
| 0 | eigenvalue | nothing (Weyl: Lipschitz in `‖Ȧ‖`) | crossing changes labels |
| 1 | eigenvector / rank-one projector | internal gap `γ_int` | diverges like `γ_int^{-1}`; `\|t\|^{1/2}` at an EP |
| 2 | cluster projector | external gap `γ_ext` | analytic through interior degeneracies |
| 3 | trace, rank, index, spectral flow | external gap + integer | jumps only in integers |

Stated this way the principle is a theorem with constants (swarm directions D4–D6), and it
says something a reader can use: *choose the invariant whose protecting gap your experiment
actually controls*.

## R3. One symbol, three meanings

`C` is used for (i) transport capacity in paper 3, (ii) the persistence overlap
`Tr(Π₁Π₂)` in paper 1/3, (iii) the "boundary census" and its coefficient `C₀` in paper 10.
`R` is rigidity in paper 5 and a region/radius elsewhere. `Ω` is a structural operator in
paper 3 and a solid angle in paper 10. Since papers 1, 3 and 10 are the three most-cited of
the ten, the collision is not cosmetic.

**Repair.** A notation table in §2, one symbol per concept, and no symbol reused across
sections without a subscript. Names to fix now: capacity `𝒞`, persistence `π(Π₁,Π₂)`,
rigidity `ρ`, census `ν`, structural operator `Ω`, spectrum of the transport differential
`σ_i`, cone slope `κ`.

## R4. The refraction law is Snell's law in disguise, and that is fine — but say so

**Claim (papers 3, 5).** `R₁ sin²θ₁ = R₂ sin²θ₂` across a "rigidity interface".

**What is true.** If `R > 0` and one considers the conformal metric `ĝ = R·g`, then geodesics
of `ĝ` crossing a curve where `R` jumps satisfy Snell's law with refractive index `n = √R`;
the identity `R₁sin²θ₁ = R₂sin²θ₂` is exactly that statement. This is a theorem about
conformal metrics (swarm direction D9).

**What is not true.** That the identity is a *law of transport* for a physical system. It is
a consequence of a modelling choice: that admissible paths extremise `∫R sin²θ`. The
variational principle is `[H]`; the Snell identity is `[T]` *given* the principle. Paper 5's
`R = sec⁴ϑ` then makes the index `n = sec²ϑ`, which is a strong, falsifiable claim — worth
having, but it inherits R5.

## R5. RETRACTED — see `notes/07_TWO_MAPS.md`

**This finding was wrong.** Paper 5 differentiates the map to *squared* distances; the test below
differentiates the map to distances. Both statements are true of their own operator. The material
is kept unedited below as the audit trail; do not cite it.

**Claim.** On the equal-mass shape sphere, the Gram operator of the differential of the map
from shape to the three mutual distances has exact spectrum `σ_min = cos²ϑ`, `σ_max = 1`,
independent of longitude; hence rigidity `R = σ_min^{-2} = sec⁴ϑ`.

**Test.** Kendall metric on the shape sphere (round, radius 1/2), Euclidean mutual distances,
inertial size fixed so that `d₁₂²+d₁₃²+d₂₃² = 3`. Gate `g01_shape_spectrum.py`, 14 assertions.

**Result.** The *sum* is exact and the split is not:

$$\sigma_1^2+\sigma_2^2 = 3 \quad\text{identically (deviation } 2.2\times10^{-9}\text{)},$$

while `σ_max²` ranges over `[1.5, 3]`. No constant rescaling can make `σ_max = 1`; the
statement is not a normalisation convention, it is false as written. Two independent routes
agree: the `(α,ψ)` Hopf coordinates of the shape sphere, and a Cartesian chart checked
against it.

**What is true, and is stronger.**

| claim | value | how |
| :-- | :-- | :-- |
| sum rule | `σ₁²+σ₂² = 3` identically | gate (a) |
| collinear locus | `det M = 0` exactly on `ψ ∈ {0,π}` (rank drops to 1) | gate (b) |
| equilateral locus | `det M = 9/4`, the maximum over the whole sphere | gate (c) |
| splitting | `σ₁²−σ₂² = √(9−4det)` closes **linearly** with slope exactly 3 | gate (d) |
| isotropy | the same slope in every direction: an *isotropic* cone | gate (d) |
| holonomy | eigen-line holonomy around the equilateral shape is exactly `−1` | gate (e) |
| general `N` | `Σ_{i<j}\|∇d_ij\|² = N(N−2)`, independent of the configuration | gate (f) |

So paper 5's *dichotomy* survives — the operator loses rank exactly where its gap is largest,
and its gap closes exactly where it is invertible — but the numbers are replaced by a
conservation law, and the geometric reading changes: the equal-mass equilateral degeneracy is
a **genuine conical intersection with `−1` holonomy**, not a quadratic closing with `+1`
holonomy. The sentence "breaking the mass symmetry produces a genuine conical intersection
with linear gap closing and eigenvector holonomy −1" is therefore describing something that is
*already there* at equal masses. What mass-symmetry breaking plausibly does is *tilt the cone*
(anisotropic instead of isotropic), which maps onto the uniaxial/biaxial language far better
than a holonomy dichotomy does. That is a conjecture for the new paper, with a gate to settle
it.

**Why the repair is better.** A formula that depends on a chart can always be got wrong; a
conserved total cannot. `Σ|∇d_ij|² = N(N−2)` says the total capacity of the distance map is
fixed by the number of bodies alone, and the shape only decides how it is distributed. That is
the corpus's own slogan — "a transport can forget almost every direction and still retain a
constant" — as a theorem.

## R6. The Λ derivation is circular and should be retired

**Claim (paper 8).** `Λ ~ 10⁻¹²² M_p⁴` "derived" from a finite-rank truncation
`N ~ (M_p·R_universe)²` plus a trace-log identity.

**Why it is circular.** `N` is chosen so that the regularised sum is finite, and the order of
magnitude of `Λ` is then read out of that same regularised sum. The answer is an input
carried through the cutoff. A derivation would require a stability theorem: that the result
is insensitive to `N` over a range, and that the range is selected by something other than the
desired answer. No such theorem is present.

**Also.** The archived abstract contains a malformed formula (`dK/dt = -2[(K, K†, K†)`).
Whatever the intended flow, the published sentence is not parseable. For a corpus that
elsewhere audits its own axiom use, this is the wrong kind of inconsistency.

**Repair.** Grade the whole cosmological section `[H]`, state it as an *ansatz* for a vacuum
operator with a cutoff, and drop "Resolution of Cosmic Singularity and Vacuum Divergence" from
the title. The new paper does not need it: the conservation law and the exact shape-sphere
geometry are stronger evidence for the programme than a numerological agreement could be.

## R7. The edition is a moving target

`README.md` says the paper labels follow "the 29 June 2026 edition named in `PROVENANCE.md`"
and that "the version behind the DOI may number them differently". `CITATION.cff` cites
`10.5281/zenodo.21089303`, which "always opens the newest version". So the proof-of-record
points at a document that can change under it, and the theorem numbers in the README can
silently stop matching the paper.

**Repair, and it is cheap.** (i) Cite the *versioned* DOI in `CITATION.cff` and in the paper.
(ii) Add `paper/MANIFEST.md`: theorem label → Lean name → gate id, hashed. (iii) Keep the
concept DOI only as "latest version". A kernel-checked claim attached to a mutable document
is not a proof of record.

## R8. No falsification asymmetry — except paper 10

Nine of the ten abstracts say what the framework explains or predicts. One (paper 10) says
what would refute it, and one (paper 6) states three observational tests. Everything else is
unfalsifiable as written, not because the mathematics is weak but because no observation is
named that would count against it.

**Repair.** The new paper gets a section "What would prove this wrong", with at least one
test per claim class, and the tests must be *cheap* — a test that needs a new instrument is a
wish.

## R9. The corpus has one real dependency it does not draw

Paper 2 (four bodies, three dimensions) is exactly the square case `N = d+1`, so paper 4's
theorem — real spectrum in the regular interior, defectiveness only on `det G = 0` — *is* the
proof of paper 2's central structural claim ("the collinear horizon remains generically
semi-simple; defectiveness is confined to higher-codimension strata"). The two papers never
say so. Similarly paper 9's lattice is a realisation of paper 6's operator, and paper 10's
capacity census is a numerical shadow of the sum rule proved here.

**Repair.** The new paper states the dependency graph explicitly and marks each arrow `[T]`
(proved here) or `[C]` (imported).

---

## The four gaps the corpus leaves

1. **No conservation law.** Nothing in the corpus says what is *invariant* about transport
   capacity. Papers count channels, measure plateaus, fit coefficients — and never ask what
   the total is. `Σ|∇d_ij|² = N(N−2)` answers it for the distance map.
2. **No inequality for the hierarchy.** The hierarchy is a slogan; it needs constants.
3. **No derivation of refraction from a variational principle.** It is asserted across a
   "rigidity interface" and never varied.
4. **No statement of refutation.** Except paper 10.

Those four gaps are the new paper's four sections, in that order.

---

## Verdict

The corpus is one good idea with ten coats, one kernel-checked core, two genuinely strong
mathematical papers (4 and 10), one honest and useful correction record, and one claim
(paper 8's Λ) that should be withdrawn. Its weakness is not the mathematics — it is that the
vocabulary promises more than the theorems deliver, so a reader cannot tell which sentence is
load-bearing.

That is fixable in a single paper, and fixing it is worth more than an eleventh coat.

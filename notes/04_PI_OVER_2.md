# The π/2 constant: resolved

**Resolution (later the same day).** The question was not a proof problem; it was a
normalization problem, and it had three answers, not one:

1. **Finite pairs.** `‖P − P'‖ ≤ δ/(γ − δ)`, where γ is the gap of A and δ = ‖A − A'‖ < γ/2.
   The denominator is the *union* gap; claiming `δ/γ` with constant 1 is false, and a targeted
   search reaches `‖P − P'‖ = 0.3735` against `δ = 0.3465`. Recorded in gate
   `g04_projector_constant` (f).
2. **Infinitesimal.** `‖Ṗ‖ ≤ ‖Ȧ‖/γ` with constant 1, sharp (the rotating family attains it).
   This is the form the paper uses, and the only one in which "constant 1" is true.
3. **Angle.** `Θ ≤ arcsin(δ/(γ − δ))`, which increases to `π/2` at the edge of the stable range
   `δ → γ/2`. So `π/2` is exactly the endpoint constant of the angle bound — which is where it
   belongs, and not in the projector estimate.

The lesson is the one the note below opens with, and I had to learn it by getting the statement
wrong twice: the constant is meaningless until the norm, the gap and the finite/infinitesimal
alternative are pinned.

**Second resolution (zbMATH route, later the same day).** Settled, with one part still open:
* the angle form is documented: Albeverio and Motovilov (Complex Anal. Oper. Theory 7 (2013)
  1389--1416; arXiv:1112.0149; Zbl 1288.47006) bound `arcsin‖P-Q‖ <= M(‖V‖/d)` for `‖V‖ < d/2`
  and show the acute-angle case is guaranteed only for `‖V‖ < 0.454169... d`. That threshold
  below `d/2` is precisely the statement that the angle reaches `pi/2` inside the stable range,
  which is Theorem 5.2(c) in this paper's normalisation. The `pi/2` is therefore sourced as an
  angle constant, not a norm constant.
* the attribution TO KATO is not verified, and is now dropped from the paper. zbMATH's review of
  Kato's book (Zbl 0148.12601, H. Baumgaertel) summarises Chapter II as finite-dimensional
  analytic perturbation theory --- eigenprojector series, reduction for semisimple eigenvalues,
  convergence radii --- without naming a constant, and Chapter II section 4 could not be read.
  Dropped for want of evidence, not as a disagreement.

The original sketch is kept below, unedited, because it records the reasoning that led to the
question and because its first section is what made the resolution possible.

---

Status: **superseded sketch, kept for the record**. §5.2 of the paper states two constants — `1/γ` for an ordered
(cluster at an end of the spectrum) and `π/2γ` in general — and grades them `[C]`. This note
sets out what a proof would have to contain, so that the gap is a research problem rather than
a blank.

## First: the statement has to be pinned, because the constant depends on it

"Cato's constant is π/2" is not a theorem until four choices are made, and different choices
give different numbers:

1. **Which norm** — operator, Frobenius, or the angle `Θ` itself (`sin Θ = ‖P − P'‖`)?
   In Frobenius the rank-one case is exactly `√2 ‖v̇⊥‖` (paper Thm 5.3), so a constant quoted
   for "the projector" is a constant for one norm only.
2. **Which inequality** — `‖P − P'‖ ≤ c ‖A − A'‖/γ` (a *perturbation* bound) or
   `‖Ṗ‖ ≤ c ‖Ȧ‖/γ` (a *derivative* bound)? The second follows from the first by a difference
   quotient, with the same `c`, but only if the bound is uniform over the path.
3. **Which gap** — two-sided (`dist(σ, σ') ≥ γ`) or one-sided/ordered
   (`max σ + γ ≤ min σ'`)? This is exactly the difference between the two constants in the
   paper: `1` for ordered (Davis–Kahan), `π/2` for two-sided.
4. **Which perturbations** — bounded self-adjoint only, or a general closed operator with a
   resolvent condition? Kato's theory covers far more than the finite-dimensional case, and a
   constant proved in the general theory is a different statement from one proved in `M_n(ℂ)`.

The paper's §5.2 fixes (1) operator norm, (2) derivative bound via the perturbation bound,
(3) both gaps, (4) finite-dimensional bounded. The second task is to *check* that `π/2` is
what the literature gives under exactly these four choices, rather than importing a constant
from a neighbouring statement. My own search did not settle this: the queries returned
unrelated material, and I did not read Kato's Chapter II §4 directly. **This is the first open
item, and it is bookkeeping, not mathematics** — a library visit, not a proof.

## What the proof has to do, in four steps

**Step 1 (reduce to a 2×2 model).** Split `H = M ⊕ M^⊥` with `M = ran P`. The perturbation
`E = A' − A` becomes a 2×2 block operator, and `P'` is the graph of an operator `X: M → M^⊥`
satisfying a Riccati equation. The estimate reduces to a bound on `‖X‖` in terms of
`‖E‖/γ`. The classical reduction (Kato; also the "angular operator" of Davis–Kahan) shows the
worst case has `X` of rank one, so **the problem is scalar** and dimension-free. This step is
elementary but must be written out, because it is where the two-sided gap enters: a two-sided
gap means `X` may be of either sign, which is precisely what destroys the constant `1`.

**Step 2 (the scalar core).** For the 2×2 family `A(t) = [[a(t), b(t)],[b(t), −a(t)]]` with
spectral gap `γ = 2√(a² + b²) ≥ γ₀`, the eigenline angle `θ` satisfies
`sin(2θ) = b/√(a²+b²)`, and one needs the sharp bound
```
|θ̇|  ≤  c · |(ȧ, ḃ)| / γ₀ .
```
A direct computation gives `θ̇ = (a ḃ − b ȧ)/(2(a² + b²))`, so the sharp constant is the norm
of the linear functional `(ȧ, ḃ) ↦ (a ḃ − b ȧ)/(2(a²+b²))` on the tangent space — which is
`1/(2√(a²+b²)) = 1/γ`, **constant 1**, for a single 2×2 family. So the π/2 cannot come from
the scalar core alone: it must come from Step 3. Any proof that claims π/2 must show where
the extra factor appears, and this computation is the check that it is not being smuggled in.

**Step 3 (where π/2 actually enters).** The factor `π/2` is the `L¹` norm of a kernel: it is
`∫₀^∞ (sin x)/x dx`. It appears when the bound is proved by *integrating the derivative bound
along the path* and then optimising over paths, i.e. when the two-sidedness of the gap forces
the angle to travel through a quarter turn. Concretely, one expects the sharp statement to be
of the form
```
‖P − P'‖  ≤  sin( (π/2) · ‖E‖/γ )        (two-sided)
```
whose linearisation is the π/2 bound and whose saturation at `‖E‖/γ = 1` is a quarter-turn.
Proving this needs: (i) the scalar identity of Step 2 for the *infinitesimal* angle,
(ii) an argument that the extremal path is the one that turns the angle monotonically, and
(iii) the evaluation of the resulting one-dimensional integral, which is where `π/2` is born.
The Fourier/Hilbert-transform form of the same computation (which is how the swarm member
phrased it) is the operator-valued version of the same identity.

**Step 4 (sharpness).** Exhibit a family with ratio tending to `π/2`. The natural candidate is
a Toeplitz (Jordan-block-like) family of growing dimension; the swarm check
`results/swarm/check_D4_m5.py` reaches `1.5618` at `N = 129`, i.e. `0.6%` below `π/2` and
rising. That is *consistent* with `π/2` and proves nothing; the sharpness proof needs an
explicit asymptotic computation, not a trend.

## What would make the π/2 claim unnecessary

There is a cheaper route, and it is the one I would take if the goal is a correct paper rather
than a complete one: **state the ordered case only** (`1/γ`, Davis–Kahan, with a proof by
contour integration that gives `2/γ` and a sharper argument that gives `1/γ`), and quote the
two-sided constant as `[C]` with its source pinned. The paper's §5 argument does not need the
sharp two-sided constant: the hierarchy table's content is that *clusters are protected by the
external gap and rank-one projectors are not protected at all*, and both survive with the
non-sharp `2/γ`. The π/2 is a refinement of a constant, not of the structure.

## Concrete next actions, in order of cost

1. Read Kato, *Perturbation Theory for Linear Operators*, Ch. II §4 (and the Karow–Kressner
   perturbation-bound paper found in the literature search) and record, with page numbers,
   the exact hypotheses under which `π/2` is stated. **One hour.** This is the only step that
   is bookkeeping, and it should be done before anything else, because everything downstream
   depends on which statement is being sharpened.
2. Write Step 1 (the angular-operator reduction) for finite-dimensional `A`. **Half a day**,
   and it is a good exercise for the paper's appendix regardless of the constant.
3. Compute the exact sharp constant for the two-level *path* problem numerically (maximise
   `|θ̇|/(|(ȧ,ḃ)|/γ)` over a box of paths) to see whether it is `1` or larger; if it is `1`,
   the π/2 story is about something else (probably the *angle* rather than the derivative) and
   the paper's statement needs rewording.
4. Only then attempt the integral evaluation of Step 3.

Until step 3 is done I would not put `π/2` in a theorem statement with a `[T]` grade, which is
why the paper does not.

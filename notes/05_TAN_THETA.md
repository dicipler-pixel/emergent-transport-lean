# The sharpened angle bound, and what proving it would take

Question: does Motovilov–Selin (2006) sharpen the angle bound past `pi/2`, and what would a
proof cost?

## What their paper says

A. K. Motovilov and A. V. Selin, *Some sharp norm estimates in the subspace perturbation
problem*, Integral Equations Oper. Theory **56** (2006) 511–542; arXiv:math/0409558;
Zbl 1121.47007. Their Theorem 2 (read from the arXiv v2 typesetting, eqs. (1.13)–(1.14)):

> Let `spec(A) = σ− ∪ σ+` with `d = dist(σ−,σ+) > 0`, suppose the convex hull of `σ−` does not
> meet `σ+`, let `V` be **off-diagonal** with respect to `H = Ran E_A(σ−) ⊕ Ran E_A(σ+)`, and
> suppose `‖V‖ < d`. Then
> `‖E_L(σ′−) − E_A(σ−)‖ ≤ sin( arctan( ‖V‖ / √(d² + ‖V‖²) ) )`,
> equivalently `‖tan Θ‖ ≤ ‖V‖/d`, where `Θ` is the operator angle between the two subspaces.

So the answer is **yes, and by a lot**. With `δ = ‖V‖` and `d` the set distance:

| class | sharp angle bound | value at `δ = γ/2` |
| :-- | :-- | :-- |
| all self-adjoint `V` (this paper, Thm 5.2(c)) | `Θ ≤ arcsin(δ/(γ−δ))` | `π/2 = 90°` |
| off-diagonal `V`, convex-hull separation | `Θ ≤ arctan(δ/d)` | `arctan(1/2) = 26.6°` |

The two are sharp in *different classes*, so neither replaces the other: `π/2` is the endpoint of
the unrestricted angle envelope, and `arctan` is the envelope once diagonality is excluded. That
is now Remark 5.4 of the paper, with both constants recorded and the class named as the
hypothesis a reader must check.

## What proving it would take

Four steps, in increasing cost. Steps 1 and 4 are afternoons; step 3 is the paper.

**Step 1 (block reduction, finite-dimensional).** Write `H = M ⊕ M⊥` with `M = Ran P`. For
off-diagonal `V` the perturbed operator is the block matrix `[[A_+, V],[V*, A_−]]` with `A_±` the
compressions. Its invariant subspace graph is `{(x, Xx)}` with `X: M → M⊥` solving the Riccati
equation `A_−X − XA_+ = X V X − V*`. Then `tan Θ = ‖X‖`. This is elementary in finite dimensions
and should be written out; it is also the step that shows *why* off-diagonality is essential —
for a general `V` the diagonal blocks shift, `X` no longer solves a quadratic with the same
structure, and the argument degrades to the `sin` bound.

**Step 2 (the Riccati a priori bound).** From the Riccati equation, `‖X‖ ≤ ‖V‖/d` follows if
`A_±` have separated spectra and the numerical range of `V` is controlled. In finite dimensions
this can be done by a fixed-point/contraction argument on the ball `‖X‖ ≤ ‖V‖/d`, or by the
"direct rotation" construction: the direct rotation `U` from `M` to `N` has `tan Θ = ‖(1−P)UP‖`,
and the off-diagonal hypothesis makes `U` explicit. Either route is a half-day.

**Step 3 (the convex-hull hypothesis).** This is the substantive part and it is where I would
expect the work. The convex-hull condition is what makes the *numerical range* of the two
diagonal blocks lie in disjoint half-planes, which is what allows `d` (the set distance) to
appear rather than the larger "gap of the union". Proving the sharp constant requires an
estimate on `(A_− − z)^{-1}` uniform in the half-plane, i.e. a numerical-range (accretivity)
estimate, and then the sharpness example showing the constant cannot be improved. The
Kostrykin–Makarov–Motovilov papers (Int. Eq. Op. Th. 51 (2005) 121–140, and the `tan 2Θ`
generalisation, OT: Adv. Appl. 149 (2004) 349–372) contain that machinery; a proof here would
either reproduce it in finite dimensions or cite it and verify the hypotheses.

**Step 4 — DONE.** Gate `g05_tan_theta` (4 assertions, `results/gates/g05_tan_theta.json`):
the bound holds over 300 random off-diagonal perturbations of interval clusters (worst ratio
0.987), is approached in the 2x2 model as `delta/d -> 0` (0.99999999), and **fails by a factor
1.122** once a diagonal part is admitted at `delta/d = 0.318` — so the off-diagonality is
load-bearing, not decoration. The remark is now graded `[C]/[V]`; Motovilov–Selin's own sharpness
argument is still not reproduced, which is what step 3 would supply.

The original plan for step 4: Unlike the earlier constants, this one
can be *tested* without proving it: generate random finite-dimensional `A` with a convex-hull
separated spectrum, random off-diagonal `V` with `‖V‖ < d`, and check
`‖tan Θ‖ ≤ ‖V‖/d` — with a matching search for near-equality. That is a gate of about forty
lines, and it would let the paper state the off-diagonal bound as `[V]` with the citation rather
than as `[C]` alone. **This is what I would do next**, not step 3: it is cheap, it is decisive
about whether the constant is right as transcribed, and it does not require reproducing a
200-page literature.

## What this does *not* settle

The threshold `c = 0.454169…` of Albeverio–Motovilov (2013) for the acute-angle case is *below*
`1/2`, so the unrestricted class really does reach `π/2` before the count can change — that part
is consistent and now double-sourced. What remains open is the *sharp* envelope in the
off-diagonal class when the convex-hull hypothesis fails: neither paper covers it, and it is
where the two regimes meet. It is listed as O2 in the paper.

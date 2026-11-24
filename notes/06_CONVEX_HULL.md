# Step 3: the convex-hull argument, reproduced in finite dimensions

**Answer to "is it really a week?"** No for rank one — that took about an hour, and it is now
Theorem 5.4 of the paper, proved and gated. Yes for rank $k\ge2$, and the week is not padding:
the rank-one argument is a two-dimensional computation, and the step to rank $k$ is where the
whole Riccati / direct-rotation machinery sits.

## What is proved (rank one, line-separated)

Theorem 5.4. $A$ self-adjoint, $a$ a simple eigenvalue with unit eigenvector $u$, all other
eigenvalues at distance $\ge d$ *above* $a$; $V$ self-adjoint and off-diagonal w.r.t.
$\operatorname{span}u\oplus u^\perp$, $\delta=\|V\|$. Then, with $\Theta$ the angle between
$\operatorname{span}u$ and the perturbed eigenvector,

  `|tan 2Θ| ≤ 2δ/d`,  hence  `tan Θ ≤ (sqrt(d²+4δ²) − d)/(2δ) < δ/d`.

Both sharp: the $2\times2$ model $A=\operatorname{diag}(a+d,a)$, $V=\delta\sigma_1$ gives
`tan Θ = δ/(d/2 + sqrt(d²/4 + δ²))` and `|tan 2Θ| = 2δ/d` *exactly*, for every $\delta<d/2$.

The proof is six lines. Write $\nu=\cos\Theta\,u+\sin\Theta\,w$; the eigenvalue equation has
exactly two scalar consequences,
`(λ−a)cosΘ = μ sinΘ` and `(λ−b)sinΘ = μ cosΘ`, with $b=\langle Aw,w\rangle$, $\mu=\langle u,Vw\rangle$.
Divide and subtract: `b − a = μ(tanΘ − cotΘ) = −2μ/tan 2Θ`, so `|tan 2Θ| = 2|μ|/|b−a|`. Then
`|μ| ≤ δ` and `b − a ≥ d`. QED.

**A finding worth keeping:** this is *stronger* than the Motovilov–Selin bound $\tan\Theta\le\delta/d$
that motivated step 3 — for every $\delta>0$ the $\tan 2\Theta$ bound implies a strictly better
estimate on $\tan\Theta$. At rank one with line separation, $\tan 2\Theta\le2\delta/d$ is the sharp
constant, not $\tan\Theta\le\delta/d$.

## Where the hypothesis enters, identified

The key step is `b − a ≥ d`, and $b=\langle Aw,w\rangle$ is a point of the *numerical range* of the
compression $A|_{u^\perp}$, which fills the convex hull of the rest of the spectrum. So:

* **line separation** (rest entirely above $a$) ⟹ $b-a\ge d$ for every $w$ ⟹ the bound holds;
* **convex hull straddling $a$** ⟹ $b$ can sit at $a$ ⟹ the bound fails. Gate
  `g06_projector_tan2(d)` exhibits a violation by a factor **1.21** at $\delta/d=0.446$.

That is precisely what the convex-hull hypothesis in the literature is for, and the rank-one
computation makes the mechanism visible: it is not bookkeeping, it is the difference between the
numerical range meeting $a$ or missing it.

## What rank $k$ still costs (the actual week)

For rank $k\ge2$, $\Theta$ is an operator angle and the scalar pair of equations does not close:
one gets a 2-dimensional reduction for *each* eigenvector of the perturbed cluster, with its own
$b$ and $\mu$, but assembling these into a bound on $\|X\|$ for the angular operator $X$ needs the
Riccati equation $A_+X-XA_-=XBX-B^*$ and an a priori estimate on $\|X\|$ that the elementary
trace argument does not give (I tried the trace route: it yields a quadratic condition
$w\|X\|_F^2-d\|X\|_F+w\ge0$ that carries no information when $w<d/2$). What is needed, in order:

1. existence of a bounded solution $X$ of the Riccati equation with $\|X\|\le\delta/d$, by a
   contraction on the ball (needs the numerical-range estimate uniform in the half-plane);
2. the direct-rotation construction $U$ with $\tan\Theta=\|(1-P)UP\|$, and the identification of
   $U$ from $X$;
3. the convex-hull hypothesis used as in step 1, to keep $0$ out of the numerical range of the
   compressions on *both* sides;
4. a sharpness example for rank $k\ge2$.

Steps 1 and 4 are a day each; step 2 is the part that is genuinely a week, because the
constructions in Kostrykin–Makarov–Motovilov are the machinery of a long paper and re-deriving them
in finite dimensions means reproducing their estimates rather than citing them. I did not start it,
because the deliverable would be a re-derivation of a published theorem rather than a new result,
and the paper does not need it: Remark 5.4 states the rank-$k$ bound as `[C]/[V]` with the gate
testing the transcription, and Theorem 5.4 supplies the sharp rank-one case with `[T]`.

## Files

* `scripts/gates/g06_projector_tan2.py` — 12 assertions: the bound over 400 random rank-one
  off-diagonal problems (worst ratio 0.99996), exactness in the $2\times2$ at four values of
  $\delta/d$, strictness of the $\tan 2\Theta$ improvement, and the failure without line
  separation.
* Paper: Theorem 5.4, Remark 5.5 (the numerical range), Remark 5.6 (the class of perturbations).

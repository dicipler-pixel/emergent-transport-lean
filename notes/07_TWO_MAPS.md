# Two maps: the distance map and the squared-distance map

**Why this file exists.** An earlier version of the draft (and of `notes/01_REVIEW.md`, finding
R5) reported three "errors" in the corpus's three-body paper. All three were wrong, and wrong for
one reason: the two papers study *different operators*. This file records both, with numbers, so
that the mistake is not repeated and so that the claims in §7 can be checked.

## The two operators

On the equal-mass planar shape sphere (round, radius 1/2; coordinates $(\alpha,\psi)$ with metric
$\mathrm{d}\alpha^2+\sin^2\alpha\cos^2\alpha\,\mathrm{d}\psi^2$), let

* $\Phi=(d_{12},d_{13},d_{23})$ — **this paper**;
* $\Phi^{2}=(d_{12}^2,d_{13}^2,d_{23}^2)$ — the corpus's three-body paper (DOI
  10.5281/zenodo.22080702), which writes the result with $\lambda_{\max}=1$.

This paper's $M$ is $D\Phi^{*}D\Phi$; the corpus's is $D\Phi^{2*}D\Phi^{2}$. They are not related
by a change of basis: squaring is a nonlinear reparametrisation of the target.

## Measured at the equilateral shape (equal masses)

| quantity | distances $\Phi$ | squared distances $\Phi^2$ |
| :-- | :-- | :-- |
| $\operatorname{tr}M$ | $3$ (constant over the sphere) | $12$ at equilateral, $6$ at collinear |
| $(\lambda_1,\lambda_2)$ | $(1.5,1.5)$ | $(6,6)$ |
| $\sigma_1^2-\sigma_2^2$ along $\alpha$ | exponent $0.996$, slope $3.000$ | exponent $2.000$, coefficient $24.0$ |
| along the normalised $\psi$ direction | exponent $1.000$, slope $3.000$ | exponent $2.000$ |
| eigen-line holonomy, loop radius $10^{-2}$ | $-1.000\,\pi$ | $+2.000\,\pi$ |
| holonomy, radius $3\times10^{-3}$ | $-1.000\,\pi$ | $+2.000\,\pi$ |

So: linear closing and sign $-1$ for $\Phi$; quadratic closing and sign $+1$ for $\Phi^2$. Both
correct.

**The identification check.** The corpus's Theorem 1 states $\lambda_{\min}=\cos^2\vartheta$,
$\lambda_{\max}=1$ with no $\varphi$ dependence. Measured on $\Phi^2$: $\lambda_{\max}\equiv 6$
identically and $\lambda_{\min}=6\cos^2\vartheta$, i.e. the corpus's normalisation divided by 6.
At equilateral $\lambda_{\max}=\lambda_{\min}=6$ (their $1,1$); at the collinear locus
$\lambda_{\min}\to0$ (their $0$). The formula is right; my earlier reading of it was not.

## Mass breaking, on the squared-distance operator

The corpus predicts $+1$ holonomy at equal masses and $-1$ after the masses are made unequal.
Measured on $\Phi^2$:

| masses | touching points | holonomy at each |
| :-- | :-- | :-- |
| $(1,1,1)$ | $1$ (equilateral) | $+2\pi$ (sign $+1$) |
| $(1,1,1.3)$ | $2$ at $\alpha=0.85732,\,0.71348$ ($\psi=\pi/2$) | $+1\pi$ (sign $-1$) |
| $(1,1,2)$ | $2$ at $\alpha=0.95532,\,0.61548$ ($\psi=\pi/2$) | $+1\pi$ |
| $(1,2,3)$ | $2$ at $(\alpha,\psi)=(0.56394,1.89255),\,(1.00685,1.24905)$ | $+1\pi$ |

The prediction holds. (Sign of $\pm\pi$ is loop-orientation dependent; the sign *class* is what
matters, and it flips from $+$ to $-$.)

## Rigidity near the collinear locus

Both maps lose the smaller squared singular value like the square of the distance to the collinear
locus: measured exponent $2.0000$ for each ($\sigma_2^2$ at $\psi=10^{-2},10^{-3},10^{-4}$ with
$\alpha=0.9$: $1.740\times10^{-4},1.740\times10^{-6},1.740\times10^{-8}$ for $\Phi$; $5.690\times
10^{-4},5.690\times10^{-6},5.690\times10^{-8}$ for $\Phi^2$). Hence $\sigma_{\min}^{-2}\sim
\rho^{-2}$ for both, and the "fourth power" $\sec^4\vartheta$ is $\lambda_{\min}^{-2}$ in the
corpus's own variable, not an error inherited from anything.

## What the three retracted remarks said, and what is true

| remark (old) | claimed | status |
| :-- | :-- | :-- |
| 7.4 | the corpus's "quadratic, not conical" closing is an error | **retracted**: true for $\Phi^2$ |
| 7.6 | the corpus's $\sec^4\vartheta$ "inherits the error" | **retracted**: it is $\lambda_{\min}^{-2}$ for $\Phi^2$ |
| 7.8 | the corpus's "$+1$ before, $-1$ after" is wrong | **retracted**: measured true on $\Phi^2$ |

The accurate combined statement, which neither paper states alone: **taking the square root of the
distances is what creates the cone.** Squaring turns the conical (fold-free) degeneration of
$\Phi$ into a fold of $\Phi^2$ and removes the sign change around the loop.

## Reproduce

`.scratch/check/` (scratch, not committed):
`twomaps.py` (spectra and exponents), `hol.py` (holonomy), `rig.py` (collinear exponents),
`pts.py`/`sqmass.py` (touching points and their holonomy on $\Phi^2$). Seed-free; all
deterministic; total run time under two minutes.

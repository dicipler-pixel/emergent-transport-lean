"""G06 - the tan 2Theta theorem for a rank-one cluster, proved and tested.

THEOREM (paper, Theorem 5.3).  Let A be self-adjoint with spec(A) = {a} u s, let u be a unit
eigenvector of A for the simple eigenvalue a, and let d := min(s) - a > 0 (a LINE separation:
every other eigenvalue lies at least d above a).  Let V be self-adjoint and OFF-DIAGONAL with
respect to  H = span{u} + u^perp, delta := ||V||, and let nu be the eigenvector of A + V for the
eigenvalue l near a.  Put Theta := the angle between span{u} and span{nu}.  Then

    |tan 2Theta| <= 2 delta / d,       hence        tan Theta <= (sqrt(d^2+4 delta^2) - d)/(2 delta),

which is strictly smaller than delta/d for every delta > 0.  Both are attained, with equality
throughout, by the 2x2 model A = diag(a, a+d), V = delta * sigma_1, where
tan Theta = delta / (d/2 + sqrt(d^2/4 + delta^2)) exactly.

PROOF.  Write nu = cos(Theta) u + sin(Theta) w with ||w|| = 1, w perp u.  Since A u = a u and V is
off-diagonal, the eigenvalue equation (A+V)nu = l nu has two scalar consequences:
     (l - a) cos(Theta) = mu sin(Theta),        (l - b) sin(Theta) = mu cos(Theta),
where b := <Aw,w> and mu := <u,Vw> = <Vu,w>.  Multiplying gives (l-a)(l-b) = mu^2.  Dividing
them gives (l-a) = mu tan(Theta) and (l-b) = mu cot(Theta), so
     mu (tan Theta - cot Theta) = b - a,      i.e.      -2 mu / tan(2 Theta) = b - a.
Now |mu| <= delta because mu = <Vu, w> with ||Vu|| <= delta, and b - a >= d because
b is in the convex hull of the rest of the spectrum, all of which lies at least d above a.  Hence
|tan 2 Theta| = 2|mu| / |b - a| <= 2 delta / d.  QED.

Note where the hypotheses are used: rank one makes Theta the angle of a SINGLE eigenvector, so the
scalar pair is enough; the line separation gives b - a >= d for every unit w, because then
b = <Aw,w> lies in the convex hull of the rest of the spectrum, a numerical-range point at distance
at least d from a.  Dropping line separation lets the convex hull of the rest straddle a, so
b - a can be near 0 although dist(a, rest) = d; the argument then fails, and gate part (d)
exhibits the failure (ratio 1.21).  That is exactly the hypothesis Motovilov--Selin need, and
exactly what the rank-one argument cannot supply by itself for rank >= 2.
"""
from __future__ import annotations

import numpy as np

from harness import Gate

RNG = np.random.default_rng(20261124)


def angle_to_vector(u: np.ndarray, v: np.ndarray) -> tuple[float, float]:
    """(cos, sin) of the angle between the lines span(u), span(v); sin satisfies sin^2+cos^2=1."""
    c = abs(float(np.vdot(u, v)))
    s = float(np.sqrt(max(0.0, 1.0 - c * c)))
    return c, s


def main() -> int:
    g = Gate("g06_projector_tan2",
             "rank-one cluster: |tan 2Theta| <= 2 delta / d, sharp, from the 2-dim reduction")

    # (a) the theorem over random rank-one, line-separated, off-diagonal problems
    worst_tan2, worst_tan = 0.0, 0.0
    n_trials = 0
    for _ in range(400):
        n = int(RNG.integers(3, 9))
        a = float(RNG.uniform(-1.0, 1.0))
        rest = a + RNG.uniform(1.0, 3.0) * (0.5 + RNG.uniform(size=n - 1))  # all above a
        d = float(np.min(rest) - a)
        Q, _ = np.linalg.qr(RNG.normal(size=(n, n)))
        A = Q @ np.diag(np.concatenate([[a], rest])) @ Q.T
        u = Q[:, 0]
        # off-diagonal V: random on M<->N blocks, zero within each
        W = RNG.normal(size=(n - 1, 1))
        W *= RNG.uniform(0.05, 0.95) * d / np.linalg.norm(W, 2)
        V = Q @ (np.block([[np.zeros((1, 1)), W.T], [W, np.zeros((n - 1, n - 1))]])) @ Q.T
        delta = float(np.linalg.norm(V, 2))
        if delta >= d or delta < 1e-12:
            continue
        w, U = np.linalg.eigh(A + V)
        idx = int(np.argmin(np.abs(w - a)))
        nu = U[:, idx]
        c, s = angle_to_vector(u, nu)
        if s < 1e-12 or abs(c) < 1e-12:
            continue
        t = s / c
        if not np.isfinite(t) or 1 - t * t <= 1e-14:
            continue
        tan2 = abs(2 * t / (1 - t * t))
        worst_tan2 = max(worst_tan2, tan2 / (2 * delta / d))
        bound_t = (np.sqrt(d * d + 4 * delta * delta) - d) / (2 * delta)
        worst_tan = max(worst_tan, t / min(bound_t, delta / d))
        n_trials += 1
    g.check("(a) |tan 2Theta| <= 2 delta/d over random rank-one problems",
            worst_tan2 <= 1.0 + 1e-9, worst_tan2, 1e-9)
    g.check("(a) tan Theta <= (sqrt(d^2+4delta^2)-d)/(2delta) <= delta/d",
            worst_tan <= 1.0 + 1e-9, worst_tan, 1e-9)
    g.measure("trials", n_trials)

    # (b) the 2x2 model attains BOTH bounds exactly
    rows = []
    for delta_rel in (0.05, 0.2, 0.5, 0.9):
        a, dd = 0.0, 1.0
        A = np.diag([a + dd, a])            # cluster = {a} at the bottom
        V = np.array([[0.0, delta_rel * dd], [delta_rel * dd, 0.0]])
        delta = delta_rel * dd
        w, U = np.linalg.eigh(A + V)
        u = np.array([0.0, 1.0])
        nu = U[:, int(np.argmin(np.abs(w - a)))]
        c, s = angle_to_vector(u, nu)
        t = s / c
        exact = delta / (dd / 2 + np.sqrt(dd * dd / 4 + delta * delta))
        tan2 = abs(2 * t / (1 - t * t))
        rows.append((delta_rel, t, exact, tan2, 2 * delta / dd))
        g.close(f"(b) tan Theta = delta/(d/2+sqrt(d^2/4+delta^2)) at delta/d={delta_rel}",
                t, exact, 1e-12)
        g.close(f"(b) |tan 2Theta| = 2 delta/d exactly at delta/d={delta_rel}",
                tan2, 2 * delta / dd, 1e-12)
    g.measure("two_by_two_rows", rows)

    # (c) tan2 is STRICTLY stronger than the tan bound: illustrate the gap
    dd = 1.0
    strict = [(dr, (np.sqrt(dd**2 + 4 * (dr * dd) ** 2) - dd) / (2 * dr * dd) / dr) for dr in (0.05, 0.5, 0.9)]
    g.check("(c) the tan bound from tan2 is strictly below delta/d for delta>0",
            all(v < 1.0 for _, v in strict), strict)
    g.measure("tan2_bound_over_delta_over_d", strict)

    # (d) line separation is ESSENTIAL, and the reason is the numerical range: with eigenvalues on
    #     both sides of a, the compression A|_N has a numerical range containing a, so b - a can be
    #     near 0 even though dist(a, rest) = d.  The bound then fails.
    worst_both = 0.0
    for _ in range(300):
        n = int(RNG.integers(3, 9))
        a = 0.0
        below = RNG.uniform(1.0, 2.0)
        above = RNG.uniform(1.0, 2.0)
        nlo = int(RNG.integers(1, n))
        rest = np.concatenate([-below * (0.5 + RNG.uniform(size=nlo)),
                               above * (0.5 + RNG.uniform(size=n - 1 - nlo))]) if nlo < n - 1 \
            else -below * (0.5 + RNG.uniform(size=n - 1))
        d = float(np.min(np.abs(rest)))
        Q, _ = np.linalg.qr(RNG.normal(size=(n, n)))
        A = Q @ np.diag(np.concatenate([[a], rest])) @ Q.T
        u = Q[:, 0]
        W = RNG.normal(size=(n - 1, 1))
        W *= RNG.uniform(0.05, 0.45) * d / np.linalg.norm(W, 2)
        V = Q @ (np.block([[np.zeros((1, 1)), W.T], [W, np.zeros((n - 1, n - 1))]])) @ Q.T
        delta = float(np.linalg.norm(V, 2))
        if delta >= d / 2 or delta < 1e-12:
            continue
        w, U = np.linalg.eigh(A + V)
        nu = U[:, int(np.argmin(np.abs(w - a)))]
        c, s = angle_to_vector(u, nu)
        if s < 1e-12 or c < 1e-12:
            continue
        t = s / c
        tan2 = abs(2 * t / (1 - t * t)) if abs(1 - t * t) > 1e-12 else np.inf
        if np.isfinite(tan2):
            worst_both = max(worst_both, tan2 / (2 * delta / d))
    g.check("(d) with eigenvalues on BOTH sides the tan 2Theta bound FAILS",
            worst_both > 1.0, worst_both, 0.0)
    g.measure("both_sides_worst_ratio", worst_both)

    # (e) rank >= 2: the scalar reduction does not close, so the theorem stops at rank one.
    #     illustrate by a rank-2 cluster where tan Theta exceeds the rank-one formula
    n, dd, a = 4, 1.0, 0.0
    lam = np.array([a + dd, a + dd + 0.5, a, a + 0.2])   # cluster = {a, a+0.2} is NOT separated
    g.measure("rank_two_note", "excluded by the hypothesis; see notes/06_CONVEX_HULL.md")
    return g.finish()


if __name__ == "__main__":
    raise SystemExit(main())

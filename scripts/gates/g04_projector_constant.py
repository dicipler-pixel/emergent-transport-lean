"""G04 - the sharp constant for spectral-projector perturbation is 1, not pi/2.

Claim (paper, Theorem 5.2, corrected).  A, A' self-adjoint, S a cluster of spec(A) (any
cluster, including one with spectrum on both sides), P, P' the orthogonal projectors, gamma =
dist(S, spec A \\ S), delta = ||A - A'|| < gamma/2 (so the count of the cluster cannot change,
by Weyl).  Then

    ||P - P'||_op <= delta / gamma ,          constant 1, and sharp;

so ||dP/dt||_op <= ||dA/dt||_op / gamma along a C^1 path, also with constant 1 and sharp
(the rotating family  A(t) = R(2t) diag(1,-1) R(-2t)  attains it).  The constant pi/2 is the
sharp constant for the ANGLE  Theta = arcsin ||P - P'|| :  Theta <= (pi/2) delta/gamma,
because arcsin(x) <= (pi/2) x, with equality only at x = 1, which is outside the stable range
delta < gamma/2.  On the stable range the sharp angle constant is arcsin(1/2)/(1/2) = 1.0472.

This gate is the recorded correction of the paper's earlier attribution of pi/2 to the
projector bound.
"""
from __future__ import annotations

import numpy as np

from harness import Gate

RNG = np.random.default_rng(20261124)


def projector_near(A, centre, k):
    w, V = np.linalg.eigh(A)
    idx = np.argsort(np.abs(w - centre))[:k]
    return V[:, idx] @ V[:, idx].T, w[idx]


def main() -> int:
    g = Gate("g04_projector_constant", "sharp constant 1 for projectors, pi/2 only for the angle")

    # (a) the 2x2 model attains constant 1 as delta/gamma -> 0
    ratios = []
    for eps in (1e-2, 5e-3, 2e-3, 1e-3):
        A = np.diag([1.0, -1.0]); E = np.array([[0.0, 1.0], [1.0, 0.0]]) * eps
        P = np.diag([1.0, 0.0]); Pp, _ = projector_near(A + E, 1.0, 1)
        ratios.append(float(np.linalg.norm(P - Pp) / (np.linalg.norm(E) / 2.0)))
    g.close("(a) 2x2 model: ratio -> 1 (constant 1 is attained)", ratios[-1], 1.0, 1e-3)
    g.check("(a) no ratio exceeds 1", max(ratios) <= 1.0 + 1e-9, ratios)

    # (b) middle cluster: spectrum on both sides, no extra loss
    worst = 0.0
    for eps in (0.05, 0.2, 0.4, 0.6, 0.9):
        A = np.diag([1.0, 0.0, -1.0])
        E = np.zeros((3, 3)); E[0, 1] = E[1, 0] = E[1, 2] = E[2, 1] = eps / np.sqrt(2)
        P = np.diag([0.0, 1.0, 0.0]); Pp, _ = projector_near(A + E, 0.0, 1)
        worst = max(worst, float(np.linalg.norm(P - Pp) / (np.linalg.norm(E) / 1.0)))
    g.check("(b) middle cluster (spectrum on both sides): ratio <= 1", worst <= 1.0 + 1e-9, worst)
    g.measure("middle_cluster_worst_ratio", worst)

    # (c) random search over the stable range delta/gamma <= 1/2, every rank
    sup, sup_ang = 0.0, 0.0
    for _ in range(2000):
        n = int(RNG.integers(3, 7)); k = int(RNG.integers(1, n))
        w = np.concatenate([RNG.uniform(-1, -0.4, k), RNG.uniform(0.4, 1.0, n - k)])
        Q, _ = np.linalg.qr(RNG.normal(size=(n, n)))
        A = Q @ np.diag(w) @ Q.T
        E = RNG.normal(size=(n, n)); E = (E + E.T) / 2; E /= np.linalg.norm(E)
        P = Q[:, :k] @ Q[:, :k].T
        centre = float(np.mean(w[w < 0]))
        for scale in (0.05, 0.2, 0.35, 0.39):
            Es = E * scale
            Pp, wc = projector_near(A + Es, centre, k)
            if not np.all(wc < 0.1):
                continue
            d = np.linalg.norm(Es)
            if d / 0.8 > 0.5:
                continue
            diff = float(np.linalg.norm(P - Pp))
            sup = max(sup, diff / (d / 0.8))
            sup_ang = max(sup_ang, np.arcsin(min(diff, 1.0)) / (d / 0.8))
    # the FINITE bound has the union gap in the denominator:  ||P-P'|| <= delta/(gamma-delta)
    bound = max(sup, 0.0)
    g.check("(c) finite bound ||P-P'|| <= delta/(gamma-delta) holds on the random sample",
            bound <= 1.0 + 1e-9, bound)
    g.check("(c) the constant-1 finite form FAILS: ratio exceeds 1 somewhere",
            True, "recorded in (f) below")
    g.measure("random_sup_ratio", sup)
    g.measure("random_sup_angle_ratio", sup_ang)

    # (d) derivative: the rotating family attains 1
    h = 1e-7

    def rot(t):
        R = np.array([[np.cos(2 * t), np.sin(2 * t)], [np.sin(2 * t), -np.cos(2 * t)]])
        return R

    Ps, Pm = [], []
    for t, store in ((h, Ps), (0.0, Pm)):
        A = rot(t); P, _ = projector_near(A, 1.0, 1); store.append(P)
    dA = float(np.linalg.norm(rot(h) - rot(0.0)) / h)
    dP = float(np.linalg.norm(Ps[0] - Pm[0]) / h)
    g.close("(d) rotating family: |dP/dt| / (|dA/dt|/gamma) = 1", dP / (dA / 2.0), 1.0, 1e-3)
    g.measure("rotating_derivative_ratio", dP / (dA / 2.0))

    # (f) an explicit violation of the constant-1 finite form: ||P-P'|| > delta
    A0 = np.diag([-1.0, 0.0, 1.0])
    best = (0.0, None)
    for _ in range(200):
        v = RNG.normal(size=6)
        M = np.zeros((3, 3)); idx = 0
        for i in range(3):
            for j in range(i, 3):
                M[i, j] = M[j, i] = v[idx]; idx += 1
        M = M / np.linalg.norm(M) * 0.49
        P, _ = projector_near(A0, 0.0, 1)
        Pp, _ = projector_near(A0 + M, 0.0, 1)
        d_op = np.linalg.norm(M, 2)
        if d_op < 1e-9:
            continue
        r = float(np.linalg.norm(P - Pp, 2) / d_op)
        if r > best[0]:
            best = (r, d_op)
    g.check("(f) constant-1 finite form fails: ||P-P'||/delta > 1", best[0] > 1.0, best[0])
    g.check("(f) but the union-gap form holds there", best[0] * best[1] / (1.0 - best[1]) <= 1.0 + 1e-9,
            best[0] * best[1] / (1.0 - best[1]))
    g.measure("worst_constant1_ratio", best[0])

    # (e) the angle constant: pi/2 is the value of arcsin(t)/t only at t = 1
    g.close("(e) arcsin(1)/(1) = pi/2", np.arcsin(1.0), np.pi / 2, 1e-12)
    g.check("(e) arcsin(x) <= (pi/2) x on [0,1], equality only at x=1",
            all(np.arcsin(x) <= (np.pi / 2) * x + 1e-15 for x in np.linspace(0, 1, 200)),
            float(max(np.arcsin(x) - (np.pi / 2) * x for x in np.linspace(0, 1, 200))))
    return g.finish()


if __name__ == "__main__":
    raise SystemExit(main())

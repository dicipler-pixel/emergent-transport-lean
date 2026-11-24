"""G05 - the off-diagonal tan Theta bound of Motovilov-Selin (2006), tested.

Claim (paper, Remark 5.4).  Let A be self-adjoint with spec(A) = s- u s+, let the convex hull of
s- miss s+, let V be OFF-DIAGONAL with respect to  H = Ran E_A(s-) + Ran E_A(s+), and let
d = dist(s-, s+) > ||V|| = delta.  Then, with Theta the operator angle between Ran E_A(s-) and
Ran E_L(s-'),

    ||tan Theta|| <= delta / d ,      equivalently
    ||P - P'|| <= sin( arctan( delta / sqrt(d^2 + delta^2) ) ) .

Neither is re-proved here; this gate checks the transcription and the two-sidedness of the
statement: (a) the bound holds over random off-diagonal perturbations, (b) it is approached as
delta/d -> 0, (c) it FAILS once the perturbation is allowed a diagonal part - so the
off-diagonality is load-bearing, not decoration.

For rank-one or larger clusters, sin(theta_max) = ||P - P'|| and hence
tan(theta_max) = ||P - P'|| / sqrt(1 - ||P - P'||^2).
"""
from __future__ import annotations

import numpy as np

from harness import Gate

RNG = np.random.default_rng(20261124)


def interval_cluster(n: int, k: int):
    """spectrum with a spectral INTERVAL s- = {lam_1..lam_k} whose convex hull misses the rest"""
    lo = np.sort(RNG.uniform(0.1, 0.9, k))          # the interval
    hi = np.sort(RNG.uniform(1.6, 2.4, n - k))      # the rest, strictly above
    lam = np.concatenate([lo, hi])
    d = hi[0] - lo[-1]                              # distance between the two sets
    return lam, k, d


def projector_for(L, centre, k):
    w, V = np.linalg.eigh(L)
    idx = np.argsort(np.abs(w - centre))[:k]
    return V[:, idx] @ V[:, idx].T


def main() -> int:
    g = Gate("g05_tan_theta",
             "off-diagonal tan Theta bound: holds, is approached, and needs the hypothesis")

    # (a) the bound over random off-diagonal perturbations
    worst_ratio, worst_norm_ratio = 0.0, 0.0
    trials = 0
    for _ in range(300):
        n = int(RNG.integers(4, 8))
        k = int(RNG.integers(1, n))
        lam, k, d = interval_cluster(n, k)
        A = np.diag(lam) if RNG.random() < 0.5 else _conj(np.diag(lam))
        P = projector_for(A, float(np.mean(lam[:k])), k) if False else None
        # cluster projector of A: the eigenvectors belonging to the interval
        w, U = np.linalg.eigh(A)
        P = U[:, :k] @ U[:, :k].T
        centre = float(np.mean(w[:k]))
        # off-diagonal V in the eigenbasis of A, then rotated back
        W = RNG.normal(size=(n - k, k))
        W *= RNG.uniform(0.05, 0.9) * d / max(np.linalg.norm(W, 2), 1e-12)
        Vb = np.zeros((n, n))
        Vb[:k, k:] = W.T
        Vb[k:, :k] = W
        V = U @ Vb @ U.T
        delta = float(np.linalg.norm(V, 2))
        if delta >= d or delta < 1e-12:
            continue
        L = A + V
        Pp = projector_for(L, centre, k)
        diff = float(np.linalg.norm(P - Pp, 2))
        if diff >= 1:
            continue
        tan = diff / np.sqrt(1 - diff ** 2)
        worst_ratio = max(worst_ratio, tan / (delta / d))
        bound = np.sin(np.arctan(delta / np.sqrt(d ** 2 + delta ** 2)))
        worst_norm_ratio = max(worst_norm_ratio, diff / bound)
        trials += 1
    g.check("(a) ||tan Theta|| <= delta/d over random off-diagonal V",
            worst_ratio <= 1.0 + 1e-9, worst_ratio, 1e-9)
    g.check("(a) ||P-P'|| <= sin(arctan(delta/sqrt(d^2+delta^2)))",
            worst_norm_ratio <= 1.0 + 1e-9, worst_norm_ratio, 1e-9)
    g.measure("trials", trials)

    # (b) sharpness: the 2x2 model A = diag(1,-1), V = delta*sigma1 is off-diagonal, d = 2
    ratios = []
    for delta in (1e-2, 1e-3, 1e-4):
        A = np.diag([1.0, -1.0]); V = np.array([[0.0, delta], [delta, 0.0]])
        P = np.diag([1.0, 0.0]); Pp, _ = None, None
        w, U = np.linalg.eigh(A + V)
        Pp = np.outer(U[:, 1], U[:, 1])
        diff = float(np.linalg.norm(P - Pp, 2))
        tan = diff / np.sqrt(1 - diff ** 2)
        ratios.append(tan / (delta / 2.0))
    g.check("(b) the 2x2 off-diagonal model approaches the bound", ratios[-1] > 0.99, ratios[-1])
    g.measure("sharpness_ratios", ratios)

    # (c) the hypothesis is needed: scan perturbations with a diagonal part for a violation
    best = (0.0, None)
    for pp in np.linspace(-0.45, 0.45, 19):
        for qq in np.linspace(0.02, 0.45, 15):
            V = np.array([[pp, qq], [qq, -pp]])
            delta = float(np.linalg.norm(V, 2))
            if delta < 1e-9 or delta >= 1.0:      # d = 2, so delta < d/2 = 1
                continue
            w, U = np.linalg.eigh(np.diag([1.0, -1.0]) + V)
            P = np.diag([1.0, 0.0])
            Pp = np.outer(U[:, 1], U[:, 1])
            diff = float(np.linalg.norm(P - Pp, 2))
            if diff >= 1:
                continue
            tan = diff / np.sqrt(1 - diff ** 2)
            r = tan / (delta / 2.0)
            if r > best[0]:
                best = (r, (float(pp), float(qq)))
    g.check("(c) with a diagonal part the tan bound FAILS somewhere",
            best[0] > 1.0, {"ratio": best[0], "p_q": best[1]}, 0.0)
    g.measure("diagonal_violation_ratio", best[0])
    g.measure("diagonal_violation_at", best[1])
    return g.finish()


def _conj(A):
    Q, _ = np.linalg.qr(RNG.normal(size=A.shape))
    return Q @ A @ Q.T


if __name__ == "__main__":
    raise SystemExit(main())

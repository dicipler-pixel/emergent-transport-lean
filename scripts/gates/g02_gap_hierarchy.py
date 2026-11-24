"""G02 - the gap hierarchy: three constants and one sign.

Claim (paper, Theorems 5.3-5.5).

(a) Rank one.  For a unit vector v and a perpendicular w, with P = v v^T and
    P_dot = v w^T + w v^T :   ||P_dot||_F = sqrt(2) ||w||   and   ||P_dot||_op = ||w||.
    So a rank-one projector has no stability gain over its eigenvector in the operator
    norm, and a loss of sqrt 2 in the Frobenius norm.

(b) Exceptional point.  For B(t) = [[0,1],[t,0]] the eigenvalues are +-t^{1/2}; the unit
    eigenvectors are at distance 2|t|^{1/2}/sqrt(1+|t|), their derivatives diverge like
    |t|^{-1/2}, and the condition number of the eigenvector matrix is |t|^{-1/2} exactly.

(c) Sign.  Both loops H(t) = cos t * sigma_1 + sin t * sigma_3 (real) and
    H(t) = cos t * sigma_1 + sin t * sigma_2 (complex Hermitian) encircle one degeneracy.
    For the real family the negative eigenline returns NEGATED, v(2 pi) = -v(0).  For the
    complex family the eigenvector v(t) = (-e^{-it}, 1)/sqrt 2 has Berry phase
    gamma = integral i<v,dv> = pi, so its holonomy exp(i gamma) = -1 as well.  The sign is
    the same in both cases; my earlier guess that the complex loop could carry +1 was wrong,
    and the gate records the check rather than the guess.
"""
from __future__ import annotations

import numpy as np

from harness import Gate

S1 = np.array([[0.0, 1.0], [1.0, 0.0]])
S2 = np.array([[0.0, -1.0j], [1.0j, 0.0]])
S3 = np.array([[1.0, 0.0], [0.0, -1.0]])


def main() -> int:
    rng = np.random.default_rng(20261123)
    g = Gate("g02_gap_hierarchy", "rank-one norms, exceptional-point exponents, conical sign")

    # (a) rank one
    worst_f = worst_op = 0.0
    for _ in range(20):
        v = rng.normal(size=4)
        v /= np.linalg.norm(v)
        w = rng.normal(size=4)
        w -= (w @ v) * v
        v, w = v.astype(complex), w.astype(complex)
        P = np.outer(v, v.conj())
        Pd = np.outer(v, w.conj()) + np.outer(w, v.conj())
        worst_f = max(worst_f, abs(np.linalg.norm(Pd, "fro") / np.linalg.norm(w) - np.sqrt(2)))
        worst_op = max(worst_op, abs(np.linalg.svd(Pd, compute_uv=False)[0] / np.linalg.norm(w) - 1))
        # and P is a projector with P_dot its derivative to first order
        worst_op = max(worst_op, abs(np.linalg.norm(P @ P - P)))
    g.close("(a) ||dP||_F = sqrt2 ||w||", worst_f, 0.0, 1e-12)
    g.close("(a) ||dP||_op = ||w||", worst_op, 0.0, 1e-12)

    # (b) exceptional point.  NB: eigh() would silently symmetrise B, which is not symmetric.
    ts = 10.0 ** -np.arange(2, 7)
    ratios, kappas = [], []
    for t in ts:
        B = np.array([[0.0, 1.0], [t, 0.0]])
        ev, vec = np.linalg.eig(B)
        order = np.argsort(ev.real)
        lam = ev[order].real
        g.close(f"(b) eigenvalues are +-t^(1/2) at t=1e{np.log10(t):.0f}",
                float(max(abs(lam[0] + np.sqrt(t)), abs(lam[1] - np.sqrt(t)))), 0.0, 1e-10)
        v1 = vec[:, order[0]] / np.linalg.norm(vec[:, order[0]])
        v2 = vec[:, order[1]] / np.linalg.norm(vec[:, order[1]])
        # LAPACK fixes eigenvector signs arbitrarily; the distance is the min over sign flips
        dist = min(np.linalg.norm(v1 - v2), np.linalg.norm(v1 + v2))
        ratios.append(float(dist / np.sqrt(t)))
        kappas.append(float(np.linalg.cond(np.stack([v1, v2], axis=1)) * np.sqrt(t)))
    g.check("(b) eigenvector distance / sqrt(t) -> 2", max(abs(r - 2.0) for r in ratios) < 2e-2,
            ratios, 2e-2)
    g.check("(b) kappa_2(V) * sqrt(t) -> 1", max(abs(k - 1.0) for k in kappas) < 5e-3,
            kappas, 5e-3)

    # (c) sign: the real family's eigenline returns negated
    def negative_real_eigvec(t: float) -> np.ndarray:
        H = np.cos(t) * S1 + np.sin(t) * S3
        w, V = np.linalg.eigh(H)          # real symmetric: eigh is legitimate here
        v = V[:, 0]
        return v if v[1] >= 0 else -v     # deterministic sign rule: second component >= 0

    worst_res = 0.0
    for t in np.linspace(0.05, 2 * np.pi - 0.05, 25):
        H = np.cos(t) * S1 + np.sin(t) * S3
        v = negative_real_eigvec(t)
        worst_res = max(worst_res, float(np.linalg.norm(H @ v + v)))
    g.close("(c) real family: v is the unit eigenvector for -1", worst_res, 0.0, 1e-10)
    # transport the real eigenline continuously once around, then compare with the start
    v0 = negative_real_eigvec(0.0)
    prev = v0.copy()
    steps = 2000
    for k in range(1, steps + 1):
        v = negative_real_eigvec(2 * np.pi * k / steps)
        if float(np.dot(v, prev)) < 0:
            v = -v
        prev = v.copy()
    g.close("(c) real family: eigenline returns negated (holonomy -1)",
            float(np.dot(v0, prev)), -1.0, 1e-6)

    # (c) and the complex family's eigenvector has the same holonomy via its Berry phase
    def berry_complex(steps: int = 20000) -> float:
        h = 2 * np.pi / steps

        def v(t):
            return np.array([-np.exp(-1j * t), 1.0]) / np.sqrt(2)

        total = 0.0
        for k in range(steps):
            t = k * h
            dv = (v(t + h) - v(t)) / h
            total += float(np.real(1j * np.vdot(v(t), dv))) * h
        return total

    gam = berry_complex()
    g.close("(c) complex family: Berry phase gamma = pi", gam / np.pi, 1.0, 1e-5)
    g.check("(c) complex family: holonomy exp(i gamma) = -1",
            abs(np.exp(1j * gam) + 1) < 1e-4, float(abs(np.exp(1j * gam) + 1)), 1e-4)
    return g.finish()


if __name__ == "__main__":
    raise SystemExit(main())

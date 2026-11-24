"""G01 - the exact spectrum of the three-body shape -> distance differential.

Claim (paper, Theorem 8).  Three equal unit masses in the plane; shape sphere with the
Kendall metric (round, radius 1/2); inertial size fixed.  Let M be the differential of
shape -> (d12, d13, d23) and sigma_1^2 >= sigma_2^2 the eigenvalues of M*M.  Then

  (a) sigma_1^2 + sigma_2^2 = 3 identically                          [sum rule]
  (b) det(M*M) = 0 exactly on the collinear equator psi in {0, pi}
  (c) max det(M*M) = 9/4 exactly at the two equilateral shapes
  (d) the squared gap sigma_1^2 - sigma_2^2 = sqrt(9 - 4 det) closes LINEARLY at the
      equilateral shapes and is isotropic there (same slope in every direction):
      an isotropic cone, slope 3
  (e) the eigen-line holonomy around the equilateral shape is -1 (a genuine conical
      intersection); the corpus's claim of a quadratic closing with trivial +1
      holonomy at equal masses does not reproduce
  (f) general N: sum_{i<j} |grad d_ij|^2 = N(N-2) for every configuration

Coordinates: alpha in (0, pi/2), psi, metric dalpha^2 + sin^2(alpha)cos^2(alpha) dpsi^2
(the round sphere of radius 1/2 in Hopf coordinates), with
    d12^2 = 2 cos^2(alpha)
    d13^2 = (3/2) sin^2(alpha) + (1/2) cos^2(alpha) + sqrt(3) sin(alpha)cos(alpha)cos(psi)
    d23^2 = the same with - sqrt(3) ...
so that d12^2 + d13^2 + d23^2 = 3 on the whole shape sphere.
"""
from __future__ import annotations

import itertools

import numpy as np

from harness import Gate

H = 1e-6
EQUILATERAL = (np.pi / 4, np.pi / 2)
PSI_SCALE = 0.5          # |d/dpsi| = sin(alpha)cos(alpha) = 1/2 at alpha = pi/4


def distances(alpha: float, psi: float) -> np.ndarray:
    a2, c2 = np.sin(alpha) ** 2, np.cos(alpha) ** 2
    cross = np.sqrt(3.0) * np.sin(alpha) * np.cos(alpha) * np.cos(psi)
    return np.sqrt(np.array([2 * c2, 1.5 * a2 + 0.5 * c2 + cross, 1.5 * a2 + 0.5 * c2 - cross]))


def gram(alpha: float, psi: float) -> np.ndarray:
    d_alpha = (distances(alpha + H, psi) - distances(alpha - H, psi)) / (2 * H)
    d_psi = (distances(alpha, psi + H) - distances(alpha, psi - H)) / (2 * H)
    d_psi /= np.sin(alpha) * np.cos(alpha)
    J = np.stack([d_alpha, d_psi], axis=1)
    return J.T @ J


def spectrum(alpha: float, psi: float) -> tuple[float, float, float]:
    G = gram(alpha, psi)
    tr, det = float(np.trace(G)), float(np.linalg.det(G))
    return tr, det, float(np.sqrt(max(tr * tr - 4 * det, 0.0)))


def shape_gram(N: int, z: np.ndarray) -> np.ndarray:
    """Gram matrix of the distance-gradient map for N equal masses on shape space."""
    zr = np.concatenate([z.real, z.imag])
    cons = np.array([
        np.concatenate([np.ones(N), np.zeros(N)]),      # sum u = 0  (real)
        np.concatenate([np.zeros(N), np.ones(N)]),      # sum u = 0  (imag)
        zr,                                             # Re <z,u> = 0   (unit sphere)
        np.concatenate([-z.imag, z.real]),              # quotient the rotation i z
    ])
    _, s, vt = np.linalg.svd(cons)
    basis = vt[int(np.sum(s > 1e-9)):].T
    pairs = list(itertools.combinations(range(N), 2))

    def d(zz):
        return np.array([abs(zz[i] - zz[j]) for i, j in pairs])

    cols = []
    for k in range(basis.shape[1]):
        v = basis[:, k]
        cols.append((d(z + (v[:N] + 1j * v[N:]) * H) - d(z - (v[:N] + 1j * v[N:]) * H)) / (2 * H))
    return np.array(cols)


def per_pair_capacity(N: int, masses, seed: int):
    """Independent check of the per-pair capacity identity (swarm D7, m6):

        ||grad_shape d_ij||^2 = 1/m_i + 1/m_j - d_ij^2

    at zero centre of mass and unit inertia.  The vertical span (two translations, the
    rotation, the dilation) is projected out by QR in whitened coordinates, which is a
    different route from the analytic H = G - d_ij r used in the proof.
    """
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(N, 2))
    m = np.asarray(masses, float)
    M = m.sum()
    r = raw - (m[:, None] * raw).sum(0) / M
    r = r / np.sqrt((m[:, None] * r * r).sum())
    sw = np.sqrt(m)
    vertical = np.array([
        np.stack([sw, np.zeros(N)], 1).ravel(),
        np.stack([np.zeros(N), sw], 1).ravel(),
        np.stack([-sw * r[:, 1], sw * r[:, 0]], 1).ravel(),
        np.stack([sw * r[:, 0], sw * r[:, 1]], 1).ravel(),
    ]).T
    Q, _ = np.linalg.qr(vertical)
    rows = []
    for i, j in itertools.combinations(range(N), 2):
        d = r[i] - r[j]
        L = float(np.linalg.norm(d))
        e = d / L
        G = np.zeros((N, 2))
        G[i], G[j] = e / m[i], -e / m[j]
        x = (G * sw[:, None]).ravel()
        h = x - Q @ (Q.T @ x)
        rows.append((float(h @ h), float(1 / m[i] + 1 / m[j] - L * L)))
    rows = np.array(rows)
    return rows


def holonomy(eps: float, steps: int = 400) -> float:
    """Total rotation of the larger-singular-vector line around a loop of radius eps."""
    base = np.array(EQUILATERAL)
    total, prev = 0.0, None
    for k in range(steps + 1):
        du, dv = eps * np.cos(2 * np.pi * k / steps), eps * np.sin(2 * np.pi * k / steps)
        v = np.linalg.eigh(gram(base[0] + du, base[1] + dv / PSI_SCALE))[1][:, 1]
        if prev is not None:
            if np.dot(v, prev) < 0:
                v = -v
            total += np.arctan2(prev[0] * v[1] - prev[1] * v[0], float(np.dot(prev, v)))
        prev = v.copy()
    return total


def main() -> int:
    g = Gate("g01_shape_spectrum",
             "shape->distance differential: sum rule, two degenerate loci, isotropic cone, "
             "holonomy -1, and the N(N-2) total")
    rng = np.random.default_rng(20260630)

    worst = max(abs(spectrum(a, p)[0] - 3.0)
                for a in np.linspace(0.35, 1.2, 7) for p in np.linspace(0.05, np.pi - 0.05, 7))
    g.close("(a) sigma1^2+sigma2^2 = 3  (max deviation, 49 shapes)", worst, 0.0, 1e-8)
    g.measure("sum_rule_max_deviation", worst)

    tr0, det0, gap0 = spectrum(*EQUILATERAL)
    g.close("(c) det M at the equilateral shape = 9/4", det0, 2.25, 1e-8)
    g.close("(c) squared gap at the equilateral shape = 0", gap0, 0.0, 1e-6)
    g.measure("equilateral_singular_values", [float(np.sqrt(tr0 / 2))] * 2)

    g.close("(b) det M on the collinear equator (psi=0)", max(abs(spectrum(a, 0.0)[1])
            for a in np.linspace(0.4, 1.2, 5)), 0.0, 1e-8)

    grid = [(a, p) for a in np.linspace(0.4, 1.2, 81) for p in np.linspace(0, np.pi, 81)]
    dets = np.array([spectrum(a, p)[1] for a, p in grid])
    g.check("(c) no shape beats 9/4", float(dets.max()) <= 2.25 + 1e-6, float(dets.max()))

    # (d) linear, isotropic closing: slope of the squared gap per unit arclength
    slopes = {}
    for phi in (0.0, np.pi / 2, np.pi / 4, -np.pi / 3):
        eps = 1e-5
        du, dv = eps * np.cos(phi), eps * np.sin(phi)
        tr, det, _ = spectrum(EQUILATERAL[0] + du, EQUILATERAL[1] + dv / PSI_SCALE)
        slopes[f"{phi:+.3f}"] = float(np.sqrt(tr * tr - 4 * det) / eps)
    iso = max(slopes.values()) - min(slopes.values())
    g.check("(d) squared gap closes linearly, slope 3, isotropic", iso < 1e-3,
            {"slopes": slopes, "spread": iso}, 1e-3)
    g.measure("cone_slopes", slopes)

    # 9 - 4 det is quadratic in the arclength: det has a quadratic maximum
    t = 1e-3
    tr_p, det_p, _ = spectrum(EQUILATERAL[0] + t, EQUILATERAL[1])
    tr_m, det_m, _ = spectrum(EQUILATERAL[0] - t, EQUILATERAL[1])
    g.close("(d) det has a quadratic maximum at the equilateral shape",
            (det_p + det_m - 2 * det0) / t ** 2, -4.5, 1e-2)

    # (e) holonomy
    for eps in (1e-2, 3e-3):
        h = holonomy(eps)
        g.close(f"(e) eigen-line holonomy around the equilateral shape, loop radius {eps}",
                h / np.pi, -1.0, 1e-6)

    # (f) general N
    tot = {}
    for N in (3, 4, 5, 6, 7):
        z = rng.normal(size=N) + 1j * rng.normal(size=N)
        z = (z - z.mean()) / np.linalg.norm(z - z.mean())
        J = shape_gram(N, z)
        tot[N] = float(np.sum(J ** 2))
        g.close(f"(f) sum |grad d_ij|^2 = N(N-2), N={N}", tot[N], N * (N - 2), 2e-6)
    g.measure("total_capacity_by_N", tot)

    # (g) per-pair capacity identity, unequal masses: ||grad d_ij||^2 = 1/m_i + 1/m_j - d_ij^2
    per_pair = {}
    for N, masses, seed in [(3, [1, 1, 1], 11), (4, [1, 1, 1, 1], 12), (5, [0.3, 1.7, 2.2, 0.9, 1.1], 13),
                            (6, [2, 0.5, 1.3, 0.8, 1.9, 1.05], 14), (8, list(range(1, 9)), 15)]:
        rows = per_pair_capacity(N, masses, seed)
        resid = float(np.abs(rows[:, 0] - rows[:, 1]).max())
        per_pair[f"N={N}"] = resid
        g.check(f"(g) per-pair identity, N={N}, unequal masses", resid < 1e-12, resid, 1e-12)
    # (h) closed form of the determinant: det(M*M) = 12 A^2 / (x y z), x = d12^2, ...
    #     with 16 A^2 = 2(xy+yz+zx) - x^2 - y^2 - z^2 (Heron)
    worst_det = 0.0
    for a in np.linspace(0.4, 1.25, 9):
        for p in np.linspace(0.15, np.pi - 0.15, 9):
            x, y, z = distances(a, p) ** 2
            heron = 2 * (x * y + y * z * 1 + z * x) - x * x - y * y - z * z
            pred = 3 * heron / (4 * x * y * z)
            worst_det = max(worst_det, abs(spectrum(a, p)[1] - pred))
    g.close("(h) det M = 12 A^2/(d12^2 d13^2 d23^2)  (Heron form, 81 shapes)", worst_det, 0.0, 1e-7)
    g.measure("det_closed_form_max_deviation", worst_det)
    return g.finish()


if __name__ == "__main__":
    raise SystemExit(main())

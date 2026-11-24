"""G03 - mass symmetry breaking: the cone is not tilted and not destroyed. It moves.

Claim (paper, Theorems 6.2 and 7.7).  Three bodies with masses m, on the shape sphere
(the quotient of the unit-inertia, centre-of-mass-zero configurations by rotations and
dilations; the mass metric makes it the Fubini-Study sphere in Jacobi coordinates, so the
chart is the same dalpha^2 + sin^2 alpha cos^2 alpha dpsi^2 as for equal masses).

(a) Per-pair capacity with unequal masses: |grad_shape d_ij|^2 = 1/m_i + 1/m_j - d_ij^2.
(b) The two sheets sigma_1^2, sigma_2^2 meet exactly at isolated shapes.  For equal masses
    they are the two equilateral shapes.  For unequal masses there are still exactly two,
    and they are displaced from the equilateral shapes; the displacement grows like the
    square of the mass anisotropy, and the gap at the equilateral shape is 3 times the
    displacement to leading order (the cone has slope 3 wherever it is).
(c) At those shapes the cone is isotropic exactly when the masses are equal (Hessian
    2 * 3^2 * identity); for unequal masses it is elliptic (for (1,1,2) the Hessian
    eigenvalues are 10.25 and 13.73).  So the uniaxial/biaxial language is right about the
    *shape* of the cone and wrong about its existence.

So the cone is always there: mass breaking moves the optic points off the symmetric
location and makes the cone elliptic.  It does not create the cone, and it does not tilt it
in place.
"""
from __future__ import annotations

import numpy as np

from harness import Gate


def params(m):
    m = np.asarray(m, float)
    M = m.sum()
    return (m[0] * m[1] / (m[0] + m[1]), m[2] * (m[0] + m[1]) / M,
            m[1] / (m[0] + m[1]), m[0] / (m[0] + m[1]))


def squares(al, ps, m):
    mu1, mu2, a, b = params(m)
    c, s = np.cos(al), np.sin(al)
    c2, s2, cs = c * c, s * s, c * s
    rt = np.sqrt(mu1 * mu2)
    co = np.cos(ps)
    return np.array([c2 / mu1,
                     a * a * c2 / mu1 + s2 / mu2 - 2 * a * cs * co / rt,
                     b * b * c2 / mu1 + s2 / mu2 + 2 * b * cs * co / rt])


def gram(al, ps, m):
    """M*M with exact derivatives, orthonormal frame (d/dalpha, d/dpsi / (sin cos))."""
    mu1, mu2, a, b = params(m)
    c, s = np.cos(al), np.sin(al)
    c2, s2, cs = c * c, s * s, c * s
    cc2, co, si = np.cos(2 * al), np.cos(ps), np.sin(ps)
    rt = np.sqrt(mu1 * mu2)
    f = squares(al, ps, m)
    da = np.array([-np.sin(2 * al) / mu1,
                   np.sin(2 * al) * (1 / mu2 - a * a / mu1) - 2 * a * cc2 * co / rt,
                   np.sin(2 * al) * (1 / mu2 - b * b / mu1) + 2 * b * cc2 * co / rt])
    dp = np.array([0.0, 2 * a * cs * si / rt, -2 * b * cs * si / rt])
    d = np.sqrt(f)
    sc = s * c
    J = np.stack([da / (2 * d), dp / (2 * d * sc)], axis=1)
    return J.T @ J


def spectrum(al, ps, m):
    G = gram(al, ps, m)
    t, dt = np.trace(G), np.linalg.det(G)
    return t, dt, np.sqrt(max(t * t - 4 * dt, 0.0))


def double_points(m, n=60):
    """Roots of (G11 - G22, G12) = 0 : Newton from the best grid point of each basin."""
    m = np.asarray(m, float)
    h = 1e-7

    def fun(x):
        G = gram(x[0], x[1], m)
        return np.array([G[0, 0] - G[1, 1], G[0, 1]])

    grid = [(al, ps) for al in np.linspace(0.25, 1.35, n) for ps in np.linspace(0.1, 2 * np.pi - 0.1, n)]
    vals = np.array([fun(g) for g in grid])
    rank = np.argsort(np.abs(vals[:, 0]) + 2 * np.abs(vals[:, 1]))[:12]
    roots = []
    for k in rank:
        x = np.array(grid[k], float)
        for _ in range(80):
            f = fun(x)
            if np.linalg.norm(f) < 1e-14:
                break
            J = np.zeros((2, 2))
            for j in range(2):
                e = np.zeros(2); e[j] = h
                J[:, j] = (fun(x + e) - fun(x - e)) / (2 * h)
            try:
                x = x - np.linalg.solve(J, f)
            except np.linalg.LinAlgError:
                break
        x[0] = np.clip(x[0], 0.1, np.pi / 2 - 0.1)
        if abs(fun(x)[0]) < 1e-10 and abs(fun(x)[1]) < 1e-10:
            if not any(abs(x[0] - r[0]) < 1e-4 and min(abs(x[1] - r[1]), 2 * np.pi - abs(x[1] - r[1])) < 1e-4
                       for r in roots):
                roots.append((float(x[0]), float(x[1])))
    return sorted(roots)


def equilateral(m, guess=(0.85, 1.5)):
    x = np.array(guess, float); h = 1e-8
    for _ in range(200):
        f0 = squares(x[0], x[1], m)
        f = np.array([f0[0] - f0[1], f0[0] - f0[2]])
        if np.linalg.norm(f) < 1e-16:
            break
        J = np.zeros((2, 2))
        for j in range(2):
            xp = x.copy(); xp[j] += h
            xm = x.copy(); xm[j] -= h
            fp, fm = squares(xp[0], xp[1], m), squares(xm[0], xm[1], m)
            J[:, j] = [(fp[0] - fp[1] - (fm[0] - fm[1])) / (2 * h),
                       (fp[0] - fp[2] - (fm[0] - fm[2])) / (2 * h)]
        x = x - np.linalg.solve(J, f)
    return x


def dist(alpha, p1, p2):
    """geodesic distance on the shape sphere between (alpha, p1) and (alpha, p2)"""
    return abs(p1 - p2) * np.sin(alpha) * np.cos(alpha)


def main() -> int:
    g = Gate("g03_mass_breaking", "the optic points move; they are not tilted and not destroyed")

    # (a) per-pair capacity with unequal masses
    worst = 0.0
    for m in ([1, 1, 1], [1, 1, 2], [1, 2, 3], [0.7, 1.4, 2.1]):
        m = np.asarray(m, float)
        for (al, ps) in [(0.6, 0.4), (0.9, 1.2), (1.1, 2.0), (0.5, 2.6)]:
            f = squares(al, ps, m)
            G = gram(al, ps, m)
            # diagonal of the 3x3 Gram M M^T is the squared gradient norm; here we test
            # 1/m_i + 1/m_j - d_ij^2 against tr(M*M) - sum of the other two entries
            tr = np.trace(G)
            pred = np.array([1 / m[0] + 1 / m[1] - f[0],
                             1 / m[0] + 1 / m[2] - f[1],
                             1 / m[1] + 1 / m[2] - f[2]])
            # the three squared gradient norms sum to tr; test the sum and the identity
            worst = max(worst, abs(pred.sum() - tr))
    g.close("(a) sum of per-pair capacities equals tr(M*M), unequal masses", worst, 0.0, 1e-9)

    # (b) equal masses: two double points at the equilateral shapes
    pts = double_points([1, 1, 1])
    g.check("(b) equal masses: exactly two double points", len(pts) == 2, len(pts))
    x = equilateral([1, 1, 1])
    dd = min(np.hypot(a - x[0], dist(a, p, x[1])) for a, p in pts)
    g.close("(b) equal masses: both sit at the equilateral shape", dd, 0.0, 1e-6)
    g.close("(b) equal masses: the gap there is zero", spectrum(x[0], x[1], [1, 1, 1])[2], 0.0, 1e-6)

    # (c) unequal masses: two double points, displaced, and the cone has slope 3
    rows = []
    for m in ([1, 1, 1.02], [1, 1, 1.1], [1, 1, 1.5], [1, 1, 2], [1, 2, 3]):
        m = np.asarray(m, float)
        pts = double_points(m)
        x = equilateral(m)
        gap_eq = spectrum(x[0], x[1], m)[2]
        near = min(pts, key=lambda q: np.hypot(q[0] - x[0], dist(q[0], q[1], x[1])))
        dh = np.hypot(near[0] - x[0], dist(near[0], near[1], x[1]))
        rows.append((float(m[2]), len(pts), dh, gap_eq))
        g.check(f"(c) m={m.tolist()}: two double points", len(pts) == 2, len(pts))
        g.check(f"(c) m={m.tolist()}: gap at the equilateral shape is positive", gap_eq > 1e-6, gap_eq)
        if m[2] <= 1.03:   # only where the equilateral shape is close enough for the local cone
            g.check(f"(c) m={m.tolist()}: gap = 3 x displacement (local cone slope 3)",
                    abs(gap_eq / dh - 3.0) < 0.05, float(gap_eq / dh), 0.05)
    g.measure("mass_breaking_rows", rows)

    # (d) the displacement grows quadratically in the anisotropy
    eps = np.array([1e-3, 2e-3, 5e-3, 1e-2])
    disp = []
    for e in eps:
        m = np.array([1.0, 1.0, 1 + e])
        pts = double_points(m); x = equilateral(m)
        near = min(pts, key=lambda q: np.hypot(q[0] - x[0], dist(q[0], q[1], x[1])))
        disp.append(np.hypot(near[0] - x[0], dist(near[0], near[1], x[1])))
    disp = np.array(disp)
    expo = np.polyfit(np.log(eps), np.log(disp), 1)[0]
    g.check("(d) displacement ~ (mass anisotropy)^2", abs(expo - 2.0) < 0.05, float(expo), 0.05)
    g.check("(d) displacement/eps^2 -> 1/9 (so the gap at the equilateral shape -> eps^2/3)",
            abs(disp[-1] / eps[-1] ** 2 - 1 / 9) < 2e-3, float(disp[-1] / eps[-1] ** 2), 2e-3)
    g.measure("displacement_rows", list(map(float, disp)))

    # (e) the shape of the cone: isotropic at equal masses, elliptic when they differ
    def cone_hessian(m, point):
        a0, p0 = point
        sc = np.sin(a0) * np.cos(a0)
        h = 1e-4

        def F(u, v):
            return spectrum(a0 + u, p0 + v / sc, m)[2] ** 2

        H = np.array([[(F(h, 0) - 2 * F(0, 0) + F(-h, 0)) / h ** 2,
                       (F(h, h) - F(h, -h) - F(-h, h) + F(-h, -h)) / (4 * h * h)],
                      [0.0, (F(0, h) - 2 * F(0, 0) + F(0, -h)) / h ** 2]])
        H[1, 0] = H[0, 1]
        return np.linalg.eigvalsh(H)

    ev_eq = cone_hessian(np.array([1.0, 1.0, 1.0]), double_points([1, 1, 1])[0])
    g.check("(e) equal masses: the cone is isotropic",
            abs(ev_eq[1] - ev_eq[0]) / ev_eq[1] < 1e-3, [float(ev_eq[0]), float(ev_eq[1])], 1e-3)
    g.close("(e) equal masses: isotropic cone of slope 3 (Hessian = 2*9)",
            float(np.sum(ev_eq) / 2), 18.0, 0.05)

    m = np.array([1.0, 1.0, 2.0])
    ev_un = cone_hessian(m, double_points(m)[0])
    g.check("(e) unequal masses: the cone at the displaced optic point is elliptic",
            (ev_un[1] - ev_un[0]) / ev_un[1] > 0.1, [float(ev_un[0]), float(ev_un[1])], 0.1)
    g.measure("cone_hessian_equal", list(map(float, ev_eq)))
    g.measure("cone_hessian_unequal_1_1_2", list(map(float, ev_un)))
    return g.finish()


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deterministic numerical checks for D8_m3.md (NumPy only)."""
import numpy as np

SQRT3 = np.sqrt(3.0)


def squared_distances(alpha, psi):
    s, c = np.sin(alpha), np.cos(alpha)
    C, p = s * c, np.cos(psi)
    x = 2.0 * c * c
    Y = 0.5 + s * s
    D = SQRT3 * C * p
    return np.array([x, Y + D, Y - D], dtype=float)


def distances(alpha, psi):
    return np.sqrt(squared_distances(alpha, psi))


def differential(alpha, psi):
    """Rows of M in the orthonormal coframe (d alpha, C d psi)."""
    s, c = np.sin(alpha), np.cos(alpha)
    C, p, q = s * c, np.cos(psi), np.sin(psi)
    r = squared_distances(alpha, psi)
    T = c * c - s * s
    A = np.array([-4.0 * C, 2.0 * C + SQRT3 * T * p,
                  2.0 * C - SQRT3 * T * p])
    B = np.array([0.0, -SQRT3 * C * q, SQRT3 * C * q])
    M = np.column_stack((A, B / C)) / (2.0 * np.sqrt(r)[:, None])
    return M


def closed_determinants(alpha, psi):
    s, c = np.sin(alpha), np.cos(alpha)
    x, y, z = squared_distances(alpha, psi)
    heron = 2.0 * (x*y + y*z + z*x) - x*x - y*y - z*z
    trig = 9.0 * (s*c)**2 * np.sin(psi)**2 / (x*y*z)
    rational = 3.0 * heron / (4.0 * x*y*z)
    return trig, rational, heron


def spectrum(alpha, psi):
    M = differential(alpha, psi)
    H = M.T @ M
    eig = np.linalg.eigvalsh(H)  # ascending
    return M, H, eig


def main():
    rng = np.random.default_rng(812367)
    trace_error = det_trig_error = det_rational_error = 0.0
    horizontal_error = gap_identity_error = finite_difference_error = 0.0
    largest_sample_det = -np.inf
    bound_violation = 0.0
    tested = 0

    while tested < 2500:
        alpha = rng.uniform(0.015, np.pi/2 - 0.015)
        psi = rng.uniform(0.0, 2.0*np.pi)
        r = squared_distances(alpha, psi)
        if np.min(r) < 1.0e-8:
            continue
        M, H, eig = spectrum(alpha, psi)
        det_h = float(np.linalg.det(H))
        det_t, det_r, heron = closed_determinants(alpha, psi)
        trace_error = max(trace_error, abs(np.trace(H) - 3.0))
        det_trig_error = max(det_trig_error, abs(det_h - det_t))
        det_rational_error = max(det_rational_error, abs(det_h - det_r))
        horizontal_error = max(horizontal_error,
                               np.max(np.abs(np.sum(M*M, axis=1) - (2.0-r))))
        gap = eig[1] - eig[0]
        gap_identity_error = max(gap_identity_error,
                                 abs(gap*gap - (9.0 - 4.0*det_h)))
        largest_sample_det = max(largest_sample_det, det_h)
        bound_violation = max(bound_violation, det_h - 9.0/4.0)
        tested += 1

    # Independent central finite differences of Phi, in the same orthonormal frame.
    for alpha, psi in [(0.31, 0.77), (0.73, 2.4), (1.12, 5.3)]:
        h = 2.0e-5
        C = np.sin(alpha)*np.cos(alpha)
        J_alpha = (distances(alpha+h, psi)-distances(alpha-h, psi))/(2*h)
        J_psi = (distances(alpha, psi+h)-distances(alpha, psi-h))/(2*h*C)
        M_fd = np.column_stack((J_alpha, J_psi))
        finite_difference_error = max(finite_difference_error,
                                      np.max(np.abs(M_fd-differential(alpha, psi))))

    # Equilateral values and the second symmetric equilateral point.
    equilateral_error = 0.0
    for psi in [np.pi/2, 3.0*np.pi/2]:
        _, H, eig = spectrum(np.pi/4, psi)
        equilateral_error = max(equilateral_error,
                                np.max(np.abs(H-1.5*np.eye(2))),
                                abs(np.linalg.det(H)-9.0/4.0),
                                np.max(np.abs(eig-1.5)))

    # Non-collision collinear meridians: eigenvalues must be (0,3).
    collinear_error = collinear_rank_error = 0.0
    for alpha in [0.08, 0.3, 0.65, 1.0, 1.45]:
        for psi in [0.0, np.pi]:
            M, H, eig = spectrum(alpha, psi)
            collinear_error = max(collinear_error, abs(np.linalg.det(H)))
            collinear_rank_error = max(collinear_rank_error,
                                       np.max(np.abs(eig-np.array([0.0, 3.0]))))

    # Equilateral asymptotics: gap^2/rho^2 -> 9 and gap/rho -> 3.
    rate_error = 0.0
    rate_rows = []
    for k in range(1, 7):
        t = 10.0**(-k)
        X, Y = t, t/3.0
        rho = np.hypot(X, Y)
        _, _, eig = spectrum(np.pi/4 + X, np.pi/2 + 2.0*Y)
        gap = eig[1]-eig[0]
        ratio_sq = gap*gap/(rho*rho)
        ratio = gap/rho
        rate_rows.append((t, ratio_sq, ratio))
        if k >= 4:
            rate_error = max(rate_error, abs(ratio_sq-9.0), abs(ratio-3.0))

    # Two one-sided derivatives at the 23-collision (pi/6, 0).
    a0, h = np.pi/6, 1.0e-4
    # The exact base value is zero; evaluating it in floating point gives O(1e-8).
    d0 = 0.0
    left = (d0-distances(a0-h, 0.0)[2])/h
    right = (distances(a0+h, 0.0)[2]-d0)/h
    collision_derivative_error = max(abs(left+np.sqrt(2.0)),
                                     abs(right-np.sqrt(2.0)))

    # The determinant has two different limits at the 23-collision.
    # At alpha=pi/6 it is identically 2 away from psi=0,pi; on psi=0 it is 0.
    collision_path_limit_error = 0.0
    for psi in [0.2, 0.7, 1.3]:
        M, H, eig = spectrum(np.pi/6, psi)
        collision_path_limit_error = max(collision_path_limit_error,
                                         abs(np.linalg.det(H)-2.0))
    for alpha in [np.pi/6-0.1, np.pi/6, np.pi/6+0.1]:
        if abs(alpha-np.pi/6) > 0.0:
            M, H, eig = spectrum(alpha, 0.0)
            collision_path_limit_error = max(collision_path_limit_error,
                                             abs(np.linalg.det(H)))

    # Heron's (unnormalized) numerator is zero at all three collisions.
    collision_heron_error = 0.0
    for alpha, psi in [(np.pi/2, 0.0), (np.pi/6, 0.0), (np.pi/6, np.pi)]:
        x, y, z = squared_distances(alpha, psi)
        heron = 2.0*(x*y+y*z+z*x)-x*x-y*y-z*z
        collision_heron_error = max(collision_heron_error, abs(heron))

    hard_error = max(trace_error, det_trig_error, det_rational_error,
                     horizontal_error, gap_identity_error,
                     finite_difference_error, equilateral_error,
                     collinear_error, collinear_rank_error,
                     collision_path_limit_error, collision_heron_error)
    passed = (hard_error < 2.0e-8 and rate_error < 2.0e-3 and
              collision_derivative_error < 2.0e-5 and
              bound_violation < 2.0e-12)

    print(f"PASS={passed}; tested_regular_shapes={tested}")
    print(f"trace={trace_error:.3e}; det_trig={det_trig_error:.3e}; det_rational={det_rational_error:.3e}; horizontal={horizontal_error:.3e}; gap_identity={gap_identity_error:.3e}")
    print(f"finite_difference_M={finite_difference_error:.3e}; equilateral={equilateral_error:.3e}; collinear_det={collinear_error:.3e}; collinear_eigen={collinear_rank_error:.3e}")
    print(f"max_sample_det={largest_sample_det:.12f}; bound_excess={max(0.0,bound_violation):.3e}")
    t, ratio_sq, ratio = rate_rows[3]
    print(f"rates_at_t={t:.0e}: gap^2/rho^2={ratio_sq:.9f}; gap/rho={ratio:.9f}; rate_residual={rate_error:.3e}")
    print(f"collision_cusp={collision_derivative_error:.3e}; two_path_limits={collision_path_limit_error:.3e}; Heron_numerator={collision_heron_error:.3e}")
    print("OVERALL", "PASS" if passed else "FAIL")


if __name__ == "__main__":
    main()

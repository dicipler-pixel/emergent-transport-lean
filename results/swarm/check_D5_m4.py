import numpy as np

np.set_printoptions(precision=6, suppress=True)
I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)
P4_exact = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
failures = []
max_residual = 0.0


def record(name, residual, tolerance):
    global max_residual
    residual = float(residual)
    max_residual = max(max_residual, residual)
    ok = bool(np.isfinite(residual) and residual <= tolerance)
    if not ok:
        failures.append(name)
    print(f"{'PASS' if ok else 'FAIL'} {name:44s} residual={residual:.3e} tolerance={tolerance:.1e}")


def B(t):
    return np.array([[0.0, 1.0], [t, 0.0]], dtype=complex)


def RB(z, t):
    return (z * I2 + B(t)) / (z * z - t)


def A4(t):
    out = np.zeros((4, 4), dtype=complex)
    out[:2, :2] = B(t)
    out[2, 2] = 3.0 + t
    out[3, 3] = 4.0 - t
    return out


def A4dot():
    out = np.zeros((4, 4), dtype=complex)
    out[1, 0] = 1.0
    out[2, 2] = 1.0
    out[3, 3] = -1.0
    return out


def R4(z, t):
    out = np.zeros((4, 4), dtype=complex)
    out[:2, :2] = RB(z, t)
    out[2, 2] = 1.0 / (z - 3.0 - t)
    out[3, 3] = 1.0 / (z - 4.0 + t)
    return out


# Trapezoidal contour integral on |z|=1. The factor z is dz/(i*z*dtheta).
theta = 2.0 * np.pi * np.arange(256) / 256.0
zgrid = np.exp(1j * theta)

# The unperturbed matrix is a nonzero nilpotent Jordan block.
B0 = B(0.0)
record("Jordan EP: B(0) is nonzero", np.linalg.norm(B0, 2) - 1.0, 1e-14)
record("Jordan EP: B(0)^2=0", np.linalg.norm(B0 @ B0, np.inf), 1e-14)

for t in [1e-2, -1e-2, 1e-4, 1e-4 + 3e-5j]:
    t = complex(t)
    r = abs(t)
    s = np.sqrt(np.complex128(t))
    Bt = B(t)
    vp = np.array([1.0, s], dtype=complex)
    vm = np.array([1.0, -s], dtype=complex)
    up = vp / np.sqrt(1.0 + r)
    um = vm / np.sqrt(1.0 + r)
    wp = 0.5 * np.array([1.0, 1.0 / s], dtype=complex)
    wm = 0.5 * np.array([1.0, -1.0 / s], dtype=complex)
    V = np.column_stack((vp, vm))
    Pp = np.outer(vp, wp)
    Pm = np.outer(vm, wm)

    eig_res = max(np.linalg.norm(Bt @ vp - s * vp, np.inf),
                  np.linalg.norm(Bt @ vm + s * vm, np.inf))
    dual_res = max(np.linalg.norm(wp @ Bt - s * wp, np.inf),
                   np.linalg.norm(wm @ Bt + s * wm, np.inf),
                   abs(wp @ vp - 1.0), abs(wm @ vm - 1.0),
                   abs(wp @ vm), abs(wm @ vp))
    record(f"eigen/dual equations t={t}", max(eig_res, dual_res), 2e-13)

    unit_res = max(abs(np.linalg.norm(up) - 1.0), abs(np.linalg.norm(um) - 1.0))
    coalescence_res = abs(np.linalg.norm(up - um) - 2.0 * np.sqrt(r) / np.sqrt(1.0 + r))
    overlap_res = abs(np.vdot(up, um) - (1.0 - r) / (1.0 + r))
    puiseux_res = abs(abs(s) / np.sqrt(r) - 1.0)
    record(f"coalescence/Puiseux rates t={t}",
           max(unit_res, coalescence_res, overlap_res, puiseux_res), 2e-13)

    cond_res = abs(np.linalg.cond(V, 2) - r ** -0.5) * np.sqrt(r)
    p_norm_formula = (1.0 + r) / (2.0 * np.sqrt(r))
    p_norm_res = max(abs(np.linalg.norm(Pp, 2) - p_norm_formula),
                     abs(np.linalg.norm(Pm, 2) - p_norm_formula)) * np.sqrt(r)
    p_sum_res = np.linalg.norm(Pp + Pm - I2, np.inf)
    record(f"divergence and P++P-=I t={t}",
           max(cond_res, p_norm_res, p_sum_res), 5e-11)

# Contour integration includes the EP itself and both real/complex nearby values.
for t in [0.0, 1e-4, -1e-4, 1e-4 + 3e-5j]:
    t = complex(t)
    Pnum = np.zeros((2, 2), dtype=complex)
    for z in zgrid:
        Pnum += z * RB(z, t)
    Pnum /= len(zgrid)
    record(f"pair Riesz projector=I t={t}", np.linalg.norm(Pnum - I2, np.inf), 2e-13)

# The block family has a uniform gap gamma=9/4 for |t|<=1/4.
for t in [-0.25, -0.01, 0.0, 0.01, 0.25]:
    t = complex(t)
    s = np.sqrt(np.complex128(t))
    ep_spectrum = np.array([s, -s])
    other_spectrum = np.array([3.0 + t, 4.0 - t])
    gap = np.min(np.abs(ep_spectrum[:, None] - other_spectrum[None, :]))
    record(f"uniform gap gamma=9/4 t={t}", max(0.0, 9.0 / 4.0 - gap), 2e-14)

for t in [0.0, -0.2, 0.2, 1e-4 + 3e-5j]:
    t = complex(t)
    Pnum = np.zeros((4, 4), dtype=complex)
    Pdotnum = np.zeros((4, 4), dtype=complex)
    for z in zgrid:
        Rz = R4(z, t)
        Pnum += z * Rz
        Pdotnum += z * (Rz @ A4dot() @ Rz)
    Pnum /= len(zgrid)
    Pdotnum /= len(zgrid)
    direct_sum_res = np.linalg.norm(A4(t) @ P4_exact - P4_exact @ A4(t), np.inf)
    record(f"4x4 Riesz/direct sum t={t}",
           max(np.linalg.norm(Pnum - P4_exact, np.inf), direct_sum_res), 3e-13)
    record(f"4x4 contour derivative=0 t={t}", np.linalg.norm(Pdotnum, np.inf), 3e-13)

if failures:
    print(f"FAIL max_residual={max_residual:.3e}; failed_checks={','.join(failures)}")
    raise SystemExit(1)
print(f"PASS max_residual={max_residual:.3e}; all_checks={31}")

"""Deterministic checks for D3; exact projector derivatives at (x,y)=(0,0)."""
import numpy as np

residuals = []
records = {}

for k in (1, 2, 4):
    n = k + 1
    # P = |v><v| + I_fixed, v=(1,x+iy)/sqrt(1+x^2+y^2).
    # At the origin U is an orthonormal frame and dU=Z is transverse.
    U = np.zeros((n, k), dtype=complex)
    U[0, 0] = 1.0
    for col in range(1, k):
        U[col + 1, col] = 1.0
    P = U @ U.conj().T
    Z = [np.zeros((n, k), dtype=complex) for _ in range(2)]
    Z[0][1, 0] = 1.0
    Z[1][1, 0] = 1j
    dP = [z @ U.conj().T + U @ z.conj().T for z in Z]

    # Literal Q and the repaired, standard projected QGT.
    Q_literal = np.array([[np.trace(a @ b) for b in dP] for a in dP])
    Q_projected = np.array([[np.trace(P @ a @ b) for b in dP] for a in dP])
    Q_frame = np.array([[np.trace(a.conj().T @ b) for b in Z] for a in Z])
    Q_expected = np.array([[1.0, 1.0j], [-1.0j, 1.0]])

    residuals += [
        np.max(np.abs(Q_literal.imag)),
        np.max(np.abs(Q_literal - Q_literal.T)),
        np.max(np.abs(Q_literal - 2 * Q_projected.real)),
        np.max(np.abs(Q_projected - Q_frame)),
        np.max(np.abs(Q_projected - Q_expected)),
    ]

    g = Q_projected.real
    scale = np.sqrt(g[0, 0] * g[1, 1])
    sharp_im_residual = abs(Q_projected[0, 1].imag) - scale

    # A_mu=i<v,d_mu v>, F_xy=d_x A_y-d_y A_x.
    dv = [np.array([0.0, 1.0], dtype=complex),
          np.array([0.0, 1.0j], dtype=complex)]
    berry = 1j * (np.vdot(dv[0], dv[1]) - np.vdot(dv[1], dv[0]))
    assert abs(berry.imag) < 1e-14
    berry = berry.real
    curvature_identity_residual = berry + 2 * Q_projected[0, 1].imag
    sharp_curvature_residual = abs(berry) - 2 * scale
    residuals += [abs(sharp_im_residual), abs(curvature_identity_residual),
                  abs(sharp_curvature_residual)]

    if k == 1:
        records["literal_Q"] = Q_literal
        records["literal_constant2_equality_residual"] = (
            abs(Q_literal[0, 1].imag)
            - 2 * np.sqrt(Q_literal[0, 0].real * Q_literal[1, 1].real)
        )
        # This nonzero value disproves nondegenerate sharpness of constant 2
        # for Im(Q_projected), although the loose inequality remains valid.
        records["projected_ImQ_constant2_equality_residual"] = (
            abs(Q_projected[0, 1].imag) - 2 * scale
        )

# Also check the frame identities away from parallel gauge.  The tangent
# condition dU=U*C+Z uses C skew-Hermitian and Z transverse, but is otherwise generic.
rng = np.random.default_rng(202603)
n, k = 5, 3
U, _ = np.linalg.qr(rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)))
P = U @ U.conj().T
R = np.eye(n) - P
Z, dU = [], []
for _ in range(2):
    C = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k))
    C = (C - C.conj().T) / 2
    z = R @ (rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k)))
    Z.append(z)
    dU.append(U @ C + z)
dP = [d @ U.conj().T + U @ d.conj().T for d in dU]
Q_projected = np.array([[np.trace(P @ a @ b) for b in dP] for a in dP])
Q_frame = np.array([[np.trace(a.conj().T @ b) for b in Z] for a in Z])
Q_literal = np.array([[np.trace(a @ b) for b in dP] for a in dP])
berry = 1j * (np.trace(dU[0].conj().T @ dU[1])
              - np.trace(dU[1].conj().T @ dU[0]))
g = Q_projected.real
bound_slack = np.sqrt(g[0, 0] * g[1, 1]) - abs(Q_projected[0, 1].imag)
residuals += [np.max(np.abs(Q_projected - Q_frame)),
              np.max(np.abs(Q_literal - 2 * Q_projected.real)),
              abs(berry.imag), abs(berry.real + 2 * Q_projected[0, 1].imag),
              max(0.0, -bound_slack)]

max_residual = float(np.max(residuals))
passed = max_residual < 1e-12
print("PASS" if passed else "FAIL")
print(f"max_residual = {max_residual:.3e}")
print(f"literal_ImQ_max_abs = {np.max(np.abs(records['literal_Q'].imag)):.3e}")
print(f"sharp_rank_independent_residual = {max_residual:.3e}")
print("literal_constant2_equality_residual = "
      f"{records['literal_constant2_equality_residual']:.3e} (nonzero strict gap)")
print("projected_ImQ_constant2_equality_residual = "
      f"{records['projected_ImQ_constant2_equality_residual']:.3e} (nonzero strict gap)")
raise SystemExit(0 if passed else 1)

"""Deterministic numerical check for D1 (NumPy only)."""
import numpy as np


def redistribution(Omega, P):
    Q = np.eye(P.shape[0], dtype=P.dtype) - P
    return P @ Omega @ Q + Q @ Omega @ P


rng = np.random.default_rng(20261123)
n = 6
P = np.diag([1.0, 1.0, 0.0, 0.0, 0.0, 0.0]).astype(complex)
Q = np.eye(n, dtype=complex) - P
B = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
H = B + B.conj().T  # generic self-adjoint matrix
D = P @ H @ P + Q @ H @ Q  # self-adjoint block-diagonal matrix
Omega = B  # arbitrary, in particular non-self-adjoint, matrix

residuals = {}
FH = redistribution(H, P)
A = P @ H @ Q
C = H @ P - P @ H
norm_F2 = np.linalg.norm(FH, "fro") ** 2
norm_A2 = np.linalg.norm(A, "fro") ** 2
norm_C2 = np.linalg.norm(C, "fro") ** 2
trace_value = np.trace(P @ H @ Q @ H)
residuals["trace, arbitrary Omega"] = abs(np.trace(redistribution(Omega, P)))
residuals["F norm squared"] = abs(norm_F2 - 2.0 * norm_A2)
residuals["corrected commutator norm squared"] = abs(norm_F2 - norm_C2)
residuals["trace identity"] = abs(trace_value - norm_A2)
residuals["trace imaginary part"] = abs(trace_value.imag)

# Numerical instances of the three-way equivalence in both directions.
off_diagonal = H - D
nondegenerate = (
    np.linalg.norm(FH, "fro") > 1e-10
    and np.linalg.norm(C, "fro") > 1e-10
    and np.linalg.norm(off_diagonal, "fro") > 1e-10
)
FD = redistribution(D, P)
CD = D @ P - P @ D
block_diagonal_residual = max(
    np.linalg.norm(FD, "fro"), np.linalg.norm(CD, "fro")
)
residuals["block-diagonal equivalence"] = block_diagonal_residual

# The requested two-dimensional non-normal example.
N = np.array([[0.0, 1.0], [0.0, 0.0]])
P2 = np.diag([1.0, 0.0])
FN = redistribution(N, P2)
nonnormality = np.linalg.norm(N @ N.T - N.T @ N, "fro")
example_ok = (
    nonnormality > 1.0
    and np.linalg.norm(FN, "fro") > 0.5
    and abs(np.trace(FN)) < 1e-14
)

# A self-adjoint counterexample to the proposed factor 1/2 on the commutator.
sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
Q2 = np.eye(2) - P2
Fsigma = redistribution(sigma_x, P2)
Csigma = sigma_x @ P2 - P2 @ sigma_x
Asigma = P2 @ sigma_x @ Q2
Fsigma2 = np.linalg.norm(Fsigma, "fro") ** 2
Csigma2 = np.linalg.norm(Csigma, "fro") ** 2
Asigma2 = np.linalg.norm(Asigma, "fro") ** 2
original_discrepancy = abs(Fsigma2 - 0.5 * Csigma2)
residuals["counterexample corrected norm identity"] = max(
    abs(Fsigma2 - 2.0 * Asigma2), abs(Fsigma2 - Csigma2)
)
half_factor_counterexample_ok = (
    abs(Fsigma2 - 2.0) < 1e-14
    and abs(Csigma2 - 2.0) < 1e-14
    and original_discrepancy > 0.5
)

max_residual = max(residuals.values())
passed = (
    max_residual < 1e-11
    and trace_value.real >= -1e-11
    and nondegenerate
    and example_ok
    and half_factor_counterexample_ok
)
for name, value in residuals.items():
    print(f"{name}: {value:.3e}")
print(f"Tr(P H Q H) real part (must be nonnegative): {trace_value.real:.6f}")
print(f"example nonnormality ||N N* - N* N||_F: {nonnormality:.3e}")
print(f"sigma_x discrepancy for the false half-factor: {original_discrepancy:.3e}")
print(f"{'PASS' if passed else 'FAIL'}; maximum numerical residual: {max_residual:.3e}")

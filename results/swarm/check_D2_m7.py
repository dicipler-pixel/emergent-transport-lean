#!/usr/bin/env python3
"""Deterministic checks for D2; NumPy only."""
import numpy as np


def spin_data(theta, phi):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    ephi = np.exp(1j * phi)
    v = np.array([c, ephi * s], dtype=complex)
    dv = [
        np.array([-s / 2, ephi * c / 2], dtype=complex),
        np.array([0, 1j * ephi * s], dtype=complex),
    ]
    P = np.outer(v, v.conj())
    D = [np.outer(d, v.conj()) + np.outer(v, d.conj()) for d in dv]
    Q0 = np.array([[np.trace(D[a] @ D[b]) for b in range(2)] for a in range(2)])
    Q = np.array([[np.trace(P @ D[a] @ D[b]) for b in range(2)] for a in range(2)])
    W = [(np.eye(2) - P) @ d for d in dv]
    QW = np.array([[np.vdot(W[a], W[b]) for b in range(2)] for a in range(2)])
    comm = D[0] @ D[1] - D[1] @ D[0]
    F = 1j * np.trace(P @ comm)
    return v, P, D, Q0, Q, QW, F


def rank_copies(theta, phi, k):
    v, P1, D1, _, _, _, _ = spin_data(theta, phi)
    I = np.eye(k)
    P = np.kron(I, P1)
    D = [np.kron(I, d) for d in D1]
    Q = np.array([[np.trace(P @ D[a] @ D[b]) for b in range(2)] for a in range(2)])
    F = 1j * np.trace(P @ (D[0] @ D[1] - D[1] @ D[0]))
    return Q, F


def riesz_checks():
    E11 = np.array([[1, 0], [0, 0]], dtype=complex)
    E12 = np.array([[0, 1], [0, 0]], dtype=complex)
    E21 = np.array([[0, 0], [1, 0]], dtype=complex)
    D = [E21, E12]
    Q0R = np.array([[np.trace(D[a] @ D[b]) for b in range(2)] for a in range(2)])
    QR = np.array([[np.trace(E11 @ D[a] @ D[b]) for b in range(2)] for a in range(2)])
    DC = [E21, 1j * E12]
    Q0C = np.array([[np.trace(DC[a] @ DC[b]) for b in range(2)] for a in range(2)])
    v, w = 0.2, 0.1
    PR = np.array([[1, w], [v, v * w]], dtype=complex) / (1 + v * w)
    PC = np.array([[1, 1j * w], [v, 1j * v * w]], dtype=complex) / (1 + 1j * v * w)
    return Q0R, QR, Q0C, PR, PC


def main():
    residuals = []
    hard_failures = []
    theta, phi = 0.8, 0.3
    v, P, D, Q0, Q, QW, F = spin_data(theta, phi)
    Q0_target = np.diag([0.5, 0.5 * np.sin(theta) ** 2])
    Q_target = np.array([
        [0.25, 0.25j * np.sin(theta)],
        [-0.25j * np.sin(theta), 0.25 * np.sin(theta) ** 2],
    ])
    residuals.extend([
        np.linalg.norm(P @ P - P),
        np.linalg.norm(P - P.conj().T),
        abs(np.vdot(v, v) - 1),
        np.linalg.norm(Q0 - Q0_target),
        np.linalg.norm(Q - Q_target),
        np.linalg.norm(QW - Q),
        np.linalg.norm(Q0 - 2 * Q.real),
        np.linalg.norm(Q0 - Q0.conj().T),
        np.linalg.norm(Q - Q.conj().T),
        np.linalg.norm(np.imag(Q0)),
        abs(F + 0.5 * np.sin(theta)),
        abs(F + 2 * Q[0, 1].imag),
    ])
    min_eig_Q0 = np.linalg.eigvalsh(Q0)[0]
    min_eig_Q = np.linalg.eigvalsh(Q)[0]
    residuals.extend([max(0.0, -min_eig_Q0), max(0.0, -min_eig_Q)])
    if abs(F) < 0.1:  # the original imaginary-part claim must really fail here
        hard_failures.append("spin Berry curvature unexpectedly vanished")

    Q3, F3 = rank_copies(theta, phi, 3)
    residuals.extend([np.linalg.norm(Q3 - 3 * Q), abs(F3 - 3 * F)])

    # Gauss--Legendre quadrature of the spherical Berry curvature period.
    nodes, weights = np.polynomial.legendre.leggauss(32)
    thetas = (nodes + 1) * np.pi / 2
    weights = weights * np.pi / 2
    vals = np.array([spin_data(t, 0.71)[6] for t in thetas])
    period = 2 * np.pi * np.sum(weights * vals)
    period_residual = abs(period + 2 * np.pi)
    residuals.append(period_residual)

    Q0R, QR, Q0C, PR, PC = riesz_checks()
    residuals.extend([
        np.linalg.norm(Q0R - np.array([[0, 1], [1, 0]])),
        np.linalg.norm(QR - np.array([[0, 0], [1, 0]])),
        np.linalg.norm(Q0C - np.array([[0, 1j], [1j, 0]])),
        np.linalg.norm(PR @ PR - PR),
        np.linalg.norm(PC @ PC - PC),
    ])
    riesz_min_eig = np.linalg.eigvalsh(Q0R.real)[0]
    riesz_hermitian_defect = np.linalg.norm(QR - QR.conj().T)
    riesz_complex_defect = np.linalg.norm(Q0C - Q0C.conj().T)
    if riesz_min_eig >= -0.5:
        hard_failures.append("Riesz real-part counterexample is not indefinite")
    if riesz_hermitian_defect < 0.5 or riesz_complex_defect < 0.5:
        hard_failures.append("Riesz Hermiticity counterexample failed")
    if min(np.linalg.norm(PR - PR.conj().T), np.linalg.norm(PC - PC.conj().T)) < 0.1:
        hard_failures.append("Riesz example unexpectedly orthogonal")

    max_residual = float(max(residuals))
    passed = max_residual < 2e-12 and not hard_failures
    print(f"{'PASS' if passed else 'FAIL'} max_residual={max_residual:.3e}")
    print(f"spin_min_eigenvalues Qcirc={min_eig_Q0:.3e} Qcorrected={min_eig_Q:.3e}")
    print(f"spin_original_imag_residual={np.linalg.norm(np.imag(Q0)):.3e} "
          f"nonzero_Berry_curvature={abs(F):.6f}")
    print(f"S2_period={period:.15f} period_over_2pi={period / (2 * np.pi):.15f} "
          f"period_residual={period_residual:.3e}")
    print(f"rank3_scaling_residual={max(np.linalg.norm(Q3 - 3 * Q), abs(F3 - 3 * F)):.3e}")
    print(f"Riesz_min_eig_Re_Qcirc={riesz_min_eig:.6f} "
          f"Riesz_Qcorrected_Hermitian_defect={riesz_hermitian_defect:.6f} "
          f"Riesz_Qcirc_Hermitian_defect={riesz_complex_defect:.6f}")
    if hard_failures:
        print("hard_failures=" + "; ".join(hard_failures))


if __name__ == "__main__":
    main()

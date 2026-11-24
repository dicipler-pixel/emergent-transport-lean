"""Deterministic numpy check for D6 (integer winding versus spectral flow)."""
import numpy as np

S1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
S2 = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
S3 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def hamiltonian(a, b, c):
    return a * S1 + b * S2 + c * S3


def winding(z):
    """Argument sum on a closed polygon; no differentiation is used."""
    increments = np.angle(np.roll(z, -1) * np.conj(z))
    return np.sum(increments) / (2.0 * np.pi)


def spectrum(z, c):
    return np.array([
        np.linalg.eigvalsh(hamiltonian(z[k].real, z[k].imag, c[k]))
        for k in range(len(z))
    ])


def net_spectral_flow(eigenvalues, level):
    """Signed branch crossings, including the endpoint-identification segment."""
    shifted = eigenvalues - level
    following = np.roll(shifted, -1, axis=0)
    upward = (shifted < 0.0) & (following >= 0.0)
    downward = (shifted > 0.0) & (following <= 0.0)
    return int(np.sum(upward) - np.sum(downward))


def berry_phase(z):
    """Gauge-invariant negative-band Berry phase on a c=0 loop."""
    vectors = []
    for value in z:
        h = hamiltonian(value.real, value.imag, 0.0)
        _, eigenvectors = np.linalg.eigh(h)
        vectors.append(eigenvectors[:, 0])
    vectors = np.array(vectors)
    overlaps = np.sum(np.conj(vectors) * np.roll(vectors, -1, axis=0), axis=1)
    return -float(np.sum(np.angle(overlaps)))


def main():
    n = 512
    t = 2.0 * np.pi * np.arange(n) / n
    failures = []

    # The principal counterexample: winding one, identically zero spectral flow.
    z = np.exp(1.0j * t)
    c = np.zeros(n)
    eig = spectrum(z, c)
    w_float = winding(z)
    w = int(np.rint(w_float))
    sf = net_spectral_flow(eig, 0.0)
    level_gap = float(np.min(np.abs(eig)))
    winding_residual = abs(w_float - 1.0)
    if winding_residual > 1.0e-12 or w != 1 or sf != 0 or abs(level_gap - 1.0) > 1.0e-12:
        failures.append("winding/spectral-flow counterexample")
    print("principal loop: winding = %d, spectral_flow = %d, level_gap = %.16g" %
          (w, sf, level_gap))
    print("winding residual = %.3e; |winding-spectral_flow| = %.3e" %
          (winding_residual, abs(w - sf)))

    # Signed Berry formula gamma_- = -pi*w for c=0, including even/odd cases.
    berry_residual = 0.0
    holonomy_residual = 0.0
    for degree in (-2, -1, 0, 1, 2):
        z_degree = np.exp(1.0j * degree * t)
        degree_float = winding(z_degree)
        gamma = berry_phase(z_degree)
        berry_residual = max(berry_residual, abs(degree_float - degree),
                             abs(gamma + np.pi * degree))
        holonomy_residual = max(
            holonomy_residual, abs(np.exp(1.0j * gamma) - (-1) ** degree))
        print("c=0, w = %+d: Berry phase = %+.16g, holonomy error = %.3e" %
              (degree, gamma, abs(np.exp(1.0j * gamma) - (-1) ** degree)))
    if berry_residual > 2.0e-11 or holonomy_residual > 2.0e-11:
        failures.append("Berry phase or holonomy")
    print("Berry identity residual = %.3e; holonomy residual = %.3e" %
          (berry_residual, holonomy_residual))

    # Nonzero c and varying |z|: winding is still integral when z never vanishes.
    z_general = (1.1 + 0.2 * np.cos(3.0 * t)) * np.exp(1.0j * t)
    c_general = 0.35 * np.sin(2.0 * t) + 0.1
    general_w_float = winding(z_general)
    general_eig = spectrum(z_general, c_general)
    general_gap = float(np.min(np.abs(general_eig)))
    general_sf = net_spectral_flow(general_eig, 0.0)
    general_residual = abs(general_w_float - 1.0)
    if (general_residual > 1.0e-12 or general_gap <= 0.0 or general_sf != 0):
        failures.append("general nonzero-z loop")
    print("nonchiral loop: winding residual = %.3e, level_gap = %.16g, spectral_flow = %d" %
              (general_residual, general_gap, general_sf))

    # A gap at zero alone does not make the winding defined: z == 0, c == 1.
    constant_eig = np.linalg.eigvalsh(hamiltonian(0.0, 0.0, 1.0))
    constant_z_norm = abs(0.0 + 0.0j)
    if constant_z_norm != 0.0 or abs(np.min(np.abs(constant_eig)) - 1.0) > 1.0e-12:
        failures.append("undefined-winding counterexample")
    print("H=sigma_3 counterexample: |a+ib| = %.1f, level_gap = %.16g, winding undefined" %
          (constant_z_norm, np.min(np.abs(constant_eig))))

    # At a nonzero reference level, radius region is an additional invariant.
    inside = np.linalg.eigvalsh(hamiltonian(0.5, 0.0, 0.0))
    outside = np.linalg.eigvalsh(hamiltonian(2.0, 0.0, 0.0))
    if np.min(np.abs(inside - 1.0)) <= 0.0 or np.min(np.abs(outside - 1.0)) <= 0.0:
        failures.append("nonzero-level examples")
    print("level 1, w=0: radii 0.5 and 2.0 are separated by the forbidden radius 1.0")

    if failures:
        print("FAIL: " + "; ".join(failures))
        print("maximum numerical residual = %.3e" %
              max(winding_residual, berry_residual, holonomy_residual, general_residual))
        return 1
    print("PASS")
    print("maximum numerical residual = %.3e" %
          max(winding_residual, berry_residual, holonomy_residual, general_residual))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

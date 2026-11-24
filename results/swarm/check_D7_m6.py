import numpy as np


def normalise(raw, masses):
    raw = np.asarray(raw, dtype=float)
    masses = np.asarray(masses, dtype=float)
    total = masses.sum()
    centre = (masses[:, None] * raw).sum(axis=0) / total
    centred = raw - centre
    inertia = (masses[:, None] * centred * centred).sum()
    return centred / np.sqrt(inertia)


def residuals(raw, masses, equal_case=False):
    raw = np.asarray(raw, dtype=float)
    m = np.asarray(masses, dtype=float)
    n = len(m)
    total = m.sum()
    centre = (m[:, None] * raw).sum(axis=0)
    inertia_raw = (m[:, None] * raw * raw).sum()
    pair_inertia_raw = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            pair_inertia_raw += m[i] * m[j] * np.sum((raw[i] - raw[j]) ** 2)
    inertia_residual = abs(pair_inertia_raw - (total * inertia_raw - centre @ centre))

    r = normalise(raw, m)
    sqrt_m = np.sqrt(m)
    vertical = []
    for u in (np.tile([1.0, 0.0], (n, 1)),
              np.tile([0.0, 1.0], (n, 1)),
              np.column_stack((-r[:, 1], r[:, 0])), r):
        vertical.append((u * sqrt_m[:, None]).ravel())
    q, _ = np.linalg.qr(np.column_stack(vertical))
    radial = (r * sqrt_m[:, None]).ravel()

    lhs = 0.0
    distance_sq_sum = 0.0
    radial_sq_sum = 0.0
    horizontality = 0.0
    pair_inertia = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            displacement = r[i] - r[j]
            distance = np.linalg.norm(displacement)
            e = displacement / distance
            gradient = np.zeros((n, 2))
            gradient[i] = e / m[i]
            gradient[j] = -e / m[j]
            x = (gradient * sqrt_m[:, None]).ravel()
            horizontal = x - q @ (q.T @ x)
            lhs += horizontal @ horizontal
            horizontality = max(horizontality, np.linalg.norm(q.T @ horizontal))
            radial_sq_sum += (x @ radial) ** 2
            distance_sq_sum += distance ** 2
            pair_inertia += m[i] * m[j] * distance ** 2

    rhs = (n - 1) * np.sum(1.0 / m) - distance_sq_sum
    out = [inertia_residual, abs(lhs - rhs),
           abs(radial_sq_sum - distance_sq_sum),
           abs(pair_inertia - total), horizontality]
    if equal_case:
        out.append(abs(lhs - n * (n - 2)))
    return np.asarray(out), lhs


def main():
    cases = [
        ("unequal-N5", [[0.2, -0.4], [1.3, 0.7], [-0.8, 1.1],
                        [1.9, -1.2], [-1.5, -0.3]],
         [0.7, 1.1, 1.8, 0.45, 2.2], False),
        ("equal-N4", [[0.1, 0.2], [1.4, -0.3],
                      [-0.7, 1.1], [-1.2, -1.0]],
         [1.0, 1.0, 1.0, 1.0], True),
        ("equal-N2", [[-0.3, 0.8], [1.7, -0.2]], [1.0, 1.0], True),
    ]
    worst = 0.0
    for name, raw, masses, equal_case in cases:
        errors, lhs = residuals(raw, masses, equal_case)
        worst = max(worst, float(errors.max()))
        print(f"{name}: lhs={lhs:.15g}, residual={errors.max():.3e}")
    status = "PASS" if np.isfinite(worst) and worst < 1e-11 else "FAIL"
    print(f"{status} max_residual={worst:.3e}")


if __name__ == "__main__":
    main()

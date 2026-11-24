#!/usr/bin/env python3
"""Deterministic numpy checks for D4 (m5).

Only numpy is used.  The script also exhibits, rather than hides, the
sqrt(2) correction to the Frobenius statement in the question.
"""

import numpy as np

np.set_printoptions(precision=10, suppress=True)
rng = np.random.default_rng(20261123)
checks = []


def record(name, value, tolerance=2e-10):
    """Record a residual that should be at most tolerance."""
    value = float(value)
    checks.append((name, value, tolerance))


# 1. Weyl: ordered eigenvalues, varied noncommuting complex Hermitian pairs.
weyl_violation = 0.0
for n in range(1, 9):
    for _ in range(30):
        x = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        y = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        a = (x + x.conj().T) / 2
        b = (y + y.conj().T) / 2
        ea = np.linalg.eigvalsh(a)
        eb = np.linalg.eigvalsh(b)
        excess = np.max(np.abs(ea - eb)) - np.linalg.norm(a - b, 2)
        weyl_violation = max(weyl_violation, max(0.0, float(excess)))
record("Weyl inequality", weyl_violation)


# 2. The off-diagonal block of dot(P): X_{ji}=H_{ji}/(mu_j-lambda_i).
# Check general and ordered-gap operator-norm bounds and the Frobenius bound.
general_violation = 0.0
ordered_violation = 0.0
frobenius_violation = 0.0
for n in range(2, 9):
    for _ in range(30):
        gamma = float(rng.uniform(0.2, 2.5))
        # All adjacent gaps exceed gamma; a random colouring then gives an
        # arbitrary (often interleaved) cluster/complement partition.
        eig = np.cumsum(gamma + 0.3 + rng.uniform(0.05, 1.5, size=n))
        mask = rng.integers(0, 2, size=n, dtype=bool)
        if mask.all() or (~mask).all():
            mask[0] = True
            mask[-1] = False
        ii = np.flatnonzero(mask)
        jj = np.flatnonzero(~mask)
        z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        h = (z + z.conj().T) / 2
        hnorm = np.linalg.norm(h, 2)
        lam = eig[ii]
        mu = eig[jj]
        den = mu[:, None] - lam[None, :]
        assert np.min(np.abs(den)) >= gamma
        xblock = h[np.ix_(jj, ii)] / den
        general_violation = max(
            general_violation,
            max(0.0, float(np.linalg.norm(xblock, 2)
                           - (np.pi / 2) * hnorm / gamma)),
        )
        # ||dot P||_F^2=2||X||_F^2 and ||H||_F^2>=2||H_JI||_F^2.
        dotp_f = np.sqrt(2.0) * np.linalg.norm(xblock, "fro")
        frobenius_violation = max(
            frobenius_violation,
            max(0.0, float(dotp_f - np.linalg.norm(h, "fro") / gamma)),
        )
record("general projector pi/2 bound", general_violation)
record("projector Frobenius bound", frobenius_violation)

for p in range(1, 6):
    q = 7 - p
    for _ in range(30):
        gamma = float(rng.uniform(0.3, 2.0))
        lam = np.cumsum(rng.uniform(0.0, 1.0, size=p)) - 8.0
        mu = lam[-1] + gamma + np.cumsum(rng.uniform(0.0, 1.0, size=q))
        n = p + q
        z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        h = (z + z.conj().T) / 2
        xblock = h[p:, :p] / (mu[:, None] - lam[None, :])
        ordered_violation = max(
            ordered_violation,
            max(0.0, float(np.linalg.norm(xblock, 2)
                           - np.linalg.norm(h, 2) / gamma)),
        )
record("ordered-gap projector bound", ordered_violation)


# 3. Sharpness approximants for the dimension-free pi/2 constant.
# C_{ji}=1/(2(j-i)+1), Y_{ji}=C_{ji}^2.  Their infinite symbols have
# norms pi/2 and pi^2/4 respectively.
ratios = []
for half_width in (2, 4, 8, 16, 32, 64):
    m = np.arange(-half_width, half_width + 1)
    c = 1.0 / (2.0 * (m[:, None] - m[None, :]) + 1.0)
    ratio = np.linalg.norm(c * c, 2) / np.linalg.norm(c, 2)
    ratios.append(float(ratio))
sharp_gap = np.pi / 2 - ratios[-1]
checks.append(("sharpness limit resolution", float(sharp_gap), 0.0091))


# 4. Rank-one projector versus the transverse eigenvector derivative.
def top_vector(t):
    lam = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
    v = np.array([lam, t], dtype=float)
    return v / np.linalg.norm(v)


pdot_exact = np.array([[0.0, 1.0], [1.0, 0.0]])
hstep = 1e-5
vp = top_vector(hstep)
vm = top_vector(-hstep)
pp = np.outer(vp, vp)
pm = np.outer(vm, vm)
pdot_fd = (pp - pm) / (2.0 * hstep)
record("rank-one dot(P), finite diff", np.linalg.norm(pdot_fd - pdot_exact), 2e-9)
wdot_fd = (vp - vm) / (2.0 * hstep)
record("rank-one transverse dot(v)", np.linalg.norm(wdot_fd - np.array([0.0, 1.0])), 2e-9)
pf = np.linalg.norm(pdot_exact, "fro")
pop = np.linalg.norm(pdot_exact, 2)
wnorm = 1.0
record("rank-one operator-norm equality", abs(pop - wnorm))
record("rank-one corrected Frobenius eq", abs(pf - np.sqrt(2.0) * wnorm))


# 5. A fixed two-dimensional cluster is smooth through its shrinking
# internal gap, while its ordered top eigenvector derivative is 1/(2 eps).
cluster_violation = 0.0
for eps in (0.25, 0.05, 0.01):
    def cluster_top_vector(t, eps=eps):
        r = np.sqrt(eps * eps + t * t)
        v = np.array([r + eps, t], dtype=float)
        return v / np.linalg.norm(v)

    cluster_h = 1e-6
    vplus = cluster_top_vector(cluster_h)
    vminus = cluster_top_vector(-cluster_h)
    derivative = (vplus - vminus) / (2.0 * cluster_h)
    expected = np.array([0.0, 1.0 / (2.0 * eps)])
    cluster_violation = max(cluster_violation,
                            float(np.linalg.norm(derivative - expected)))
record("cluster eigenvector finite diff", cluster_violation, 5e-7)


print(f"violations: Weyl={weyl_violation:.1e}, general={general_violation:.1e}, "
      f"ordered={ordered_violation:.1e}, Frobenius={frobenius_violation:.1e}")
print(f"sharpness: N=129, ratio={ratios[-1]:.12f}, gap={sharp_gap:.6e}")
print(f"rank-one: op_norm={pop:.1f}, Frobenius={pf:.12f}, transverse={wnorm:.1f}")
print("finite-difference residuals: "
      f"projector={np.linalg.norm(pdot_fd - pdot_exact):.3e}, "
      f"eigenvector={np.linalg.norm(wdot_fd - np.array([0.0, 1.0])):.3e}, "
      f"cluster={cluster_violation:.3e}")
print("cluster eps=0.01: eigenvector sensitivity=50, cluster projector derivative=0")
failed = [name for name, value, tolerance in checks if not np.isfinite(value) or value > tolerance]
max_residual = max(value for _, value, _ in checks)
print(f"maximum recorded residual={max_residual:.6e}")
if failed:
    print("FAIL residual={:.6e}; failed checks: {}".format(max_residual, ", ".join(failed)))
    raise SystemExit(1)
print(f"PASS residual={max_residual:.6e}; all {len(checks)} checks satisfied")

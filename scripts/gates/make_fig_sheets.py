"""Figure 1 of the paper: the two sheets and the determinant, drawn from the gate G01."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from g01_shape_spectrum import spectrum

al = np.linspace(0.02, np.pi / 2 - 0.02, 400)
res = np.array([spectrum(a, np.pi / 2) for a in al])
det, gap = res[:, 1], res[:, 2]
s1, s2 = (3 + gap) / 2, (3 - gap) / 2

fig, ax = plt.subplots(1, 2, figsize=(7.4, 2.8))
ax[0].plot(al, s1, lw=1.5, label=r"$\sigma_1^2$")
ax[0].plot(al, s2, lw=1.5, label=r"$\sigma_2^2$")
ax[0].axhline(1.5, ls=":", lw=0.8, color="k")
ax[0].axvline(np.pi / 4, ls=":", lw=0.8, color="k")
ax[0].set_xlabel(r"$\alpha$  along the isosceles meridian $\psi=\pi/2$", fontsize=8)
ax[0].set_ylabel("squared singular values", fontsize=8)
ax[0].set_title(r"$\sigma_1^2+\sigma_2^2=3$ identically", fontsize=9)
ax[0].set_ylim(-0.15, 3.5)
ax[0].legend(fontsize=8, frameon=False, loc="center right")
ax[0].annotate("equilateral:\ngap closes", xy=(np.pi / 4, 1.5), xytext=(0.95, 0.55), fontsize=7,
               arrowprops=dict(arrowstyle="->", lw=0.6))
ax[0].annotate("collinear midpoint:\nrank drops", xy=(np.pi / 2 - 0.02, 2.95), xytext=(1.02, 3.02),
               fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))
ax[0].annotate("12-collision", xy=(0.06, 0.1), xytext=(0.12, 1.0), fontsize=7,
               arrowprops=dict(arrowstyle="->", lw=0.6))
ax[1].plot(al, det, lw=1.5, label=r"$\det M^*M=12A^2/(d_{12}^2d_{13}^2d_{23}^2)$")
ax[1].axhline(2.25, ls=":", lw=0.8, color="k")
ax[1].axvline(np.pi / 4, ls=":", lw=0.8, color="k")
ax[1].set_xlabel(r"$\alpha$", fontsize=8)
ax[1].set_ylabel("determinant", fontsize=8)
ax[1].set_title(r"maximum $9/4$, at the equilateral shape", fontsize=9)
ax[1].legend(fontsize=7, frameon=False, loc="lower right")
for a in ax:
    a.tick_params(labelsize=7)
fig.tight_layout()
out = pathlib.Path(__file__).resolve().parents[2] / "paper" / "fig_sheets.pdf"
fig.savefig(out)
print("wrote", out)

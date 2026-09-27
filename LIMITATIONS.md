# What is not proved here

Lean proves exactly the statements written, under exactly the hypotheses written.

* Theorem 8 (the ledger's second-order expansion) is not formalized. The correct coefficient
  is `−½ Tr(RERE)`, with product weights `1/((λₙ+η)(λₘ+η))`, not gap-squared weights. The
  gap-squared weights belong to the separate fidelity-susceptibility object.
* Theorems 1–3 (the Jacobi spine, the collinear horizon, curvature-induced exceptional points),
  Theorem 4 (Kakeya directional support sets), Theorem 9 (Seeley–DeWitt compatibility),
  Lemma 10, the gluing Theorem 15 and the Kato-type continuity statements (Prop. 4, Thm. 17)
  are not formalized.
* Proposition 2 is proved as the pointwise identity `Tr(RE) = 0`. The contour-integral
  derivative is not formalized.

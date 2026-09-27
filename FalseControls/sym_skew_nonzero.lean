import EmergentTransport.Basic
-- A symmetric times a skew matrix is traceless: for I and [[0,1],[−1,0]] the trace is 0, not 1.
example : Matrix.trace ((1 : Matrix (Fin 2) (Fin 2) ℝ) * !![0, 1; -1, 0]) = 1 := by
  simp [Matrix.trace, Fin.sum_univ_two]

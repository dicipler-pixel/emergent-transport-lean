import EmergentTransport.Basic
-- For skew E = [[0,1],[−1,0]] the undaggered trace Tr(Π₀ E (1−Π₀) E) is −1, not +1.
example : Matrix.trace (EmergentTransport.proj (0 : Fin 2) * !![(0 : ℝ), 1; -1, 0]
    * (1 - EmergentTransport.proj 0) * !![(0 : ℝ), 1; -1, 0]) = 1 := by
  simp [Matrix.trace, EmergentTransport.proj, Matrix.mul_apply, Fin.sum_univ_two]

import EmergentTransport.GapsAndTotals
-- The redistribution operator is not identically zero: for Π = diag(1,0) and Ω = [[0,1],[0,0]]
-- its (1,2) block is 1, so F = [[0,1],[0,0]] ≠ 0.
example : (!![(0 : ℝ), 1; 0, 0] : Matrix (Fin 2) (Fin 2) ℝ) = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp

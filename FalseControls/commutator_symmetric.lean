import EmergentTransport.GapsAndTotals
-- The commutator with a projector is skew, not symmetric: with Π = diag(1,0), Ω = [[0,1],[1,0]]
-- we have [Ω,Π] = [[0,1],[−1,0]], whose transpose is its negative.
example : (Matrix.transpose (!![(0 : ℝ), 1; -1, 0]) : Matrix (Fin 2) (Fin 2) ℝ)
    = !![(0 : ℝ), 1; -1, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp

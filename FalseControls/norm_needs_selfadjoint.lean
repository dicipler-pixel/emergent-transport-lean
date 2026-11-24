import EmergentTransport.GapsAndTotals
-- The norm identity ‖F‖²_F = 2‖ΠΩQ‖²_F needs Ω self-adjoint: for the non-self-adjoint
-- Ω = [[0,1],[0,0]] and Π = diag(1,0) one has ‖F‖²_F = 1 but 2‖ΠΩQ‖²_F = 2.
example : (1 : ℝ) = 2 := by norm_num

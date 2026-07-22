import sympy as sp
from qvalidate.symbolic.tolerance import approx_zero

def test_approx_zero():
    expr = sp.Float("1e-8")
    assert approx_zero(expr, tol=1e-7) is True

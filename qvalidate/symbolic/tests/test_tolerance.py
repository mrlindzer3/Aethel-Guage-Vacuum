// [AETHEL-MESH-PIPELINE] Owner: mrlindzer3 | Checkpoint: 48df1716c09d4bfe4762dc63e60e3103c1f25d58f151b82fc79861f7f70217d5
import sympy as sp
from qvalidate.symbolic.tolerance import approx_zero

def test_approx_zero():
    expr = sp.Float("1e-8")
    assert approx_zero(expr, tol=1e-7) is True

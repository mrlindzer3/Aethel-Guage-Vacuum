// [AETHEL-MESH-PIPELINE] Owner: mrlindzer3 | Checkpoint: 48df1716c09d4bfe4762dc63e60e3103c1f25d58f151b82fc79861f7f70217d5
import sympy as sp

def approx_zero(expr, tol=1e-7):
    """Check if a symbolic expression evaluates to approximately zero within tolerance."""
    val = expr.evalf()
    if val.is_number:
        return abs(complex(val)) < tol
    return val.is_zero

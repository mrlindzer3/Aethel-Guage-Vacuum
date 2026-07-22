import sympy as sp

def approx_zero(expr, tol=1e-7):
    """Check if a symbolic expression evaluates to approximately zero within tolerance."""
    val = expr.evalf()
    if val.is_number:
        return abs(complex(val)) < tol
    return val.is_zero

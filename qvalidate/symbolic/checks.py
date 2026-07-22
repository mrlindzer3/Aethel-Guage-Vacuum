"""Basic symbolic checks for quantum operators.

This module provides a small set of helper functions to run symbolic
sanity checks on matrices/operators before they are used in numerical
or simulation code.

Functions implemented (minimal scaffold):
- commutator(A, B): returns A*B - B*A
- is_unitary(U, tol=None): returns True if U^† U == I (symbolically or numerically with tol)
- simplify_unitary(expr): convenience wrapper around sympy.simplify
"""
from typing import Any, Optional

import sympy as sp
from sympy import Matrix


def _to_matrix(x: Any) -> Matrix:
    if isinstance(x, Matrix):
        return x
    try:
        return Matrix(x)
    except Exception as exc:
        raise TypeError(f"Cannot convert to Matrix: {exc}")


def commutator(A: Any, B: Any) -> Matrix:
    A_m = _to_matrix(A)
    B_m = _to_matrix(B)
    return (A_m * B_m) - (B_m * A_m)


def is_unitary(U: Any, tol: Optional[float] = None) -> bool:
    """Test whether U is unitary.

    If tol is None, perform exact symbolic check (A^† A == I) using SymPy
    simplification and exact equality for all entries. If tol is provided,
    perform a numeric tolerance-based check where entries are evaluated to
    floating-point and compared against tol.
    """
    U_m = _to_matrix(U)
    U_dag = U_m.conjugate().T
    prod = U_dag * U_m
    I = sp.eye(U_m.rows)
    diff = prod - I

    if tol is None:
        diff_s = sp.simplify(diff)
        return all(sp.simplify(entry) == 0 for entry in diff_s)

    # Numeric tolerance path
    max_abs = 0.0
    for entry in diff:
        try:
            val = complex(sp.N(entry, 17))
            absval = abs(val)
        except Exception:
            # if numeric evaluation fails, fall back to symbolic equality
            simplified = sp.simplify(entry)
            if simplified == 0:
                absval = 0.0
            else:
                return False
        if absval > max_abs:
            max_abs = absval
        if max_abs > tol:
            return False
    return True


def simplify_unitary(expr: Any) -> Any:
    return sp.simplify(expr)

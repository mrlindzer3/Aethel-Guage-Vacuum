"""Basic symbolic checks for quantum operators.

This module provides a small set of helper functions to run symbolic
sanity checks on matrices/operators before they are used in numerical
or simulation code.

Functions implemented (minimal scaffold):
- commutator(A, B): returns A*B - B*A
- is_unitary(U): returns True if U^† U == I (symbolically)
- simplify_unitary(expr): convenience wrapper around sympy.simplify
"""
from typing import Any

import sympy as sp
from sympy import Matrix


def _to_matrix(x: Any) -> Matrix:
    """Convert input to a SymPy Matrix if possible."""
    if isinstance(x, Matrix):
        return x
    try:
        return Matrix(x)
    except Exception as exc:
        raise TypeError(f"Cannot convert to Matrix: {exc}")


def commutator(A: Any, B: Any) -> Matrix:
    """Return the commutator [A, B] = A*B - B*A as a SymPy Matrix."""
    A_m = _to_matrix(A)
    B_m = _to_matrix(B)
    return (A_m * B_m) - (B_m * A_m)


def is_unitary(U: Any) -> bool:
    """Symbolically test whether U is unitary: U^† U == I.

    Returns True if the simplified difference is the zero matrix.
    """
    U_m = _to_matrix(U)
    # conjugate transpose
    U_dag = U_m.conjugate().T
    prod = (U_dag * U_m).applyfunc(sp.simplify)
    I = sp.eye(U_m.rows)
    diff = sp.simplify(prod - I)
    # For symbolic matrices, equality to zero matrix is tested by all entries being zero
    return all(sp.simplify(entry) == 0 for entry in diff)


def simplify_unitary(expr: Any) -> Any:
    """Convenience wrapper to simplify symbolic expressions representing unitaries or operators."""
    return sp.simplify(expr)

import sympy as sp
from qvalidate.symbolic.ternary import (
    ternary_cyclic_shift,
    ternary_negation,
    verify_ternary_state_consistency
)

def test_ternary_shift():
    vec = sp.Matrix([0, 1, 2])
    shifted = ternary_cyclic_shift(vec)
    assert shifted == sp.Matrix([1, 2, 0])

def test_ternary_negation():
    vec = sp.Matrix([-1, 0, 1])
    negated = ternary_negation(vec)
    assert negated == sp.Matrix([1, 0, -1])

def test_ternary_consistency():
    vec = sp.Matrix([0, 1, -1])
    assert verify_ternary_state_consistency(vec) is True

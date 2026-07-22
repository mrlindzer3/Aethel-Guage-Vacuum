import sympy as sp
from qvalidate.symbolic.isomorphism import (
    check_operator_isomorphism,
    verify_structural_isomorphism,
    eulers_demon_constraint_loop,
    poincare_hyperbolic_metric,
    poincare_distance_invariant,
    optimize_unified_isomorphism_pipeline,
)

def test_check_operator_isomorphism():
    A = sp.Matrix([[1, 0], [0, 1]])
    B = sp.Matrix([[1, 0], [0, 1]])
    assert check_operator_isomorphism(A, B) is True

def test_verify_structural_isomorphism():
    nodes = sp.Matrix([1, 1])
    stiffness = sp.Matrix([[2, -1], [-1, 2]])
    tension = sp.Matrix([[0, 0], [0, 0]])
    is_stable, laplacian = verify_structural_isomorphism(nodes, stiffness, tension)
    assert laplacian is not None

def test_eulers_demon_constraint_loop():
    state = sp.Matrix([1, 2])
    constraint = sp.Matrix([[1, 0], [0, 1]])
    multiplier = sp.Rational(1, 10)
    regulated = eulers_demon_constraint_loop(state, constraint, multiplier)
    assert regulated.shape == (2, 1)

def test_poincare_geometry():
    y = sp.Symbol('y', positive=True)
    metric = poincare_hyperbolic_metric(y)
    assert metric == 1 / (y ** 2)

    cosh_d = poincare_distance_invariant(0, 1, 0, 2)
    assert cosh_d is not None

def test_unified_pipeline():
    op_a = sp.eye(2)
    op_b = sp.eye(2)
    nodes = sp.Matrix([1, 1])
    stiffness = sp.eye(2)
    tension = sp.zeros(2)
    state = sp.Matrix([1, 1])
    constraint = sp.eye(2)
    mult = 0.1
    y = sp.Symbol('y', positive=True)

    result = optimize_unified_isomorphism_pipeline(
        op_a, op_b, nodes, stiffness, tension, state, constraint, mult, y
    )
    assert result["isomorphic"] is True
    assert "poincare_metric" in result

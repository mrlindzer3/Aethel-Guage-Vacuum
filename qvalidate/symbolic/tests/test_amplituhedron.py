import sympy as sp
from qvalidate.symbolic.amplituhedron import (
    positive_grassmannian_form,
    amplituhedron_volume_surrogate,
    unified_geometric_pipeline
)

def test_grassmannian_form():
    Z = sp.Matrix([[1, 1], [0, 1]])
    assert positive_grassmannian_form(Z) == 1

def test_amplituhedron_volume():
    vars_list = [sp.Symbol('s1', positive=True), sp.Symbol('s2', positive=True)]
    weights = [1, 1]
    res = amplituhedron_volume_surrogate(vars_list, weights)
    assert res is not None

def test_unified_geometric_pipeline():
    op_a = sp.eye(2)
    op_b = sp.eye(2)
    Z = sp.eye(2)
    vars_list = [sp.Symbol('s1', positive=True)]
    weights = [1]
    y = sp.Symbol('y', positive=True)
    
    res = unified_geometric_pipeline(op_a, op_b, Z, vars_list, weights, y)
    assert res["isomorphic"] is True
    assert res["grassmannian_signature"] == 1

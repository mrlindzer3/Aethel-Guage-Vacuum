import sympy as sp
from qvalidate.symbolic.optomechanical_horizon import (
    optomechanical_tweezer_coupling,
    phase_shift_isomorphism_transform,
    white_hole_surface_horizon_condition
)

def test_tweezer_coupling():
    a = sp.Symbol('a', commutative=False)
    a_dag = sp.Symbol('a_dag', commutative=False)
    b = sp.Symbol('b', commutative=False)
    b_dag = sp.Symbol('b_dag', commutative=False)
    g = sp.Symbol('g', real=True)
    
    h_int = optomechanical_tweezer_coupling((a, a_dag), (b, b_dag), g)
    assert h_int is not None

def test_phase_shift_transform():
    field = sp.Symbol('E')
    phi = sp.Symbol('phi')
    transformed = phase_shift_isomorphism_transform(field, phi)
    assert transformed == sp.exp(sp.I * phi) * field

def test_white_hole_horizon():
    v = sp.Symbol('v')
    c_s = sp.Symbol('c_s')
    is_active, residual = white_hole_surface_horizon_condition(v, c_s)
    assert residual == v - c_s

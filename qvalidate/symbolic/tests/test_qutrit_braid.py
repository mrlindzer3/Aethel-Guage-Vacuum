import sympy as sp
from qvalidate.symbolic.qutrit_braid import (
    qutrit_braid_generator,
    universal_constant_injector
)

def test_qutrit_braid_generator():
    theta = sp.Symbol('theta')
    braid = qutrit_braid_generator(theta)
    assert braid.shape == (3, 3)

def test_universal_constant_injector():
    state = sp.Matrix([1, 0, 0])
    const = sp.Rational(1, 1)
    rate = sp.Rational(1, 10)
    injected_state, error = universal_constant_injector(state, const, rate)
    assert injected_state.shape == (3, 1)
    assert error is not None

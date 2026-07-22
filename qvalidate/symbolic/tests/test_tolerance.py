import sympy as sp
from sympy import Matrix

from qvalidate.symbolic.checks import is_unitary


def test_is_unitary_numeric_tolerance():
    # create Hadamard and perturb slightly with floating noise
    h = (1 / sp.sqrt(2)) * Matrix([[1, 1], [1, -1]])
    h_noisy = Matrix([[h[0,0] + 1e-8, h[0,1]], [h[1,0], h[1,1] - 1e-8]])
    assert is_unitary(h_noisy, tol=1e-6)
    assert not is_unitary(h_noisy, tol=1e-12)

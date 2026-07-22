import sympy as sp
from qvalidate.symbolic.checks import commutator, is_unitary

def test_commutator():
    A = sp.Matrix([[0, 1], [1, 0]])
    B = sp.Matrix([[1, 0], [0, -1]])
    res = commutator(A, B)
    assert res is not None

def test_is_unitary():
    U = sp.eye(2)
    assert is_unitary(U) is True
import sympy as sp
from sympy import Matrix, I, sqrt

from qvalidate.symbolic.checks import commutator, is_unitary


def test_pauli_commutator():
    sigma_x = Matrix([[0, 1], [1, 0]])
    sigma_y = Matrix([[0, -I], [I, 0]])
    sigma_z = Matrix([[1, 0], [0, -1]])

    # [sigma_x, sigma_y] = 2 i sigma_z
    comm = commutator(sigma_x, sigma_y)
    expected = 2 * I * sigma_z
    assert sp.simplify(comm - expected) == Matrix([[0, 0], [0, 0]])


def test_hadamard_unitary():
    h = (1 / sqrt(2)) * Matrix([[1, 1], [1, -1]])
    assert is_unitary(h)


def test_identity_unitary():
    I2 = Matrix([[1, 0], [0, 1]])
    assert is_unitary(I2)

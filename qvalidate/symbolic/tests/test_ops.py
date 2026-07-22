import sympy as sp
from qvalidate.symbolic.ops import tensor_product, is_hermitian

def test_tensor_product():
    A = sp.Matrix([[0, 1], [1, 0]])
    B = sp.eye(2)
    tp = tensor_product(A, B)
    assert tp.shape == (4, 4)

def test_is_hermitian():
    H = sp.Matrix([[2, 1 - sp.I], [1 + sp.I, 3]])
    assert is_hermitian(H) is True

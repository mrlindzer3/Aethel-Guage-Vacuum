import sympy as sp

def tensor_product(A, B):
    """Compute the symbolic Kronecker/tensor product of matrices A and B."""
    return sp.kronecker_product(A, B)

def is_hermitian(A, tol=1e-7):
    """Check if matrix A is hermitian: A == A†."""
    diff = sp.simplify(A - A.H)
    return diff.is_zero

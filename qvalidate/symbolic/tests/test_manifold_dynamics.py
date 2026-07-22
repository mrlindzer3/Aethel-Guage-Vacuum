import sympy as sp
from qvalidate.symbolic.manifold_dynamics import (
    poincare_disk_metric,
    poincare_ball_metric,
    tensegrity_laplacian_operator,
    cauchy_lagrange_invariant,
    hawking_bekenstein_entropy_density,
    einstein_field_residual,
    goedel_consistency_projection
)

def test_poincare_disk_and_ball():
    x, y = sp.symbols('x y', real=True)
    disk_m = poincare_disk_metric(x, y)
    assert disk_m == 4 / (1 - x**2 - y**2)**2

    coords = [sp.Symbol('x1'), sp.Symbol('x2')]
    ball_m = poincare_ball_metric(coords)
    assert ball_m is not None

def test_tensegrity_and_cauchy_lagrange():
    K = sp.eye(2)
    T = sp.zeros(2)
    laplacian = tensegrity_laplacian_operator(K, T)
    assert laplacian == sp.eye(2)

    def_tensor = sp.eye(2)
    velocity = sp.Matrix([1, 1])
    assert cauchy_lagrange_invariant(def_tensor, velocity) == velocity

def test_hawking_einstein_goedel():
    area = sp.Symbol('A', positive=True)
    planck = sp.Symbol('lp', positive=True)
    entropy = hawking_bekenstein_entropy_density(area, planck)
    assert entropy == area / (4 * planck**2)

    g = sp.eye(2)
    ricci = sp.zeros(2)
    lam = sp.Symbol('Lambda')
    t_stress = sp.zeros(2)
    residual = einstein_field_residual(ricci, g, lam, t_stress)
    assert residual is not None

    state = sp.Matrix([1, 0])
    op = sp.eye(2)
    assert goedel_consistency_projection(state, op) == state

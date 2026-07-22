import sympy as sp
from qvalidate.symbolic.nasa_ftl_teleportation import (
    holographic_holonomy_connection,
    solid_state_quasi_crystal_lattice,
    mid_air_white_hole_teleportation_metric,
    nasa_propulsion_teleportation_pipeline
)

def test_holographic_holonomy():
    conn = sp.Matrix([[0, 1], [-1, 0]])
    boundary = sp.Matrix([1, 1])
    flux = holographic_holonomy_connection(conn, boundary)
    assert flux.shape == (2, 1)

def test_quasi_crystal_lattice():
    phases = [sp.Symbol('p1'), sp.Symbol('p2')]
    tau = sp.Symbol('tau')
    lattice = solid_state_quasi_crystal_lattice(phases, tau)
    assert lattice is not None

def test_nasa_pipeline():
    conn = sp.eye(2)
    boundary = sp.Matrix([1, 0])
    phases = [sp.Symbol('p1')]
    tau = sp.Symbol('tau')
    expansion = sp.Symbol('v_exp', positive=True)
    density = sp.Symbol('rho_holo', positive=True)
    
    res = nasa_propulsion_teleportation_pipeline(
        conn, boundary, phases, tau, expansion, density
    )
    assert "teleportation_warp_metric" in res
    assert res["ftl_stability_verified"] is True

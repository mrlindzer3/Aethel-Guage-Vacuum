import sympy as sp
from qvalidate.symbolic.nasa_telescope_optics import (
    quasi_crystal_optical_transfer,
    black_white_hole_horizon_optics,
    einstein_fresnel_diffraction_integral,
    fresnel_hawking_thermal_optics,
    amber_straughn_galaxy_assembly_metric,
    nasa_advanced_observatory_pipeline
)

def test_quasi_crystal_optics():
    field = sp.Symbol('E_in')
    tau = sp.Symbol('tau')
    phase = sp.Symbol('phi')
    res = quasi_crystal_optical_transfer(field, tau, phase)
    assert res is not None

def test_black_white_hole_horizon_optics():
    metric = sp.Symbol('g_00', positive=True)
    kappa = sp.Symbol('kappa')
    r_h = sp.Symbol('r_h', positive=True)
    lens = black_white_hole_horizon_optics(metric, kappa, r_h)
    assert lens == 2 * kappa * r_h / metric

def test_straughn_galaxy_assembly():
    z = sp.Symbol('z', positive=True)
    sfr = sp.Symbol('SFR', positive=True)
    morph = sp.Symbol('M_weight', positive=True)
    assembly = amber_straughn_galaxy_assembly_metric(z, sfr, morph)
    assert assembly == (1 + z)**2 * sfr * morph

def test_nasa_observatory_pipeline():
    res = nasa_advanced_observatory_pipeline(
        sp.Symbol('E'), sp.Symbol('tau'), sp.Symbol('phi'),
        sp.Symbol('g'), sp.Symbol('kappa'), sp.Symbol('r_h'),
        sp.Symbol('lam'), sp.Symbol('a'), sp.Symbol('d'),
        sp.Symbol('T'), sp.Symbol('hbar'), sp.Symbol('c'),
        sp.Symbol('z'), sp.Symbol('sfr'), sp.Symbol('morph')
    )
    assert "straughn_galaxy_assembly_index" in res
    assert "observatory_system_efficiency" in res

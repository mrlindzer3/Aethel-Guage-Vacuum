import sympy as sp
from qvalidate.symbolic.white_hole_svd import (
    white_hole_surface_svd,
    isomorphic_white_hole_rendering_pipeline
)

def test_white_hole_surface_svd():
    mat = sp.Matrix([[1, 0], [0, 2]])
    res = white_hole_surface_svd(mat)
    assert res["singular_values"] is not None
    assert res["is_invertible"] is True

def test_isomorphic_white_hole_rendering_pipeline():
    metric = sp.eye(2)
    coupling = sp.Matrix([[3, 0], [0, 4]])
    pipeline_res = isomorphic_white_hole_rendering_pipeline(metric, coupling)
    assert "rendered_surface_metric" in pipeline_res

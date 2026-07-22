import sympy as sp
from qvalidate.symbolic.folding_coherence import (
    compute_fold_recurrence_feedback,
    folding_instruction_matrix,
    comprehensive_folding_coherence_pipeline
)

def test_fold_recurrence_feedback():
    pre = sp.Matrix([1, 1])
    post = sp.Matrix([1, 1])
    fidelity, residual = compute_fold_recurrence_feedback(pre, post)
    assert residual == sp.Matrix([0, 0])
    assert fidelity == 1

def test_folding_instruction_matrix():
    state = sp.Matrix([1, 0])
    metric = sp.eye(2)
    instructions = folding_instruction_matrix(state, metric)
    assert instructions == state

def test_comprehensive_folding_pipeline():
    pre = sp.Matrix([1, 0])
    post = sp.Matrix([1, 0])
    metric = sp.eye(2)
    res = comprehensive_folding_coherence_pipeline(pre, post, metric)
    assert res["coherence_fidelity"] == 1
    assert "fold_instructions" in res

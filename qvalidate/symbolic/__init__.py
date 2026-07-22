"""Symbolic verification package for quantum operators."""
from .checks import commutator, is_unitary
from .ops import tensor_product, is_hermitian
from .tolerance import approx_zero
"""QValidate: Quantum-Classical Hybrid Verification Suite."""
__version__ = "0.1.0"
"""qvalidate.symbolic

Symbolic quantum-classical hybrid verification utilities (scaffold).
"""

from .checks import commutator, is_unitary, simplify_unitary

__all__ = ["commutator", "is_unitary", "simplify_unitary"]
"""Symbolic verification package for quantum operators."""
from .checks import commutator, is_unitary
from .ops import tensor_product, is_hermitian
from .tolerance import approx_zero
from .isomorphism import (
    check_operator_isomorphism,
    verify_algebraic_homomorphism,
    verify_structural_isomorphism,
    eulers_demon_constraint_loop,
    poincare_hyperbolic_metric,
    poincare_distance_invariant
)
from .amplituhedron import (
    positive_grassmannian_form,
    amplituhedron_volume_surrogate,
    unified_geometric_pipeline
)

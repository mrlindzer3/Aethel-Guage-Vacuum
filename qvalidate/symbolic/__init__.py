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
from .ternary import (
    ternary_cyclic_shift,
    ternary_negation,
    verify_ternary_state_consistency
)
from .qutrit_braid import (
    qutrit_braid_generator,
    universal_constant_injector
)
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
from .ternary import (
    ternary_cyclic_shift,
    ternary_negation,
    verify_ternary_state_consistency
)
from .qutrit_braid import (
    qutrit_braid_generator,
    universal_constant_injector
)
from .optomechanical_horizon import (
    optomechanical_tweezer_coupling,
    phase_shift_isomorphism_transform,
    white_hole_surface_horizon_condition
)

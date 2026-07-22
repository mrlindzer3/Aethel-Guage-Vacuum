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

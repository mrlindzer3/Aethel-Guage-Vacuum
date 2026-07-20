"""Medium-fidelity physics models for optomechanics.

This module provides deterministic, testable toy models that use numpy and scipy when available.
"""
from typing import Tuple
import numpy as np

try:
    from scipy import linalg
    SCIPY_AVAILABLE = True
except Exception:
    SCIPY_AVAILABLE = False


def harmonic_oscillator_frequency(k: float, m: float) -> float:
    """Return the natural frequency (rad/s) of a harmonic oscillator with spring k and mass m.

    Deterministic, pure numeric calculation.
    """
    k = float(k)
    m = float(m)
    if m <= 0 or k <= 0:
        raise ValueError("k and m must be positive")
    return float(np.sqrt(k / m))


def coupled_mode_spectrum(coupling_matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute eigenfrequencies of a coupled mode system.

    Returns (w, v) where w are eigenvalues and v eigenvectors. Uses scipy.linalg.eigh when available for symmetric matrices.
    """
    if SCIPY_AVAILABLE:
        vals, vecs = linalg.eigh(coupling_matrix)
    else:
        vals, vecs = np.linalg.eigh(coupling_matrix)
    return vals, vecs


def linearized_optomech_shift(g0: float, n_c: float, kappa: float) -> float:
    """Toy linearized optical frequency shift estimate: g0 * sqrt(n_c) / kappa

    Parameters are interpreted in toy units; function is deterministic.
    """
    g0 = float(g0)
    n_c = float(n_c)
    kappa = float(kappa)
    if kappa == 0:
        return float('inf')
    return float(abs(g0) * np.sqrt(max(n_c, 0.0)) / kappa)

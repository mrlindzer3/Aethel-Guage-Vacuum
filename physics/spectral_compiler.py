# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/spectral_compiler.py
# ROLE: Non-Commutative Spectral Geometry Compiler Core
# ARCHITECTURE: Connes' Dirac Operator Metric Projection Matrix
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SpectralCompiler")

class SpectralCompiler:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        # Initialize the generalized Dirac Operator D as a Hermitian matrix
        self.dirac_operator = np.zeros((node_count, node_count), dtype=np.complex64)

    def compute_spectral_action(self, base_space: np.ndarray, ternary_bus: np.ndarray) -> dict:
        """
        Constructs the non-commutative Dirac operator D and computes its 
        eigenvalue spectrum to derive the emergent spacetime metric.
        """
        logger.info("🪐 SPECTRAL: Computing the Dirac operator eigenvalues...")
        
        # Build the coordinate interaction matrix (distance scaling)
        diff = base_space[:, np.newaxis, :] - base_space[np.newaxis, :, :]
        dist_matrix = np.linalg.norm(diff, axis=-1)
        
        # Inject the discrete ternary states as diagonal mass/spin terms
        diagonal_masses = np.diag(ternary_bus.astype(np.complex64) * 2.5)
        
        # Construct D: combining spatial distance metrics with internal algebraic logic states
        self.dirac_operator = dist_matrix * (1j * np.eye(self.node_count)) + diagonal_masses
        
        # Enforce Hermiticity: D must be self-adjoint
        self.dirac_operator = 0.5 * (self.dirac_operator + self.dirac_operator.conj().T)
        
        # Compute the spectral eigenvalues (the non-commutative metric invariants)
        eigenvalues = np.linalg.eigvalsh(self.dirac_operator)
        
        # The Spectral Action is computed as the trace of a cutoff function over D
        # Tr(f(D/Lambda)) -> represented as the sum of regulated eigenvalues
        spectral_action = float(np.sum(1.0 / (1.0 + (eigenvalues / 10.0)**2)))
        
        logger.info(f"🕸️ SPECTRAL: Emergent Spectral Action Trace: {spectral_action:.6f}")
        
        return {
            "eigenvalues": eigenvalues,
            "spectral_action": spectral_action,
            "dirac_operator": self.dirac_operator
        }

    def project_spectral_metric(self, base_space: np.ndarray, spectral_profile: dict) -> np.ndarray:
        """
        Updates the physical spatial layout by projecting the emergent metric 
        derived purely from the Dirac eigenvalues back to coordinate space.
        """
        eigenvalues = spectral_profile["eigenvalues"]
        
        # Map the spectral invariants to coordinate displacement forces
        spectral_force = np.zeros_like(base_space)
        spectral_force[:, 0] = np.real(eigenvalues) * 0.0002
        spectral_force[:, 1] = np.roll(np.real(eigenvalues), 1) * 0.0002
        
        return base_space + spectral_force

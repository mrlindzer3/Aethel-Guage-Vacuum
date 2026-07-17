# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/ctc_processor.py
# ROLE: Deutschian Closed Timelike Curve (CTC) Simulator
# ARCHITECTURE: Adaptive-Tolerance Fixed-Point Quantum Solver
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TemporalCTC")

class CTCProcessor:
    def __init__(self, dimension: int = 8):
        self.dimension = dimension
        
    def generate_problem_unitary(self, matrix_key: np.ndarray) -> np.ndarray:
        """
        Generates a unitary operator 'U' representing the computational system
        coupled with the temporal loop.
        """
        hermitian = 0.5 * (matrix_key + np.conj(matrix_key).T)
        eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
        unitary = np.dot(eigenvectors * np.exp(1j * eigenvalues), np.conj(eigenvectors).T)
        return unitary

    def solve_temporal_loop(self, input_state: np.ndarray, matrix_key: np.ndarray, max_iterations: int = 150, current_laws: dict = None) -> np.ndarray:
        """
        Finds the self-consistent Deutschian fixed point using adaptive precision.
        Tightens constraints when background metrics are volatile.
        """
        logger.info("⏳ TEMPORAL: Initializing adaptive Closed Timelike Curve search...")
        
        # Determine dynamic tolerance based on the Immirzi parameter (gamma) and gravity scale
        if current_laws:
            gamma = current_laws.get("gamma", 0.272)
            gravity_G = current_laws.get("gravity_G", 1.0)
            # Volatile background metrics force a tighter convergence ceiling
            base_tolerance = 1e-6 * (1.0 / (gamma * gravity_G + 1e-5))
            tolerance = np.clip(base_tolerance, 1e-9, 1e-5)
        else:
            tolerance = 1e-6
            
        logger.info(f"🌀 TEMPORAL: Causal consistency constraint set to: {tolerance:.2e}")
        
        input_state = input_state / np.linalg.norm(input_state)
        rho_in = np.outer(input_state, np.conj(input_state))
        U = self.generate_problem_unitary(matrix_key)
        
        # Start with a maximally mixed state guess
        rho_ctc = np.eye(self.dimension, dtype=np.complex128) / self.dimension
        
        for step in range(max_iterations):
            combined_state = np.kron(rho_in, rho_ctc)
            
            dim_total = self.dimension * self.dimension
            U_expanded = np.eye(dim_total, dtype=np.complex128)
            U_expanded[:self.dimension, :self.dimension] = U
            
            evolved_state = np.dot(U_expanded, np.dot(combined_state, np.conj(U_expanded).T))
            
            # Partial trace approximation over system qubits
            next_rho_ctc = np.zeros((self.dimension, self.dimension), dtype=np.complex128)
            for i in range(self.dimension):
                next_rho_ctc += evolved_state[i*self.dimension:(i+1)*self.dimension, i*self.dimension:(i+1)*self.dimension]
            
            trace_val = np.trace(next_rho_ctc)
            if np.abs(trace_val) > 1e-12:
                next_rho_ctc /= trace_val
                
            difference = np.linalg.norm(next_rho_ctc - rho_ctc, ord='fro')
            
            if difference < tolerance:
                logger.info(f"✨ TEMPORAL: Paradox-free fixed-point locked in {step} timeline passes.")
                return next_rho_ctc
                
            rho_ctc = next_rho_ctc
            
        logger.warning("⚠️ TEMPORAL: Divergent timeline detected! Forcing loop safety fallback state.")
        return np.eye(self.dimension, dtype=np.complex128) / self.dimension

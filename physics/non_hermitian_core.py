# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/non_hermitian_core.py
# ROLE: Non-Hermitian Open System Hamiltonian Matrix Operator
# ARCHITECTURE: Exceptional Point Resonant Calibration Engine
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NonHermitianCore")

class NonHermitianCore:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def construct_non_hermitian_hamiltonian(self, base_space: np.ndarray, schrodinger_phases: np.ndarray) -> dict:
        """
        Builds a complex, non-Hermitian matrix tracking localized energy gain
        (laser pumping) and loss (dissipation) across the node network.
        """
        logger.info("🪐 PHYSICS: Constructing complex Non-Hermitian Hamiltonian...")
        
        # Diagonal elements represent real energy levels plus an imaginary gain/loss factor (i*Gamma)
        real_energy = np.cos(schrodinger_phases)
        # Emulate a alternating gain/loss profile across adjacent node channels
        imag_gain_loss = np.zeros(self.node_count, dtype=np.float32)
        imag_gain_loss[0::2] = +0.12  # Energy Gain (Laser Pumping)
        imag_gain_loss[1::2] = -0.12  # Energy Loss (Dissipation)
        
        complex_diagonal = real_energy + 1j * imag_gain_loss
        
        # Detect proximity to Exceptional Points where eigenvalues coalesce
        eigenvalue_distance = np.abs(real_energy[0::2] - real_energy[1::2])
        ep_proximity_mask = eigenvalue_distance < 0.05
        active_eps = np.where(ep_proximity_mask)[0]
        
        if len(active_eps) > 0:
            logger.info(f"✨ EXCEPTION: Substrate operating near {len(active_eps)} localized Exceptional Points. Sensor sensitivity maximized.")
            
        return {
            "complex_diagonal": complex_diagonal,
            "exceptional_points_active": ep_proximity_mask,
            "gain_loss_profile": imag_gain_loss
        }

    def compute_non_hermitian_phase_transport(self, base_space: np.ndarray, nh_profile: dict) -> np.ndarray:
        """
        Applies a non-reciprocal geometric phase shift to the node coordinates,
        using Exceptional Point dynamics to suppress ambient noise.
        """
        adjusted_space = base_space.copy()
        ep_mask = nh_profile["exceptional_points_active"]
        
        # For nodes operating right at an Exceptional Point, inject an invariant 
        # topological phase vector that dampens localized thermal jitter
        for i in range(min(len(ep_mask), self.node_count // 2)):
            if ep_mask[i]:
                node_idx_a = i * 2
                node_idx_b = i * 2 + 1
                
                # Force non-reciprocal chiral orientation updates
                inter_node_vector = base_space[node_idx_b] - base_space[node_idx_a]
                adjusted_space[node_idx_a] += np.cross(inter_node_vector, [0, 0, 0.015])
                adjusted_space[node_idx_b] -= np.cross(inter_node_vector, [0, 0, 0.015])
                
        return adjusted_space

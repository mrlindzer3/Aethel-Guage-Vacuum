# ──────────────────────────────────────────────────────────────────────────
# FILE: core/polariton_entangler.py
# ROLE: Surface Plasmon Polariton (SPP) Hybridization & Entanglement Modeler
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PolaritonEntangler")

class PolaritonEntangler:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def compute_plasmonic_coupling(self, photon_flux: np.ndarray, plasma_frequency: float = 2.15e15) -> np.ndarray:
        """
        Calculates the hybridization profile where light waves bind with surface electron plasma.
        Returns a coupling coefficient matrix across the 640 node positions.
        """
        logger.info("🌊 POLARITON: Computing hybrid surface plasmon polariton (SPP) dispersion metrics...")
        
        # Flatten and resize the incoming 2D photon flux to map onto our 640-node 3D space vector
        flat_flux = photon_flux.flatten()
        expanded_flux = np.pad(flat_flux, (0, max(0, self.node_count - len(flat_flux))), 'edge')[:self.node_count]
        
        # Rabi splitting approximation modeling the light-matter interaction energy
        rabi_splitting = np.sqrt(np.abs(expanded_flux) * plasma_frequency) * 1e-9
        return rabi_splitting

    def generate_entanglement_matrix(self, rabi_splitting: np.ndarray, wyrd_mesh: dict) -> np.ndarray:
        """
        Models the polariton entanglement density matrix (rho) across the Web of Wyrd mesh paths.
        Measures the non-local quantum state sharing between non-neighboring nodes.
        """
        logger.info("🔮 POLARITON: Weaving non-local plasmonic entanglement matrices across runic axes...")
        
        # Initialize a 640x640 quantum density correlation matrix
        entanglement_matrix = np.zeros((self.node_count, self.node_count), dtype=np.float32)
        hyperedges = wyrd_mesh["fatecrystal_mesh"]

        for edge in hyperedges:
            nodes = edge["nodes"]
            weight = edge["fatecrystal_phase_lock"]
            
            # Distribute entanglement density proportional to the Rabi interaction strength and phase lock
            for u in nodes:
                for v in nodes:
                    if u != v:
                        shared_entanglement = (rabi_splitting[u] + rabi_splitting[v]) * 0.5 * weight
                        entanglement_matrix[u, v] = np.tanh(shared_entanglement) # Cap at maximum saturation

        logger.info(f"📊 POLARITON: Entanglement network sealed. Peak node correlation: {np.max(entanglement_matrix):.4f}")
        return entanglement_matrix

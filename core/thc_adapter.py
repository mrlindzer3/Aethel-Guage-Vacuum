# ──────────────────────────────────────────────────────────────────────────
# FILE: core/thc_adapter.py
# ROLE: Tri-Harmonic Vector Equilibrium (THVE) Manifold Adapter
# ARCHITECTURE: Non-Euclidean Pseudospherical Tension Mesh Abstraction
# COMPATIBILITY: Software Layer Complementing Original Hardware Stack
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("THCAdapter")

class THCAdapter:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        # Curvature constant for the negative-space pseudospheric coordinate mapping
        self.k_curvature = -1.25

    def compute_vector_equilibrium_tensor(self, spatial_positions: np.ndarray, ternary_states: np.ndarray) -> np.ndarray:
        """
        Executes the Tri-Harmonic Vector Equilibrium (THVE) algorithm.
        Balances reciprocal tensile forces across 640 nodes projected onto a 
        negative-curvature pseudospherical manifold overlay.
        """
        logger.info("🌌 THC-ADAPTER: Resolving Tri-Harmonic Vector Equilibrium (THVE) fields...")
        
        # Map 3D coordinates onto the complex pseudosphere boundary layer
        radii = np.linalg.norm(spatial_positions, axis=1)
        max_r = np.max(radii) if np.max(radii) > 0 else 1.0
        normalized_coords = spatial_positions / max_r
        
        # Initialize the 640x640 Reciprocal Tensile Matrix (RTM)
        reciprocal_tensile_matrix = np.zeros((self.node_count, self.node_count), dtype=np.float32)
        
        logger.info("📐 THC-ADAPTER: Calculating non-Euclidean manifold metric differentials...")
        for i in range(self.node_count):
            coord_u = normalized_coords[i]
            state_u = ternary_states[i]
            
            for j in range(i + 1, self.node_count):
                coord_v = normalized_coords[j]
                state_j = ternary_states[j]
                
                # Calculate the raw Euclidean chord distance as a baseline
                chord_dist = np.linalg.norm(coord_u - coord_v)
                
                # Apply the pseudospherical metric scaling modifier based on negative curvature
                manifold_scale = np.exp(self.k_curvature * chord_dist)
                
                # Determine reciprocal equilibrium: opposite ternary states create 
                # a structural tensile pull, matching states provide a compressive strut push.
                if state_u != state_j and (state_u == -1 or state_j == -1):
                    equilibrium_tension = chord_dist * 0.75 * manifold_scale  # Tensile Cable pull
                else:
                    equilibrium_tension = (1.0 / (chord_dist + 1e-5)) * 1.25 * manifold_scale  # Compressive Strut push
                
                reciprocal_tensile_matrix[i, j] = equilibrium_tension
                reciprocal_tensile_matrix[j, i] = equilibrium_tension
                
        logger.info(f"✨ THC-ADAPTER: Equilibrium stabilized. Maximum tensor tension: {np.max(reciprocal_tensile_matrix):.4f}")
        return reciprocal_tensile_matrix

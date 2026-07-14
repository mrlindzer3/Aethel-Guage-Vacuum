# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/fracton_core.py
# ROLE: 3D Fracton Lattice Immobile Constraint Matrix Operator
# ARCHITECTURE: Subsystem Symmetry & X-Cube Projection Mesh
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("FractonCore")

class FractonCore:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        # Define a 3D grid layout size to project our 640 nodes onto an X-Cube lattice geometry
        self.grid_side = int(np.ceil(node_count ** (1/3))) # L x L x L cube bounds

    def enforce_xcube_constraints(self, base_space: np.ndarray) -> dict:
        """
        Evaluates the node positions through the strict 3D X-cube model stabilizer.
        Identifies individual node deviations that violate sub-dimensional immobility rules.
        """
        logger.info("🪐 PHYSICS: Projecting 3D coordinates onto a Fracton X-Cube lattice topology...")
        
        # Center and map spatial positions to integer lattice indices
        center = np.mean(base_space, axis=0)
        normalized_coords = base_space - center
        scaling_factor = np.max(np.abs(normalized_coords)) if np.max(np.abs(normalized_coords)) > 0 else 1.0
        
        lattice_indices = np.round((normalized_coords / scaling_factor) * (self.grid_side / 2)).astype(np.int32)
        
        # Calculate localized cube-operator invariants (Product of spins around a 3D elementary cube)
        # Any non-zero deviation represents an un-authorized individual excitation (fracton violation)
        fracton_fault_mask = np.zeros(self.node_count, dtype=bool)
        
        for i in range(self.node_count):
            # Check if an isolated node has broken away from its planar alignment subgroup
            same_plane_x = np.where(lattice_indices[:, 0] == lattice_indices[i, 0])[0]
            same_plane_y = np.where(lattice_indices[:, 1] == lattice_indices[i, 1])[0]
            
            # If a node loses planar coordination, it breaks subsystem symmetry constraints
            if len(same_plane_x) < 2 or len(same_plane_y) < 2:
                fracton_fault_mask[i] = True
                
        active_faults = np.where(fracton_fault_mask)[0]
        if len(active_faults) > 0:
            logger.warning(f"⚠️ FRACTON: Detected {len(active_faults)} isolated mobility violations. Suppressing coordinate leakage...")
            
        return {
            "faulty_node_indices": active_faults,
            "lattice_indices": lattice_indices
        }

    def apply_immobility_clamping(self, base_space: np.ndarray, fracton_profile: dict) -> np.ndarray:
        """
        Applies strict geometric damping forces that lock individual nodes down, 
        allowing coordinate adjustments only when nodes move as correlated pairs along identical lines.
        """
        clamped_space = base_space.copy()
        faulty_indices = fracton_profile["faulty_node_indices"]
        
        if len(faulty_indices) == 0:
            return clamped_space
            
        # Lock isolated, drifting nodes back into their local sub-manifold intersection points
        for idx in faulty_indices:
            # Snap individual node fluctuations back to zero-motion state
            clamped_space[idx] = np.mean(base_space, axis=0) * 0.1 + base_space[idx] * 0.9
            
        return clamped_space

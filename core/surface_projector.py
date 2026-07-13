# ──────────────────────────────────────────────────────────────────────────
# FILE: core/surface_projector.py
# ROLE: Tertiary Equidistant Juxtaposition Coordinate Projector
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SurfaceProjector")

class SurfaceProjector:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def compute_juxtaposition_layout(self, node_positions: np.ndarray, ternary_states: np.ndarray) -> np.ndarray:
        """
        Transforms 3D toroidal coordinates into a flattened 2D equidistant plan
        juxtaposed by ternary state classifications [-1, 0, +1].
        """
        logger.info("📐 PROJECTOR: Calculating tertiary equidistant surface boundaries...")
        
        flattened_coordinates = np.zeros((self.node_count, 2), dtype=np.float32)
        
        # Extract angular metrics from original 3D positions to preserve topology
        angles = np.arctan2(node_positions[:, 1], node_positions[:, 0])
        
        for i in range(self.node_count):
            state = ternary_states[i]
            
            # Establish equidistant radial baselines based on ternary classification
            if state == -1:
                radius = 1.5  # Inner Horizon
            elif state == 0:
                radius = 3.0  # Toroidal Core Backbone
            else:
                radius = 4.5  # Outer Wyrd Envelope
                
            # Compute balanced 2D surface position
            x_planar = radius * np.cos(angles[i])
            y_planar = radius * np.sin(angles[i])
            
            flattened_coordinates[i] = [x_planar, y_planar]
            
        logger.info("📊 PROJECTOR: 2D Equidistant surface layout compiled successfully.")
        return flattened_coordinates

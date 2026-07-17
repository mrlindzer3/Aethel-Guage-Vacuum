# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/rendering_bridge.py
# ROLE: Server-Side Vector Frame Buffer Generator
# ARCHITECTURE: Hardware-Agnostic Matrix Streamer
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RenderingBridge")

class SubstrateFrameBuffer:
    def __init__(self, target_width: int = 7680, target_height: int = 4320):
        # 8K Target Dimensions
        self.width = target_width
        self.height = target_height

    def project_substrate_to_pixels(self, 3d_positions: np.ndarray) -> list:
        """
        Converts raw 3D spatial node coordinates into an optimized 
        2D screen projection list on the server.
        """
        if len(3d_positions) == 0:
            return []

        # Extract X and Y components and normalize them to a 0.0 to 1.0 range
        x_coords = 3d_positions[:, 0]
        y_coords = 3d_positions[:, 1]
        
        norm_x = (x_coords - np.min(x_coords)) / (np.ptp(x_coords) + 1e-5)
        norm_y = (y_coords - np.min(y_coords)) / (np.ptp(y_coords) + 1e-5)
        
        # Scale directly to 8K screen space matrix locations
        pixel_x = (norm_x * self.width).astype(int)
        pixel_y = (norm_y * self.height).astype(int)
        
        # Zip into a lightweight, compressed flat coordinate stream
        projected_frame = np.column_stack((pixel_x, pixel_y)).tolist()
        
        logger.info(f"🖥️ BRIDGE: Projected {len(3d_positions)} physics nodes to 8K viewport coordinates.")
        return projected_frame

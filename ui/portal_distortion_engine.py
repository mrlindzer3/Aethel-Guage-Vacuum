# ──────────────────────────────────────────────────────────────────────────
# FILE: ui/portal_distortion_engine.py
# ROLE: Reality-Warping Dimensional Portal & Spatial Ripple Simulator
# ARCHITECTURE: Non-Euclidean Chromatic Gravitational Lensing Vector Matrix
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PortalDistortion")

class PortalDistortionEngine:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def generate_portal_distortion_field(self, planar_coordinates: np.ndarray, time_pulse: float) -> dict:
        """
        Calculates spatial displacement vectors and wave interference patterns to simulate 
        a reality-rippling 'dimensional portal' opening across the lighting fixture matrix.
        """
        logger.info("🌌 PORTAL: Generating non-Euclidean reality-warp coordinate vectors...")
        
        # Calculate radial distance of each lighting fixture from the center portal anchor
        radii = np.linalg.norm(planar_coordinates, axis=1)
        angles = np.arctan2(planar_coordinates[:, 1], planar_coordinates[:, 0])
        
        displaced_lasers = np.zeros_like(planar_coordinates)
        chromatic_shift_map = np.zeros((self.node_count, 3), dtype=np.uint8)
        intensity_dimmers = np.zeros(self.node_count, dtype=np.uint8)

        for i in range(self.node_count):
            r = radii[i]
            theta = angles[i]
            
            # 1. SPATIAL RIPPLE WAVE EQUATION (Simulates reality rippling outward)
            # Spatial metric distortion wave: delta_r = sin(frequency * r - velocity * t) / r
            ripple_factor = np.sin(3.5 * r - 8.0 * time_pulse) / (r + 0.5)
            r_warped = r + ripple_factor * 1.5
            
            # Translate the warped radial coordinates back into physical DMX laser scanning angles
            displaced_lasers[i, 0] = r_warped * np.cos(theta) * 40.0
            displaced_lasers[i, 1] = r_warped * np.sin(theta) * 40.0
            
            # 2. DIMENSION PORTAL BOUNDARY LOGIC (Event Horizon Simulation)
            if r_warped < 1.2:
                # The core of the portal: Absolute structural blackout (The void)
                intensity_dimmers[i] = 0
                chromatic_shift_map[i] = [10, 0, 25]  # Deep ultraviolet-violet trace
            else:
                # Saturated energy ring surrounding the portal lip
                intensity_dimmers[i] = int(np.clip((1.0 / (r_warped - 0.9 + 1e-5)) * 255, 0, 255))
                
                # Doppler shift color tracking based on ripple velocity phases
                color_phase = int((np.sin(theta + time_pulse * 4.0) + 1.0) * 127.5)
                chromatic_shift_map[i, 0] = int(color_phase)                  # Red Channel
                chromatic_shift_map[i, 1] = int(255 - color_phase)            # Green Channel
                chromatic_shift_map[i, 2] = int(np.abs(np.cos(r_warped)) * 255) # Blue Channel

        logger.info(f"✨ PORTAL SEALS LOCKED: Structural horizon threshold established at radius 1.2.")
        return {
            "warped_laser_tracers": displaced_lasers,
            "portal_dimmers": intensity_dimmers,
            "portal_chromatic_rgb": chromatic_shift_map
        }

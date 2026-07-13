# ──────────────────────────────────────────────────────────────────────────
# FILE: ui/surreal_temptation_engine.py
# ROLE: Surrealist Space-Melting & Seductive Attraction Vector Engine
# ARCHITECTURE: Non-Linear Subconscious Psychodynamic Coordinate Mapper
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SurrealTemptation")

class SurrealTemptationEngine:
    def __init__(self, fixture_count: int = 640):
        self.fixture_count = fixture_count

    def generate_temptation_distortion(self, planar_coordinates: np.ndarray, time_pulse: float) -> dict:
        """
        Maps Surrealist reality-melting vectors and magnetic temptation profiles
        across the 640-node environment array.
        """
        logger.info("👁️ SURREALISM: Unlocking subconscious spatial mapping matrix...")
        
        # Define the coordinates of the moving "Temptation Center" (The Forbidden Focus)
        temptation_x = np.sin(time_pulse * 1.5) * 2.0
        temptation_y = np.cos(time_pulse * 1.1) * 2.0
        temptation_center = np.array([temptation_x, temptation_y])

        melted_lasers = np.zeros_like(planar_coordinates)
        temptation_rgb = np.zeros((self.fixture_count, 3), dtype=np.uint8)
        subconscious_dimmers = np.zeros(self.fixture_count, dtype=np.uint8)

        for i in range(self.fixture_count):
            pos = planar_coordinates[i]
            
            # Calculate distance vector pointing directly to the Temptation center
            vector_to_temptation = temptation_center - pos
            distance_to_temptation = np.linalg.norm(vector_to_temptation)
            
            # 1. ANISOTROPIC SPACE MELTING (Vertical spatial sag calculation)
            # Simulates a liquid-like dripping reality along the vertical tracking axis
            melt_coefficient = np.sin(pos[0] * 2.0 + time_pulse) * 0.8
            melted_lasers[i, 0] = pos[0] * 35.0
            melted_lasers[i, 1] = (pos[1] - np.abs(melt_coefficient)) * 35.0  # Force downward "sag"
            
            # 2. TEMPTATION GRAVITY WELL (Seductive pull adjustments)
            # As fixtures get closer to the temptation center, their intensity maximizes
            pull_intensity = np.exp(-0.4 * (distance_to_temptation ** 2))
            subconscious_dimmers[i] = int(100 + pull_intensity * 155)
            
            # 3. SUBCONSCIOUS COLOR SHIFTING (Crimson-Gold vs Cold Shadow)
            if pull_intensity > 0.5:
                # Seductive, warm temptation hues directly enveloping the gravity well
                temptation_rgb[i, 0] = int(255)                                # Pure Crimson Intensity
                temptation_rgb[i, 1] = int(180 * pull_intensity)               # Shimmering Gold blend
                temptation_rgb[i, 2] = int(50)
            else:
                # Cold, surreal, detached subconscious backdrop tones
                shadow_phase = (np.cos(pos[0] + time_pulse * 3.0) + 1.0) * 0.5
                temptation_rgb[i, 0] = int(30 * shadow_phase)
                temptation_rgb[i, 1] = int(10)
                temptation_rgb[i, 2] = int(150 * (1.0 - shadow_phase))        # Deep Subconscious Indigo
                
        logger.info("✨ SURREALISM OPERATIONAL: Subconscious spatial tension fully destabilized.")
        return {
            "melted_laser_tracers": melted_lasers,
            "temptation_dimmers": subconscious_dimmers,
            "surreal_rgb_matrix": temptation_rgb
        }

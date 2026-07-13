# ──────────────────────────────────────────────────────────────────────────
# FILE: core/evanescent_decoupler.py
# ROLE: Evanescent Wave Attenuation & Boundary Isolation Mask Generator
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EvanescentDecoupler")

class EvanescentDecoupler:
    def __init__(self, grid_size: int = 16):
        self.grid_size = grid_size

    def compute_attenuation_profile(self, refractive_index: np.ndarray, incident_angle: float, wavelength: float) -> np.ndarray:
        """
        Calculates the spatial attenuation coefficient alpha across the boundary layer.
        Formula: alpha = (2 * pi / wavelength) * sqrt((n_core * sin(theta))^2 - n_cladding^2)
        """
        logger.info("🛡️ DECOUPLER: Calculating sub-wavelength evanescent attenuation coefficients...")
        
        n_core = np.max(refractive_index)
        n_cladding = np.min(refractive_index)
        
        argument = (n_core * np.sin(incident_angle))**2 - n_cladding**2
        # Ensure we are in the total internal reflection regime (argument > 0)
        argument = np.clip(argument, a_min=0.0, a_max=None)
        
        alpha = (2.0 * np.pi / wavelength) * np.sqrt(argument)
        logger.info(f"🛡️ DECOUPLER: Boundary calculation complete. Peak attenuation factor alpha: {alpha:.4f}")
        return alpha

    def apply_quenching_filter(self, field_tensor: np.ndarray, alpha: float) -> np.ndarray:
        """
        Applies a localized exponential decay envelope to extinguish trailing evanescent tails
        at the outer boundaries of the hypergraph coordinates.
        """
        logger.info("🛡️ DECOUPLER: Enforcing boundary isolation quenching mask...")
        rows, cols = field_tensor.shape
        quenched_tensor = np.copy(field_tensor)
        
        # Apply exponential suppression envelope to the outer grid boundaries (last 2 rows/cols)
        for r in range(rows):
            for c in range(cols):
                distance_to_edge = min(r, c, rows - 1 - r, cols - 1 - c)
                if distance_to_edge <= 2:
                    suppression = np.exp(-alpha * (3 - distance_to_edge))
                    quenched_tensor[r, c] *= suppression
                    
        return quenched_tensor

# ──────────────────────────────────────────────────────────────────────────
# FILE: core/acousto_optic_mixer.py
# ROLE: Photon-Phonon Plasma Interaction & Dynamic Refractive Grating
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AcoustoOpticMixer")

class AcoustoOpticMixer:
    def __init__(self, grid_size: int = 16):
        self.grid_size = grid_size
        # Baseline refractive index of ambient air (n_0)
        self.n_ambient = 1.000293 

    def calculate_plasma_grating(self, photon_intensity: np.ndarray, phonon_pressure: np.ndarray) -> np.ndarray:
        """
        Computes the transient non-linear refractive index map n(x,y) generated 
        by overlapping optical energy and acoustic pressure waves in air plasma.
        """
        logger.info("💥 PLASMA: Mixing photon fields and phonon pressure waves...")
        
        # Stimulated Brillouin component: Sound shifts the physical density of the medium
        photoelastic_coefficient = 0.31
        delta_n_sound = photoelastic_coefficient * phonon_pressure
        
        # Optical Kerr component: High intensity light alters the index via plasma generation
        n2_kerr = 3.2e-19  # m^2/W approximation for air/plasma transition
        delta_n_light = n2_kerr * photon_intensity
        
        # Combined dynamic refractive index matrix
        dynamic_refractive_index = self.n_ambient + delta_n_sound + delta_n_light
        
        # Measure maximum gradient divergence (where diffraction is strongest)
        max_gradient = np.max(np.abs(np.gradient(dynamic_refractive_index)))
        logger.info(f"💥 PLASMA: Grating computed. Peak refractive gradient: {max_gradient:.6e}")
        
        return dynamic_refractive_index

# physics/maxwell_wavefront.py
import numpy as np

class MaxwellWavefront:
    def __init__(self):
        # Physical constants in SI units
        self.mu_0 = 4.0 * np.pi * 1e-7  # Permeability of free space
        self.epsilon_0 = 8.854187817e-12 # Permittivity of free space
        self.c = 1.0 / np.sqrt(self.mu_0 * self.epsilon_0)

    def calculate_phase_velocity(self, local_permeability_matrix: np.ndarray) -> np.ndarray:
        """Computes the localized sub-wavelength propagation velocity across the canvas."""
        return 1.0 / np.sqrt(local_permeability_matrix * self.epsilon_0)

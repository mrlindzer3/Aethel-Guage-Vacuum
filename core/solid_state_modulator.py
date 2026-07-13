# ──────────────────────────────────────────────────────────────────────────
# FILE: core/solid_state_modulator.py
# ROLE: Solid-State Total Internal Reflection (TIR) Wavefront Projector
# ARCHITECTURE: Sub-Wavelength Plasmonic Confinement Emission Pipeline
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SolidStateModulator")

class SolidStateModulator:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        # Setup the dielectric refractive index constant for silica-air interface
        self.n_substrate = 1.45
        self.n_air = 1.00
        # Calculate critical angle for Total Internal Reflection: theta_c = asin(n2 / n1)
        self.critical_angle_rad = np.arcsin(self.n_air / self.n_substrate)

    def compute_plasmonic_emission_field(self, ml_predicted_tensor: np.ndarray, current_positions: np.ndarray) -> dict:
        """
        Calculates the sub-wavelength evanescent scattering vectors required to 
        project the 150MP canvas directly from the substrate surface.
        """
        logger.info("🔦 SOLID-STATE: Computing evanescent wavefront scattering coefficients...")
        
        # Extract the spatial displacement vectors from the neuromorphic reservoir prediction
        melted_x = ml_predicted_tensor[:, 0]
        melted_y = ml_predicted_tensor[:, 1]
        luminescence = np.abs(ml_predicted_tensor[:, 2])
        
        # Initialize wavefront phase profile arrays
        wavefront_phases = np.zeros(self.node_count, dtype=np.float32)
        plasmonic_confinement_nm = np.zeros(self.node_count, dtype=np.float32)
        
        for i in range(self.node_count):
            z_depth = np.abs(current_positions[i, 2])
            
            # 1. EVANESCENT DECAY MODULATION (Field intensity vs depth)
            # Intensity drops exponentially outside the guide: I = I0 * exp(-2 * kappa * z)
            kappa = (2.0 * np.pi / 1.55e-6) * np.sqrt((self.n_substrate ** 2) * (np.sin(self.critical_angle_rad + 0.05) ** 2) - 1.0)
            evanescent_coupling = np.exp(-2.0 * kappa * z_depth)
            
            # 2. SUB-WAVELENGTH CONFINEMENT RATIO
            # Determines the spatial sharpness of the emitting node channel
            plasmonic_confinement_nm[i] = 45.0 * (1.0 - np.tanh(luminescence[i]))
            
            # Calculate the final phase escape profile
            wavefront_phases[i] = np.mod(melted_x[i] * melted_y[i] * evanescent_coupling, 2 * np.pi)
            
        logger.info(f"✨ SOLID-STATE: Wavefront compiled. Sub-wavelength focal point profile: {np.mean(plasmonic_confinement_nm):.2f} nm")
        return {
            "surface_emission_phases": wavefront_phases,
            "confinement_profiles_nm": plasmonic_confinement_nm,
            "solid_state_locked": True
        }

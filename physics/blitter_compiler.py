# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/blitter_compiler.py
# ROLE: Optical Blitter Frequency Mapping Engine
# ARCHITECTURE: Homotopy Path to RF/AOD Control Spectrum Generator
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BlitterCompiler")

class BlitterCompiler:
    def __init__(self, node_count: int = 640, carrier_frequency_thz: float = 375.0):
        self.node_count = node_count
        self.carrier_thz = carrier_frequency_thz # Red-shifted trapping laser baseline

    def compile_blitter_frequencies(self, univalent_positions: np.ndarray, homotopy_profile: dict) -> dict:
        """
        Translates the homotopy path deformations and physical node coordinates
        into a discrete set of RF modulation frequencies for the AOD/SLM hardware.
        """
        logger.info("🪐 BLITTER: Mapping univalent proof paths to RF frequency spectra...")
        
        # Convert the complex-valued unitary matrix transitions into raw spatial phases
        u_matrix = homotopy_profile["u_matrix"]
        phase_angles = np.angle(u_matrix)
        
        # Perform 1D FFT along the spatial dimensions to extract the spatial frequency components
        # This determines the spatial spacing and pitch of our optical trapping grid
        spatial_frequencies = np.fft.rfft(np.mean(phase_angles, axis=0))
        
        # Convert spatial frequencies to physical RF drive frequencies (MHz range)
        # Typically, acousto-optic deflectors operate in the 50 MHz to 150 MHz range
        rf_drive_frequencies = 50.0 + (np.abs(spatial_frequencies[:self.node_count // 2]) * 100.0)
        
        # Map complexity to laser intensity (amplitude) modulation depth
        complexity = homotopy_profile["complexity"]
        modulation_depth = np.clip(complexity / 10.0, 0.0, 1.0)
        
        logger.info(f"🕸️ BLITTER: Spectrum generated. Carrier: {self.carrier_thz} THz. Max Drive RF: {np.max(rf_drive_frequencies):.4f} MHz")
        
        return {
            "rf_frequencies_mhz": rf_drive_frequencies,
            "modulation_depth": modulation_depth,
            "carrier_thz": self.carrier_thz
        }

    def generate_blitter_phase_mask(self, base_space: np.ndarray, blitter_profile: dict) -> np.ndarray:
        """
        Generates the 2D spatial phase hologram mask to be written directly 
        to the liquid crystal panel of the Spatial Light Modulator (SLM).
        """
        rf_freqs = blitter_profile["rf_frequencies_mhz"]
        depth = blitter_profile["modulation_depth"]
        
        # Synthesize a 2D interference grid based on the physical coordinate layout
        x_coords = base_space[:, 0]
        y_coords = base_space[:, 1]
        
        # Generate a synthetic phase mask overlay
        phase_mask = np.sin(x_coords[:, np.newaxis] * rf_freqs[np.newaxis, :20]) * depth
        
        return phase_mask

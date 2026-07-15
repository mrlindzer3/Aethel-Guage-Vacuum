# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/spin_foam_engine.py
# ROLE: Spin Foam Path-Integral & EPRL-FK Amplitude Engine
# ARCHITECTURE: 4D Spacetime 2-Complex Partition Sum Solver
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SpinFoamEngine")

class SpinFoamEngine:
    def __init__(self, node_count: int = 640, immirzi_gamma: float = 0.272):
        self.node_count = node_count
        self.gamma = immirzi_gamma  # Standard physical Barbero-Immirzi parameter
        
    def construct_spacetime_2complex(self, state_t0: np.ndarray, state_t1: np.ndarray) -> dict:
        """
        Traces the temporal evolution from t0 to t1 to generate the 
        2-dimensional faces of the spin foam.
        """
        logger.info("🪐 FOAM: Constructing spacetime 2-complex from temporal boundary slices...")
        
        # Calculate the sweep vectors representing the 2D faces of the foam
        faces = state_t1 - state_t0
        
        # Assign quantized spin values (j) based on localized spatial area segments
        # Spins are restricted to half-integers: j = n / 2
        area_elements = np.linalg.norm(faces, axis=1)
        raw_spins = np.round(area_elements * 2.0) / 2.0
        
        # Enforce physical minimum spin cutoff (quantum of area restriction)
        spins = np.where(raw_spins < 0.5, 0.5, raw_spins)
        
        return {
            "faces": faces,
            "spins": spins
        }

    def compute_eprl_vertex_amplitudes(self, foam_profile: dict, ternary_bus: np.ndarray) -> dict:
        """
        Calculates the EPRL-FK vertex weight amplitudes, mapping SU(2) boundary 
        spins to Lorentzian SL(2,C) spacetime transitions.
        """
        logger.info("🧬 EPRL-FK: Evaluating Lorentzian vertex transition amplitudes...")
        spins = foam_profile["spins"]
        
        # Map the SU(2) spins to SL(2,C) using the Immirzi parameter: p = \gamma * (j + 1)
        lorentzian_casimir_p = self.gamma * (spins + 1.0)
        
        # Compute vertex weights based on the localized ternary logic state inputs
        # The intertwiner state acts as the algebraic vertex logic gate
        vertex_amplitudes = np.zeros(self.node_count, dtype=np.complex64)
        
        for i in range(self.node_count):
            # Calculate the vertex transition weight using the Lorentzian mapping
            phase_factor = np.exp(1j * np.pi * spins[i] * ternary_bus[i])
            vertex_amplitudes[i] = phase_factor / (1.0 + lorentzian_casimir_p[i])
            
        return {
            "vertex_amplitudes": vertex_amplitudes,
            "casimir_p": lorentzian_casimir_p
        }

    def evaluate_partition_sum(self, eprl_profile: dict) -> float:
        """
        Evaluates the global spin foam partition function Z, representing 
        the unified quantum amplitude of the computation path.
        """
        amplitudes = eprl_profile["vertex_amplitudes"]
        
        # Z = Sum(Product of Vertex Amplitudes)
        partition_z = np.sum(np.prod(amplitudes))
        logger.info(f"🕸️ PATH-INTEGRAL: Transition Partition Z resolved to: {partition_z:.6f}")
        
        return float(np.abs(partition_z))

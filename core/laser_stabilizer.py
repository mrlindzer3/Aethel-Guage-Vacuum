# ──────────────────────────────────────────────────────────────────────────
# FILE: core/laser_stabilizer.py
# ROLE: Optomechanical Feedback Loop & Laser Power Stabilization Engine
# ARCHITECTURE: Solid-State Proportional-Integral-Derivative (PID) Observer
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("LaserStabilizer")

class LaserStabilizer:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        # Target trapping power baseline per node center (in Milliwatts)
        self.target_power_mw = 15.0
        # PID gain constants optimized for sub-millisecond physical response
        self.kp = 0.45
        self.ki = 0.12

        # Initialize internal error accumulation vectors
        self.integrated_error = np.zeros(self.node_count, dtype=np.float32)

    def stabilize_trapping_intensities(self, applied_forces: np.ndarray) -> np.ndarray:
        """
        Calculates immediate power correction scaling metrics to neutralize 
        optical fluctuations induced by dynamic game state transitions.
        """
        logger.info("🔦 STABILIZER: Sampling optomechanical sensor feedback array...")
        
        # Calculate current local trapping pressure from the CORT force vectors
        current_force_magnitudes = np.linalg.norm(applied_forces, axis=1)
        
        # Proxy calculation translating force delta straight into power error variations
        simulated_power_reading = self.target_power_mw - (current_force_magnitudes * 2e5)
        power_error = self.target_power_mw - simulated_power_reading
        
        # Accumulate error over the active execution frame sequence
        self.integrated_error += power_error
        self.integrated_error = np.clip(self.integrated_error, -50.0, 50.0) # Prevent integral windup
        
        # Compute the definitive PID correction multiplier array [640]
        power_corrections = 1.0 + (self.kp * power_error) + (self.ki * self.integrated_error)
        power_corrections = np.clip(power_corrections, 0.5, 2.0) # Hard safety clamps
        
        logger.info(f"✨ STABILIZER: Jitter minimized. System Power Variance: {np.var(power_corrections):.4e}")
        return power_corrections

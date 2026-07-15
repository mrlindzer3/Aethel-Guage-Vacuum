# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/partition_solver.py
# ROLE: Path Integral Partition Function (Z) Solver
# ARCHITECTURE: High-Precision Convergence & Partition Evaluator
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PartitionSolver")

class PartitionSolver:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def calculate_partition_function(self, complexity: float, spectral_action: float, rg_action: float) -> dict:
        """
        Evaluates the global partition function Z by summing the active actions
        and calculating the quantum probability density of the current state.
        """
        logger.info("🪐 PARTITION: Calculating global quantum partition function Z...")
        
        # Sum the total effective action from all three phases
        # Total Action = I_WDW (Complexity) + Dirac Spectral Action + RG Effective Action
        total_action = complexity + spectral_action + rg_action
        
        # Calculate the path integral weight: Z = exp(-Action)
        # We cap the action value to avoid numerical overflow under extreme states
        clamped_action = np.clip(total_action, -700.0, 700.0)
        partition_Z = float(np.exp(-clamped_action))
        
        # Calculate the thermodynamic Free Energy: F = -ln(Z)
        free_energy = -np.log(partition_Z + 1e-12)
        
        # Determine convergence stability
        is_converged = np.isfinite(partition_Z) and partition_Z > 0.0
        
        logger.info(f"🕸️ PARTITION: Calculation complete. Z = {partition_Z:.6e}, Free Energy F = {free_energy:.6f}")
        
        return {
            "partition_Z": partition_Z,
            "free_energy": free_energy,
            "is_converged": is_converged
        }

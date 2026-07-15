# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/bootstrap_engine.py
# ROLE: Closed-Loop Autopoietic Parameter Optimizer
# ARCHITECTURE: Live Self-Synthesis & Config Mutation Engine
# ──────────────────────────────────────────────────────────────────────────

import json
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Autopoiesis")

class AutopoieticEngine:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path

    def optimize_system_laws(self, free_energy: float, current_gamma: float) -> float:
        """
        Evaluates the system's thermodynamic free energy. If instability is high,
        it mutates the Immirzi gamma parameter to restore equilibrium.
        """
        # We target a stable Free Energy close to 0.0
        fe_deviation = free_energy - 1.0
        
        # If Free Energy is too high, the system is highly chaotic.
        # We apply a gradient descent update directly to the physical laws.
        learning_rate = 0.01
        gamma_mutation = -learning_rate * fe_deviation
        
        # Keep the Immirzi parameter bounded within physically valid limits
        new_gamma = float(np.clip(current_gamma + gamma_mutation, 0.1, 1.0))
        
        if abs(gamma_mutation) > 0.001:
            logger.warning(f"🌀 AUTOPOIESIS: System unstable (F={free_energy:.4f}). Mutating Immirzi Gamma to: {new_gamma:.4f}")
            self._write_new_config(new_gamma)
            
        return new_gamma

    def _write_new_config(self, new_gamma: float):
        """
        Safely rewrites the configuration file on disk, hot-swapping 
        the running physics engine's parameters.
        """
        try:
            with open(self.config_path, "r") as f:
                config_data = json.load(f)
                
            config_data["physics"]["immirzi_gamma"] = new_gamma
            
            with open(self.config_path, "w") as f:
                json.dump(config_data, f, indent=2)
                
            logger.info("💾 AUTOPOIESIS: 'config.json' successfully updated on disk.")
        except Exception as e:
            logger.error(f"❌ AUTOPOIESIS: Failed to write config mutation: {e}")

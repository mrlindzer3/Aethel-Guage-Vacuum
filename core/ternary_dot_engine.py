# ──────────────────────────────────────────────────────────────────────────
# FILE: core/ternary_dot_engine.py
# ROLE: Co-Located Advanced Ternary Dot-Product Execution Engine
# ARCHITECTURE: Low-Overhead Floating-Point-Free Inference Layer
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
from core.ternary_cla import TernaryCLA
from core.ternary_multiplier import TernaryMultiplier

class TernaryDotEngine:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        self.cla = TernaryCLA(trit_width=node_count)
        self.mult = TernaryMultiplier(width=node_count)

    def compute_dot_product(self, state_matrix: np.ndarray, weights_matrix: np.ndarray) -> np.ndarray:
        """
        Processes multi-trit spatial vectors through an inline weight matrix step.
        Eliminates power-hungry IEEE-754 floating-point hardware requirements.
        """
        # Convert floating point values down to quantized ternary integers [-1, 0, 1]
        quantized_states = np.sign(state_matrix).astype(np.int8)
        quantized_weights = np.sign(weights_matrix).astype(np.int8)
        
        output_projection = np.zeros_like(state_matrix)
        
        # Execute parallel row-by-column scaling matrices using advanced ternary arithmetic
        for axis in range(3):
            scaled_vector = self.mult.multiply_trit_vectors(quantized_states[:, axis], quantized_weights[axis])
            output_projection[:, axis] = self.cla.compute_parallel_addition(output_projection[:, axis], scaled_vector)
            
        return output_projection

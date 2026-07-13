# ──────────────────────────────────────────────────────────────────────────
# FILE: core/ternary_logic_unit.py
# ROLE: Balanced Ternary Logic Unit (TLU) Gate Emulator
# ARCHITECTURE: Non-Von Neumann Qutrit Mathematical Processor
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TernaryLogic")

class TernaryLogicUnit:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def gate_not(self, trit_array: np.ndarray) -> np.ndarray:
        """Inverts the balanced ternary states across the zero equilibrium axis."""
        return -1 * trit_array

    def gate_and(self, array_a: np.ndarray, array_b: np.ndarray) -> np.ndarray:
        """Executes a Ternary minimum gate step across paired node arrays."""
        return np.minimum(array_a, array_b)

    def gate_or(self, array_a: np.ndarray, array_b: np.ndarray) -> np.ndarray:
        """Executes a Ternary maximum gate step across paired node arrays."""
        return np.maximum(array_a, array_b)

    def ternary_half_adder(self, array_a: np.ndarray, array_b: np.ndarray) -> dict:
        """
        Computes balanced ternary addition for two qutrit arrays.
        Returns both the definitive Sum and Carry vectors without binary sign flags.
        """
        logger.info("🧮 TLU: Computing parallel balanced ternary addition pass...")
        
        # Linear raw arithmetic combination
        raw_sum = array_a + array_b
        
        # Initialize output trit states
        sum_trits = np.zeros(self.node_count, dtype=np.int8)
        carry_trits = np.zeros(self.node_count, dtype=np.int8)
        
        # Truth routing mapping based on balanced ternary addition rules
        # Input sums can range from -2 to +2
        for i in range(self.node_count):
            s = raw_sum[i]
            if s == 2:    # 1 + 1 = 2 -> Sum: -1, Carry: 1 (Since 3 - 1 = 2)
                sum_trits[i], carry_trits[i] = -1, 1
            elif s == 1:  # 1 + 0 = 1 -> Sum: 1, Carry: 0
                sum_trits[i], carry_trits[i] = 1, 0
            elif s == 0:  # 0 + 0 = 0 -> Sum: 0, Carry: 0
                sum_trits[i], carry_trits[i] = 0, 0
            elif s == -1: # -1 + 0 = -1 -> Sum: -1, Carry: 0
                sum_trits[i], carry_trits[i] = -1, 0
            elif s == -2: # -1 + -1 = -2 -> Sum: 1, Carry: -1 (Since -3 + 1 = -2)
                sum_trits[i], carry_trits[i] = 1, -1
                
        return {"sum": sum_trits, "carry": carry_trits}

# ──────────────────────────────────────────────────────────────────────────
# FILE: core/clock_generator.py
# ROLE: High-Frequency Hardware Clock Synchronization & Phase-Lock Loop (PLL)
# ARCHITECTURE: 200 Hz Temporal Frame-Budget Enforcement Controller
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ClockGenerator")

class ClockGenerator:
    def __init__(self, target_frequency_hz: float = 200.0):
        self.target_hz = target_frequency_hz
        self.frame_budget_sec = 1.0 / target_frequency_hz  # Exactly 0.005 seconds (5.0 ms)
        self.last_tick = time.perf_counter()

    def synchronize_hardware_bus(self) -> float:
        """
        Calculates execution delta since the last tick and applies a precision 
        delay if the software loop completed ahead of the 5.0ms hardware deadline.
        """
        current_time = time.perf_counter()
        elapsed = current_time - self.last_tick
        
        # Enforce strict hard-deadline timing alignment
        if elapsed < self.frame_budget_sec:
            sleep_needed = self.frame_budget_sec - elapsed
            # High-resolution spin-lock style delay for sub-millisecond precision
            target_time = current_time + sleep_needed
            while time.perf_counter() < target_time:
                pass
            
        final_time = time.perf_counter()
        frame_time_ms = (final_time - self.last_tick) * 1000.0
        
        # Reset master heartbeat timestamp
        self.last_tick = final_time
        logger.info(f"⏱️ CLOCK: Pulse Emitted. Master Cycle: {frame_time_ms:.2f} ms | Frame Lock: {1000.0 / frame_time_ms:.1f} Hz")
        return frame_time_ms

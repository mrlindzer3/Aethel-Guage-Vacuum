# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/hal_interface.py
# ROLE: Hardware Abstraction Layer & Data Exporter
# ARCHITECTURE: Math-to-Physical Output Bridge (JSON / Binary / Control)
# ──────────────────────────────────────────────────────────────────────────

import json
import struct
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("HardwareInterface")

class HardwareAbstractionLayer:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count

    def export_to_json(self, positions: np.ndarray, rf_frequencies: np.ndarray) -> str:
        """
        Serializes the coordinate matrix and synthesized RF frequencies into 
        a web-standard JSON format for web visualizers (like Three.js).
        """
        data = {
            "node_count": self.node_count,
            "positions": positions.tolist(),
            "rf_frequencies_mhz": rf_frequencies.tolist()
        }
        return json.dumps(data)

    def export_to_binary_packet(self, positions: np.ndarray, rf_frequencies: np.ndarray) -> bytes:
        """
        Serializes the coordinates and RF frequencies into a high-speed, 
        compact binary packet to stream directly over UDP to real DAC/AOD hardware.
        """
        # Header: 'AGV' signature (3 bytes) + node count (uint32)
        header = struct.pack("!3sI", b"AGV", self.node_count)
        
        # Flatten the positions matrix and convert to float32 bytes
        flat_positions = positions.astype(np.float32).tobytes()
        
        # Convert RF frequencies to float32 bytes
        flat_frequencies = rf_frequencies.astype(np.float32).tobytes()
        
        return header + flat_positions + flat_frequencies

    def simulate_hardware_write(self, positions: np.ndarray, rf_frequencies: np.ndarray):
        """
        Simulates writing to an acousto-optic deflector (AOD) and 
        piezo-controlled optical tweezers.
        """
        mean_offset = np.mean(positions, axis=0)
        peak_rf = np.max(rf_frequencies)
        
        logger.info("📡 HAL: Outputting signals to physical ports...")
        logger.info(f"   ↳ Trapping Laser Center of Mass: x={mean_offset[0]:.4f}, y={mean_offset[1]:.4f}")
        logger.info(f"   ↳ AOD RF Driver Amplitude Peak: {peak_rf:.4f} MHz")

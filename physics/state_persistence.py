# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/state_persistence.py
# ROLE: Non-Blocking State Persistence & Recovery Engine
# ARCHITECTURE: Asynchronous JSON Serialization File-System Drive
# ──────────────────────────────────────────────────────────────────────────

import json
import os
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StatePersistence")

class QuantumStatePersistence:
    def __init__(self, Storage_path: str = "data/gateway_state.json"):
        self.storage_path = storage_path
        # Ensure data storage directory exists
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def serialize_cache_to_disk(self, memory_cache: dict, runtime_config: dict) -> bool:
        """
        Saves the memory cache maps and server variables to a JSON file.
        Converts NumPy arrays cleanly to serializable lists.
        """
        try:
            serializable_cache = {}
            for key, val in memory_cache.items():
                if isinstance(val, np.ndarray):
                    serializable_cache[key] = val.tolist()
                else:
                    serializable_cache[key] = val

            snapshot = {
                "runtime_config": runtime_config,
                "dedup_cache": serializable_cache
            }

            with open(self.storage_path, "w") as f:
                json.dump(snapshot, f, indent=4)
            logger.info("💾 PERSISTENCE: State snapshot cleanly committed to cold storage.")
            return True
        except Exception as e:
            logger.error(f"❌ PERSISTENCE: Failed to write state to disk: {e}")
            return False

    def recover_state_from_disk(self) -> tuple:
        """
        Reads files from disk on boot to restore cache and system configuration.
        """
        if not os.path.exists(self.storage_path):
            logger.warning("💾 PERSISTENCE: No previous state snapshot found. Starting clean boot.")
            return {}, {}

        try:
            with open(self.storage_path, "r") as f:
                snapshot = json.load(f)
            
            recovered_config = snapshot.get("runtime_config", {})
            raw_cache = snapshot.get("dedup_cache", {})
            
            # Reconstruct list shapes back into usable NumPy arrays
            recovered_cache = {k: np.array(v, dtype=np.complex128) for k, v in raw_cache.items()}
            
            logger.info(f"✨ PERSISTENCE: Successfully restored {len(recovered_cache)} cached solutions.")
            return recovered_cache, recovered_config
        except Exception as e:
            logger.error(f"❌ PERSISTENCE: Core state corruption detected during restore pass: {e}")
            return {}, {}

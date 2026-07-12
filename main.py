# ──────────────────────────────────────────────────────────────────────────
# FILE: main.py
# ROLE: Global Orchestration Entry Point for the Resonance Holography Stack
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import sys
import logging
from core.holographic_matrix_conductor import HolographicMatrixConductor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AethelGaugeVacuumMain")

def main():
    logger.info("🌌 START: Bootstrapping Aethel Gauge Vacuum Simulation Stack...")
    
    try:
        # Initialize the global orchestration loop conductor
        conductor = HolographicMatrixConductor()
        
        # Execute the unified quantum field and AI optimization pass
        success = conductor.run_holographic_loop()
        
        if success:
            logger.info("🚀 SYSTEM: Global holographic synchronization pass completed nominally.")
        else:
            logger.warning("⚠️ SYSTEM: Synchronization loop completed with non-fatal field variances.")
            
    except Exception as e:
        logger.critical(f"❌ CRITICAL: System crash detected in global orchestration loop: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

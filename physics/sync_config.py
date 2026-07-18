# ──────────────────────────────────────────────────────────────────────────
# FILE: physics/sync_config.py
# ROLE: Global Causal-Temporal Sync Configuration
# ──────────────────────────────────────────────────────────────────────────

SYNC_CONFIG = {
    "temporal_throttle_min": 0.5,      # Throttling floor if convergence drops
    "convergence_threshold": 0.992,   # Global lock for visual state updates
    "telemetry_log_rate": 60,         # Log fidelity every 60 frames
    "jitters_shield_mode": True,      # Enable causal-jitter suppression
    "rendering_lock": "STRICT"        # Freeze visuals if fidelity < convergence
}

def apply_sync_settings(core_instance):
    """
    Applies the synchronization configuration to the active Quantum Core.
    """
    core_instance.sync_throttle_min = SYNC_CONFIG["temporal_throttle_min"]
    core_instance.fidelity_gate = SYNC_CONFIG["convergence_threshold"]
    
    if SYNC_CONFIG["jitters_shield_mode"]:
        print("🌀 SYNC: Causal jitter suppression enabled.")
        
    print(f"✅ SYNC: Core initialized. Convergence Gate: {SYNC_CONFIG['convergence_threshold']}")

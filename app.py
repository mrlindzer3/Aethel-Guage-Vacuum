# ──────────────────────────────────────────────────────────────────────────
# FILE: app.py
# ROLE: FastAPI Bidirectional API Server
# ARCHITECTURE: Read/Write State Controller
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from physics.unified_core import UnifiedQuantumCore

app = FastAPI(title="Aethel-Gauge-Vacuum Interactive API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NODE_COUNT = 640
core_engine = UnifiedQuantumCore(node_count=NODE_COUNT)
positions = np.random.normal(0.0, 1.0, (NODE_COUNT, 3))
previous_positions = positions.copy()

# Dynamic runtime configurations that the browser can update
runtime_config = {
    "gamma": 0.272,
    "refractive_multiplier": 1.0,
    "gravity_G": 1.0
}

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.get("/api/substrate")
def get_substrate_data():
    """Generates next frame applying the dynamic runtime configs."""
    global positions, previous_positions
    
    # Dynamic parameter injection
    core_engine.gamma = runtime_config["gamma"]
    core_engine.running_G = runtime_config["gravity_G"]
    
    ternary_input_bus = np.random.choice([-1, 0, 1], size=NODE_COUNT)
    
    positions, rf_frequencies = core_engine.execute_frame(
        current_positions=positions,
        previous_positions=previous_positions,
        ternary_bus=ternary_input_bus
    )
    previous_positions = positions.copy()
    
    # Scale frequencies by user's refractive multiplier
    adjusted_frequencies = rf_frequencies * runtime_config["refractive_multiplier"]
    
    return {
        "status": "STABLE_LANDSCAPE",
        "positions": positions.tolist(),
        "rf_frequencies_mhz": adjusted_frequencies.tolist(),
        "current_laws": runtime_config
    }

@app.post("/api/config")
def update_config(payload: dict = Body(...)):
    """Receives live parameters from the browser dashboard and updates the engine."""
    global runtime_config
    runtime_config["gamma"] = float(payload.get("gamma", runtime_config["gamma"]))
    runtime_config["refractive_multiplier"] = float(payload.get("refractive_multiplier", runtime_config["refractive_multiplier"]))
    runtime_config["gravity_G"] = float(payload.get("gravity_G", runtime_config["gravity_G"]))
    return {"status": "SUCCESS", "updated_laws": runtime_config}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

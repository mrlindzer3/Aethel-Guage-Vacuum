# ──────────────────────────────────────────────────────────────────────────
# FILE: app.py
# ROLE: FastAPI Web Server & Physics API
# ARCHITECTURE: High-Performance Client-Server Bridge
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from physics.unified_core import UnifiedQuantumCore

app = FastAPI(title="Aethel-Gauge-Vacuum API")

# Enable CORS so your web browser can talk to the local API safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our state-of-the-art physics core
NODE_COUNT = 640
core_engine = UnifiedQuantumCore(node_count=NODE_COUNT)
positions = np.random.normal(0.0, 1.0, (NODE_COUNT, 3))
previous_positions = positions.copy()

@app.get("/")
def serve_frontend():
    """Serves your 3D interactive visualizer directly from the server."""
    return FileResponse("index.html")

@app.get("/api/substrate")
def get_substrate_data():
    """
    Calculates the next evolutionary frame of the Fate Crystal 
    and returns the 3D coordinates and RF frequencies as JSON.
    """
    global positions, previous_positions
    
    # Simulate the incoming ternary data stream
    ternary_input_bus = np.random.choice([-1, 0, 1], size=NODE_COUNT)
    
    # Run the unified physics pass
    positions, rf_frequencies = core_engine.execute_frame(
        current_positions=positions,
        previous_positions=previous_positions,
        ternary_bus=ternary_input_bus
    )
    previous_positions = positions.copy()
    
    # Return clean, production-ready JSON data
    return {
        "status": "STABLE_LANDSCAPE",
        "node_count": NODE_COUNT,
        "positions": positions.tolist(),
        "rf_frequencies_mhz": rf_frequencies.tolist()
    }

# Programmatic entry point so you can run this with a simple play button in your IDE
if __name__ == "__main__":
    import uvicorn
    print("⚡ Starting Aethel-Gauge-Vacuum Web Service on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

# ──────────────────────────────────────────────────────────────────────────
# FILE: app.py
# ROLE: FastAPI WebSocket Server with Shockwave Event Handler
# ARCHITECTURE: Persistent Async Bi-directional Stream Engine
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from physics.unified_core import UnifiedQuantumCore

app = FastAPI(title="Aethel-Gauge-Vacuum Interactive WebSocket Server")

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

# Dynamic runtime configurations
runtime_config = {
    "gamma": 0.272,
    "refractive_multiplier": 1.0,
    "gravity_G": 1.0,
    "shockwave_active": False  # New transient state
}

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global positions, previous_positions, runtime_config
    await websocket.accept()
    print("🔌 WEBSOCKET: Client connected to quantum control channel.")
    
    try:
        async def receive_configs():
            global runtime_config
            while True:
                data = await websocket.receive_text()
                payload = json.loads(data)
                
                # Handle continuous slider adjustments
                runtime_config["gamma"] = float(payload.get("gamma", runtime_config["gamma"]))
                runtime_config["refractive_multiplier"] = float(payload.get("refractive_multiplier", runtime_config["refractive_multiplier"]))
                runtime_config["gravity_G"] = float(payload.get("gravity_G", runtime_config["gravity_G"]))
                
                # Handle transient shockwave button press
                if payload.get("trigger_shockwave"):
                    runtime_config["shockwave_active"] = True

        asyncio.create_task(receive_configs())

        while True:
            core_engine.gamma = runtime_config["gamma"]
            core_engine.running_G = runtime_config["gravity_G"]
            
            # Inject the shockwave state directly into our math bus if active
            ternary_input_bus = np.random.choice([-1, 0, 1], size=NODE_COUNT)
            if runtime_config["shockwave_active"]:
                # Force maximum coherent polarization in the ternary array to feed the wormhole
                ternary_input_bus = np.ones(NODE_COUNT)
            
            # Run the unified physics pass
            positions, rf_frequencies = core_engine.execute_frame(
                current_positions=positions,
                previous_positions=previous_positions,
                ternary_bus=ternary_input_bus
            )
            previous_positions = positions.copy()
            
            adjusted_frequencies = rf_frequencies * runtime_config["refractive_multiplier"]
            
            # Build the transmission packet
            frame_packet = {
                "positions": positions.tolist(),
                "rf_frequencies_mhz": adjusted_frequencies.tolist(),
                "current_laws": {
                    "gamma": runtime_config["gamma"],
                    "refractive_multiplier": runtime_config["refractive_multiplier"],
                    "gravity_G": runtime_config["gravity_G"],
                    "shockwave_active": runtime_config["shockwave_active"]
                }
            }
            await websocket.send_text(json.dumps(frame_packet))
            
            # Reset shockwave immediately so it acts as a single, transient pulse
            if runtime_config["shockwave_active"]:
                runtime_config["shockwave_active"] = False
                
            await asyncio.sleep(0.05)
            
    except WebSocketDisconnect:
        print("🔌 WEBSOCKET: Client disconnected cleanly.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# ──────────────────────────────────────────────────────────────────────────
# FILE: app.py
# ROLE: Enterprise Server with Metcalfe-Reed Dynamic Bandwidth Governor
# ARCHITECTURE: Self-Throttling Real-Time Streaming Engine
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from physics.unified_core import UnifiedQuantumCore

app = FastAPI(title="AGV Enterprise Server - Metcalfe-Reed Governor Edition")

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

PRESETS_FILE = "presets.json"
runtime_config = {
    "gamma": 0.272,
    "refractive_multiplier": 1.0,
    "gravity_G": 1.0,
    "shockwave_active": False
}

def load_presets_from_disk() -> dict:
    if not os.path.exists(PRESETS_FILE):
        default_presets = {
            "Default Core": {"gamma": 0.272, "refractive_multiplier": 1.0, "gravity_G": 1.0},
            "Hyper-Gravity": {"gamma": 0.15, "refractive_multiplier": 0.8, "gravity_G": 4.5},
            "Quantum Scramble": {"gamma": 0.95, "refractive_multiplier": 2.5, "gravity_G": 0.2}
        }
        with open(PRESETS_FILE, "w") as f:
            json.dump(default_presets, f, indent=4)
        return default_presets
    try:
        with open(PRESETS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.get("/api/presets")
def get_presets():
    return load_presets_from_disk()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global positions, previous_positions, runtime_config
    await websocket.accept()
    print("🔌 WEBSOCKET: Client connected with active Metcalfe-Reed Governor.")
    
    try:
        async def receive_configs():
            global runtime_config
            while True:
                data = await websocket.receive_text()
                payload = json.loads(data)
                action = payload.get("action")
                
                if action == "update_state":
                    runtime_config["gamma"] = float(payload.get("gamma", runtime_config["gamma"]))
                    runtime_config["refractive_multiplier"] = float(payload.get("refractive_multiplier", runtime_config["refractive_multiplier"]))
                    runtime_config["gravity_G"] = float(payload.get("gravity_G", runtime_config["gravity_G"]))
                    if payload.get("trigger_shockwave"):
                        runtime_config["shockwave_active"] = True
                        
                elif action == "save_preset":
                    preset_name = payload.get("name")
                    preset_data = payload.get("values")
                    presets = load_presets_from_disk()
                    presets[preset_name] = preset_data
                    with open(PRESETS_FILE, "w") as f:
                        json.dump(presets, f, indent=4)

        asyncio.create_task(receive_configs())

        # Network loop variables
        base_interval = 0.03  # Fast 33 FPS target
        
        while True:
            core_engine.gamma = runtime_config["gamma"]
            core_engine.running_G = runtime_config["gravity_G"]
            
            ternary_input_bus = np.random.choice([-1, 0, 1], size=NODE_COUNT)
            if runtime_config["shockwave_active"]:
                ternary_input_bus = np.ones(NODE_COUNT)
            
            positions, rf_frequencies = core_engine.execute_frame(
                current_positions=positions,
                previous_positions=previous_positions,
                ternary_bus=ternary_input_bus
            )
            previous_positions = positions.copy()
            
            # ──────────────────────────────────────────────────────────────
            # METCALFE-REED BANDWIDTH GOVERNOR
            # ──────────────────────────────────────────────────────────────
            # Calculate physical cluster closeness (entropy approximation)
            variance = np.var(positions, axis=0)
            spatial_cohesion = 1.0 / (np.mean(variance) + 1e-5)
            
            # Metcalfe connection count: n * (n-1) / 2
            metcalfe_val = (NODE_COUNT * (NODE_COUNT - 1)) / 2
            
            # Reed group potential scales exponentially based on physical clustering intensity
            reed_exponent = np.clip(spatial_cohesion * 10, 1.0, 12.0)
            reed_val_log = NODE_COUNT * reed_exponent
            
            # Dynamically adjust websocket frame sleep interval based on network congestion risks
            if spatial_cohesion > 1.5:  # High clustering (Reed Regime)
                # Group-forming dominates; stream slightly slower to allow clients to render heavier groups
                dynamic_interval = base_interval * 1.8
                stream_mode = "REED_CLUSTER"
            else:  # Scattered nodes (Metcalfe Regime)
                dynamic_interval = base_interval
                stream_mode = "METCALFE_P2P"
            
            adjusted_frequencies = rf_frequencies * runtime_config["refractive_multiplier"]
            
            frame_packet = {
                "positions": positions.tolist(),
                "rf_frequencies_mhz": adjusted_frequencies.tolist(),
                "current_laws": {
                    "gamma": runtime_config["gamma"],
                    "refractive_multiplier": runtime_config["refractive_multiplier"],
                    "gravity_G": runtime_config["gravity_G"],
                    "shockwave_active": runtime_config["shockwave_active"]
                },
                "network_metrics": {
                    "mode": stream_mode,
                    "cohesion": float(spatial_cohesion),
                    "metcalfe_val": int(metcalfe_val),
                    "reed_log_potential": float(reed_val_log)
                }
            }
            await websocket.send_text(json.dumps(frame_packet))
            
            if runtime_config["shockwave_active"]:
                runtime_config["shockwave_active"] = False
                
            await asyncio.sleep(dynamic_interval)
            
    except WebSocketDisconnect:
        print("🔌 WEBSOCKET: Client disconnected cleanly.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

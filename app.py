# ──────────────────────────────────────────────────────────────────────────
# FILE: app.py
# ROLE: FastAPI WebSocket Server with Dynamic Cluster Tracking
# ARCHITECTURE: Real-Time Telemetry & Group Analysis Pipeline
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from physics.unified_core import UnifiedQuantumCore
from physics.chronal_shield import ChronalContainmentShield
from physics.cluster_tracker import TopologicalClusterTracker  # Import Tracker

app = FastAPI(title="AGV Mission Control - Cluster Tracking Core")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

NODE_COUNT = 640
core_engine = UnifiedQuantumCore(node_count=NODE_COUNT)
shield_engine = ChronalContainmentShield(node_count=NODE_COUNT)
tracker_engine = TopologicalClusterTracker(target_clusters=8) # 8 core centers

positions = np.random.normal(0.0, 1.0, (NODE_COUNT, 3))
previous_positions = positions.copy()

runtime_config = {
    "gamma": 0.272, "refractive_multiplier": 1.0, "gravity_G": 1.0, "shockwave_active": False, "safety_factor": 2.0
}

@app.get("/")
def serve_frontend(): return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global positions, previous_positions, runtime_config
    await websocket.accept()
    
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
                    runtime_config["safety_factor"] = float(payload.get("safety_factor", runtime_config["safety_factor"]))
                    if payload.get("trigger_shockwave"): runtime_config["shockwave_active"] = True

        asyncio.create_task(receive_configs())
        base_interval = 0.03
        
        while True:
            core_engine.gamma = runtime_config["gamma"]
            core_engine.running_G = runtime_config["gravity_G"]
            
            ternary_input_bus = np.random.choice([-1, 0, 1], size=NODE_COUNT)
            if runtime_config["shockwave_active"]: ternary_input_bus = np.ones(NODE_COUNT)
            
            positions, rf_frequencies = core_engine.execute_frame(
                current_positions=positions, previous_positions=previous_positions, ternary_bus=ternary_input_bus
            )
            previous_positions = positions.copy()
            
            leakage = shield_engine.analyze_leakage_gradient(positions, runtime_config)
            attenuation, _ = shield_engine.calculate_shield_damping(leakage, runtime_config["safety_factor"])
            positions *= attenuation
            
            variance = np.var(positions, axis=0)
            spatial_cohesion = 1.0 / (np.mean(variance) + 1e-5)
            
            # Determine scaling mode and conditionally track cluster centroids
            centroids = []
            if spatial_cohesion > 1.5:
                stream_mode = "REED_CLUSTER"
                centroids = tracker_engine.extract_centroids(positions) # Extract groups!
                dynamic_interval = base_interval * 1.8
            else:
                stream_mode = "METCALFE_P2P"
                dynamic_interval = base_interval
            
            await websocket.send_text(json.dumps({
                "positions": positions.tolist(),
                "centroids": centroids, # Send centroids to browser UI
                "rf_frequencies_mhz": (rf_frequencies * runtime_config["refractive_multiplier"]).tolist(),
                "current_laws": runtime_config,
                "network_metrics": {
                    "mode": stream_mode,
                    "cohesion": float(spatial_cohesion),
                    "metcalfe_val": int((NODE_COUNT * (NODE_COUNT - 1)) / 2),
                    "reed_log_potential": float(NODE_COUNT * np.clip(spatial_cohesion * 10, 1.0, 12.0))
                },
                "shield_metrics": { "leakage": float(leakage), "attenuation": float(attenuation) }
            }))
            await asyncio.sleep(dynamic_interval)
            
    except WebSocketDisconnect: pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# Insert this billing governor inside your app.py WebSocket loop under the CTC handler:

if payload.get("run_ctc"):
    flat_coords = positions.flatten()
    ctc_result = core_engine.run_temporal_computation(flat_coords)
    
    # Financial metrics calculations
    compute_complexity_factor = ctc_result["temporal_fidelity"] * 100
    estimated_classical_hours_saved = float(compute_complexity_factor * 14.5)
    billing_charge_usd = estimated_classical_hours_saved * 150.00 # $150/hour rate
    
    await websocket.send_text(json.dumps({
        "ctc_event": True,
        "resolved_vector": ctc_result["resolved_state_vector"],
        "temporal_fidelity": ctc_result["temporal_fidelity"],
        "billing_metrics": {
            "hours_saved": estimated_classical_hours_saved,
            "invoice_accumulated_usd": billing_charge_usd
        }
    }))

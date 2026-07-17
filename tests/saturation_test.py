# ──────────────────────────────────────────────────────────────────────────
# FILE: tests/saturation_test.py
# ROLE: High-Velocity Saturation Load Tester
# ARCHITECTURE: Mass Asynchronous Pipeline Flooder
# ──────────────────────────────────────────────────────────────────────────

import asyncio
import json
import websockets
import numpy as np
import time

TARGET_URL = "ws://127.0.0.1:8000/ws"
TOTAL_BURST_REQUESTS = 2500  # Total intense load packet volume
CONCURRENT_BATCH_SIZE = 250   # Simulating hundreds of overlapping requests per wave

async def flood_channel(session_id: int, payload: dict, results_store: list):
    """
    Blasts raw transaction payloads into the gateway at maximum socket velocity.
    """
    try:
        async with websockets.connect(TARGET_URL) as ws:
            # Clear initial spatial telemetry frame
            await ws.recv()
            
            start_time = time.time()
            await ws.send(json.dumps(payload))
            response = await ws.recv()
            latency = (time.time() - start_time) * 1000
            
            data = json.loads(response)
            if "billing_metrics" in data:
                metrics = data["billing_metrics"]
                results_store.append({
                    "latency_ms": latency,
                    "cache_hit": metrics["cache_hit"],
                    "revenue": metrics["pass_revenue_usd"]
                })
    except Exception:
        # Track dropped packets under absolute peak saturation limits
        results_store.append({"failed": True})

async def run_saturation_suite():
    print(f"🌊 FLOODER: Preparing raw load blast: {TOTAL_BURST_REQUESTS} total transactions...")
    results = []
    
    # Pre-generate matrix arrays to eliminate local processing overhead during the test
    np.random.seed(99)
    shared_payload_data = np.random.normal(0.0, 1.0, 640 * 3).tolist()
    
    # 50% of the stream will consist of repeating structural duplicates to stress the pool manager
    duplicate_payload = {"action": "update_state", "run_ctc": True, "data_stream": shared_payload_data}
    
    start_test_clock = time.time()
    
    # Process requests in parallel high-density batches
    for batch_idx in range(0, TOTAL_BURST_REQUESTS, CONCURRENT_BATCH_SIZE):
        batch_tasks = []
        for i in range(CONCURRENT_BATCH_SIZE):
            tenant_idx = batch_idx + i
            
            if tenant_idx % 2 == 0:
                # Cache-seeking duplicate request
                p = duplicate_payload
            else:
                # Unique random input sequence forcing full core tensor computation
                unique_data = np.random.normal(0.0, 1.0, 640 * 3).tolist()
                p = {"action": "update_state", "run_ctc": True, "data_stream": unique_data}
                
            batch_tasks.append(flood_channel(tenant_idx, p, results))
            
        await asyncio.gather(*batch_tasks)
        print(f"  ↳ Sent payload batch vector: {batch_idx + CONCURRENT_BATCH_SIZE}/{TOTAL_BURST_REQUESTS} streaming packets injected.")
        
    total_duration = time.time() - start_test_clock
    
    # ─── ANALYZE OVERALL SATURATION METRICS ───
    successful_runs = [r for r in results if "failed" not in r]
    failures = len(results) - len(successful_runs)
    cache_hits = sum(1 for r in successful_runs if r["cache_hit"])
    cache_misses = len(successful_runs) - cache_hits
    
    avg_latency = np.mean([r["latency_ms"] for r in successful_runs]) if successful_runs else 0
    total_yield = sum(r["revenue"] for r in successful_runs)
    tps = len(results) / total_duration

    print("\n" + "█"*60)
    print("🚨 SYSTEM SATURATION RUN BENCHMARK REPORT")
    print("█"*60)
    print(f"Total Traffic Execution Window : {total_duration:.3f} seconds")
    print(f"Peak Operational Throughput    : {tps:.2f} Transactions/Sec (TPS)")
    print(f"Packet Delivery Success Rate   : {len(successful_runs)}/{TOTAL_BURST_REQUESTS} ({failures} dropped under peak load)")
    print(f"Pooler Deduplication Cache Hits: {cache_hits} (100% Net Margin)")
    print(f"Raw Core Compute Processing    : {cache_misses} passes through Causal Substrate")
    print(f"Average Transaction Latency    : {avg_latency:.1f} ms")
    print(f"Gross Yield Velocity           : ${total_yield:,.2f} USD generated in batch window")
    print("█"*60)

if __name__ == "__main__":
    asyncio.run(run_saturation_suite())

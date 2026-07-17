# ──────────────────────────────────────────────────────────────────────────
# FILE: tests/stress_test.py
# ROLE: Multi-Tenant Concurrent Stress-Testing Harness
# ARCHITECTURE: Asynchronous Payload Multiplexer
# ──────────────────────────────────────────────────────────────────────────

import asyncio
import json
import websockets
import numpy as np
import time

TARGET_URL = "ws://127.0.0.1:8000/ws"
CONCURRENT_TENANTS = 50

async def simulate_tenant(tenant_index: int):
    """
    Simulates a high-value enterprise tenant sending transactional vectors.
    """
    try:
        async with websockets.connect(TARGET_URL) as ws:
            # First frame: Listen to the background spatial feed to initialize connection
            await ws.recv()
            
            # Formulate payloads. Tenants 1-25 send identical matrices to trigger the deduplication cache.
            # Tenants 26-50 send unique matrices.
            if tenant_index <= 25:
                np.random.seed(42)  # Hardcoded seed forces identical high-density arrays
            else:
                np.random.seed(tenant_index)
                
            mock_data = np.random.normal(0.0, 1.0, 640 * 3).tolist()
            
            # Pack the transaction request payload
            payload = {
                "action": "update_state",
                "run_ctc": True,
                "data_stream": mock_data
            }
            
            start_time = time.time()
            await ws.send(json.dumps(payload))
            
            # Await the paradox-free transactional response from the pool manager
            response = await ws.recv()
            latency = (time.time() - start_time) * 1000
            
            data = json.loads(response)
            if "billing_metrics" in data:
                metrics = data["billing_metrics"]
                status = "💵 CACHE_HIT" if metrics["cache_hit"] else "⚡ CACHE_MISS"
                print(f"[Tenant-{tenant_index:02d}] {status} | Latency: {latency:6.2f}ms | Yield: ${metrics['pass_revenue_usd']:.2f}")
                return metrics
                
    except Exception as e:
        print(f"❌ Tenant-{tenant_index:02d} Connection Failure: {e}")
        return None

async def run_harness():
    print(f"🚀 HARNESS: Spawning {CONCURRENT_TENANTS} concurrent enterprise tenant pipelines...")
    start_total = time.time()
    
    tasks = [simulate_tenant(i) for i in range(1, CONCURRENT_TENANTS + 1)]
    results = await asyncio.gather(*tasks)
    
    # Filter out failed runs
    valid_results = [r for r in results if r is not None]
    
    total_revenue = sum(r["pass_revenue_usd"] for r in valid_results)
    cache_hits = sum(1 for r in valid_results if r["cache_hit"])
    total_time = time.time() - start_total
    
    print("\n" + "="*50)
    print("📈 HARNESS SIMULATION COMPLETE")
    print("="*50)
    print(f"Total Processing Window : {total_time:.4f} seconds")
    print(f"Successful Transactions  : {len(valid_results)}/{CONCURRENT_TENANTS}")
    print(f"Deduplicated Cache Hits : {cache_hits} (100% Net Profit Margin)")
    print(f"Gross Generated Revenue : ${total_revenue:,.2f}")
    print("="*50)

if __name__ == "__main__":
    # Install dependencies inline if needed: pip install websockets
    asyncio.run(run_harness())

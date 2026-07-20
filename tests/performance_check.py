import sys
import types
import argparse

from test_solid_state_fabric import run_performance_benchmark


class Dummy:
    def __init__(self, *_, **__):
        pass

    def process_player_input(self, positions, **_):
        return positions

    def execute_unified_trapping_pass(self, *_, **__):
        return {"applied_force_tensors": None}

    def execute_reservoir_prediction_step(self, *_, **__):
        return None

    def compute_plasmonic_emission_field(self, *_, **__):
        return None

    def generate_portal_distortion_field(self, *_, **__):
        return None

    def generate_euphoric_pulsing_vectors(self, *_, **__):
        return None


def inject_stubs():
    stub = Dummy()
    sys.modules.setdefault("core.quantum_game_kernel", types.SimpleNamespace(QuantumGameKernel=lambda **kw: stub))
    sys.modules.setdefault("core.cort_engine", types.SimpleNamespace(CORTEngine=lambda **kw: stub))
    sys.modules.setdefault("ai.neuromorphic_reservoir", types.SimpleNamespace(NeuromorphicReservoirML=lambda **kw: stub))
    sys.modules.setdefault("core.solid_state_modulator", types.SimpleNamespace(SolidStateModulator=lambda **kw: stub))
    sys.modules.setdefault("ui.portal_distortion_engine", types.SimpleNamespace(PortalDistortionEngine=lambda **kw: stub))
    sys.modules.setdefault("ui.synesthetic_euphoria_conductor", types.SimpleNamespace(SynestheticEuphoriaConductor=lambda **kw: stub))


def main():
    parser = argparse.ArgumentParser(description="Run a short deterministic performance check and fail if average latency exceeds threshold.")
    parser.add_argument("--threshold", type=float, default=5.0, help="Average frame time threshold in ms")
    parser.add_argument("--cycles", type=int, default=10, help="Number of frames to run for the check")
    args = parser.parse_args()

    inject_stubs()
    avg, mx = run_performance_benchmark(cycles=args.cycles, return_timings=True)

    print(f"Average frame time: {avg:.3f} ms (max: {mx:.3f} ms)")
    if avg > args.threshold:
        print(f"PERFORMANCE CHECK FAILED: average {avg:.3f} ms > threshold {args.threshold} ms")
        sys.exit(2)
    else:
        print(f"PERFORMANCE CHECK PASSED: average {avg:.3f} ms <= threshold {args.threshold} ms")


if __name__ == "__main__":
    main()

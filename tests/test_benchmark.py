import types
import sys

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


def pytest_configure(config):
    # Inject lightweight stub modules so the benchmark doesn't import heavy/absent modules
    stub = Dummy()
    sys.modules.setdefault("core.quantum_game_kernel", types.SimpleNamespace(QuantumGameKernel=lambda **kw: stub))
    sys.modules.setdefault("core.cort_engine", types.SimpleNamespace(CORTEngine=lambda **kw: stub))
    sys.modules.setdefault("ai.neuromorphic_reservoir", types.SimpleNamespace(NeuromorphicReservoirML=lambda **kw: stub))
    sys.modules.setdefault("core.solid_state_modulator", types.SimpleNamespace(SolidStateModulator=lambda **kw: stub))
    sys.modules.setdefault("ui.portal_distortion_engine", types.SimpleNamespace(PortalDistortionEngine=lambda **kw: stub))
    sys.modules.setdefault("ui.synesthetic_euphoria_conductor", types.SimpleNamespace(SynestheticEuphoriaConductor=lambda **kw: stub))


def test_benchmark_short_run():
    avg, mx = run_performance_benchmark(cycles=3, return_timings=True)
    assert isinstance(avg, float)
    assert avg >= 0.0

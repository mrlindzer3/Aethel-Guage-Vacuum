# physics/galileo_kinematics.py
import numpy as np

class GalileoKinematics:
    def __init__(self, g_baseline: float = 9.81):
        self.g = g_baseline

    def compute_displacement(self, initial_positions: np.ndarray, velocities: np.ndarray, dt: float) -> np.ndarray:
        """Applies d = v0*t + 0.5*g*t^2 uniformly across all active nodes."""
        acceleration_vector = np.array([0.0, -self.g, 0.0], dtype=np.float32)
        displacement = (velocities * dt) + (0.5 * acceleration_vector * (dt ** 2))
        return initial_positions + displacement

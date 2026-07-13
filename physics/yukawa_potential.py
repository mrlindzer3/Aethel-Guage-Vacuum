# physics/yukawa_potential.py
import numpy as np

class YukawaPotential:
    def __init__(self, coupling_constant_g: float = 1.0, range_parameter_alpha: float = 0.5):
        self.g = coupling_constant_g
        self.alpha = range_parameter_alpha

    def compute_node_binding_forces(self, rtm_distance_tensor: np.ndarray) -> np.ndarray:
        """Calculates short-range strong nuclear force binding vectors for the grid."""
        # Avoid division by zero at exact node positions
        safe_distances = np.where(rtm_distance_tensor == 0, np.inf, rtm_distance_tensor)
        
        # V(r) = -g^2 * (exp(-alpha * r) / r)
        potential_matrix = -(self.g ** 2) * (np.exp(-self.alpha * safe_distances) / safe_distances)
        return np.where(rtm_distance_tensor == 0, 0.0, potential_matrix)

# ──────────────────────────────────────────────────────────────────────────
# FILE: core/artificial_gravity_field.py
# ROLE: Non-Von Neumann Metric Artificial Gravity Field Engine
# ARCHITECTURE: Centrifugal & Coriolis Phase Velocity Gradient Mapper
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ArtificialGravity")

class ArtificialGravityField:
    def __init__(self, node_count: int = 640):
        self.node_count = node_count
        # Simulated habitat spin velocity (Angular frequency omega)
        self.omega = 2.5 

    def apply_gravitational_metric(self, planar_coordinates: np.ndarray, fragment_velocities: np.ndarray) -> dict:
        """
        Transforms raw spatial layout arrays by applying a synthetic gravitational 
        metric tensor profile using direct phase-displacement vectors.
        """
        logger.info("🛸 GRAVITY: Computing synthetic rotational metric tensor field...")
        
        # Calculate radial vectors from the central axis of the decagonal toroid
        radii = np.linalg.norm(planar_coordinates[:, :2], axis=1)
        
        gravity_accelerations = np.zeros_like(planar_coordinates)
        coriolis_shear_vectors = np.zeros((self.node_count, 2), dtype=np.float32)
        gravitational_potentials = np.zeros(self.node_count, dtype=np.float32)

        for i in range(self.node_count):
            r = radii[i]
            pos = planar_coordinates[i, :2]
            vel = fragment_velocities[i, :2] if fragment_velocities is not None else np.zeros(2)
            
            if r == 0:
                continue
                
            # 1. CENTRIFUGAL GRADIENT CARVING
            # Accel direction is radially outward: a = omega^2 * r
            radial_unit = pos / r
            centrifugal_accel = (self.omega ** 2) * r
            gravity_accelerations[i, :2] = radial_unit * centrifugal_accel
            
            # Map the potential well depth (high energy at the rim, zero at the hub)
            gravitational_potentials[i] = 0.5 * (self.omega ** 2) * (r ** 2)
            
            # 2. CORIOLIS SHEAR CORRECTION
            # F_coriolis = -2 * omega * (z_hat x velocity)
            coriolis_shear_vectors[i, 0] = -2.0 * self.omega * vel[1]
            coriolis_shear_vectors[i, 1] = 2.0 * self.omega * vel[0]

        logger.info(f"✨ GRAVITY: Field locked. Peak Rim Gravity Acceleration: {np.max(gravity_accelerations):.2f} m/s^2.")
        return {
            "metric_acceleration": gravity_accelerations,
            "coriolis_shear": coriolis_shear_vectors,
            "well_potentials": gravitational_potentials
        }

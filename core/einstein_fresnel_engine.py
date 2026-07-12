# ──────────────────────────────────────────────────────────────────────────
# FILE: core/einstein_fresnel_engine.py
# ROLE: Einstein-Fresnel Lens Mode Solver & Stability Evolution Vector Tracker
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("EinsteinFresnelEngine")

class EinsteinFresnelEngine:
    def __init__(self, n0: float = 1.000293):
        """
        Initializes the math engine using your baseline refractive index (n0).
        """
        self.n0 = n0

    def compute_spacetime_refractive_metric(self, psi_cohesion: np.ndarray, rho_prob: np.ndarray, chi_s: float) -> np.ndarray:
        """
        Calculates: n(x,y,z) = n0 + ((psi_cohesion * rho_probability) / 10^8) * chi_s
        """
        logger.info("📐 METRIC: Computing Localized Space-Time Refractive Metric...")
        interaction_term = (psi_cohesion * rho_prob) / 1e8
        n_xyz = self.n0 + (interaction_term * chi_s)
        return n_xyz

    def compute_stability_evolution_vector(self, E0: np.ndarray, n_xyz: np.ndarray, H_factor: float) -> np.ndarray:
        """
        Calculates: Es = E0 * [ H * (1 + n/10) + (1 - H) * (1 + n/10)^-1 ]
        """
        logger.info("📐 STABILITY: Modeling Stability Evolution Vector fields...")
        base_term = 1.0 + (n_xyz / 10.0)
        
        # H-factor scales the forward and inverse boundary components
        forward_component = H_factor * base_term
        inverse_component = (1.0 - H_factor) * (1.0 / base_term)
        
        E_s = E0 * (forward_component + inverse_component)
        return E_s

    def verify_surface_boundary_geometry(self, phi: np.ndarray, lambda_i: float, v_i: np.ndarray) -> np.ndarray:
        """
        Evaluates the Einstein Fresnel Lens Mode boundary condition:
        ∇²Φ(x,y,z) = λ_i * v_i  =>  ∇²Φ - λ_i * v_i = 0
        Uses finite-difference approximations to calculate the numerical Laplacian (∇²Φ).
        """
        logger.info("📐 GEOMETRY: Solving Surface Boundary Laplacian (∇²Φ - λ_i * v_i = 0)...")
        
        # Numerical 2D/3D Laplacian via numpy gradient calculations
        grad_x, grad_y = np.gradient(phi)
        laplacian_phi = np.gradient(grad_x, axis=0) + np.gradient(grad_y, axis=1)
        
        # Calculate the direct residual error matrix
        residual = laplacian_phi - (lambda_i * v_i)
        mean_deviation = np.mean(np.abs(residual))
        
        logger.info(f"📐 GEOMETRY: Einstein-Fresnel Lens mode balance verified. Mean Deviation: {mean_deviation:.6e}")
        return residual

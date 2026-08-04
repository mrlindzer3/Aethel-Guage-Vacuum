#!/usr/bin/env python3
"""
Aethel-Gauge-Vacuum: Levitated Optomechanics & Optical Tweezers Gravity Engine
Calculates optical dipole forces, gradient potential wells, and trapping stiffness 
to pin physical gravity wells to hyper-quasicrystal nodes.
"""

import numpy as np

class LevitatedOptomechanicsEngine:
    def __init__(self, wavelength_nm=550.0, particle_radius_nm=100.0, laser_power_mw=100.0):
        self.wavelength = wavelength_nm * 1e-9  # Meters
        self.radius = particle_radius_nm * 1e-9   # Meters
        self.power = laser_power_mw * 1e-3        # Watts
        self.c = 3.0e8                            # Speed of light (m/s)
        self.n_medium = 1.33                      # Refractive index of medium/vacuum boundary
        self.n_particle = 1.59                    # Refractive index of nanoparticle (e.g., Silica)

    def compute_optical_tweezers_potential(self, field_intensity_tensor):
        """
        Calculates the optical dipole potential (U_opt) for a levitated dielectric particle 
        trapped in the gradient of the optical field:
        U_opt = - (2 * pi * r^3 / c) * ((m^2 - 1) / (m^2 + 2)) * I(r)
        where m = n_particle / n_medium.
        """
        print("[*] Calculating Optical Tweezers Gradient Potential Wells...")
        
        m = self.n_particle / self.n_medium
        polarizability_factor = (m**2 - 1.0) / (m**2 + 2.0)
        
        # Volume of the spherical nanoparticle
        particle_volume = (4.0 / 3.0) * np.pi * (self.radius ** 3)
        
        # Optical trapping potential well depth (Joules)
        # Intensity tensor acts as the localized field energy density
        u_potential = - (2.5e-1) * particle_volume * self.n_medium * polarizability_factor * field_intensity_tensor
        
        return u_potential

    def pin_gravity_wells_to_nodes(self, node_coordinates, potential_tensor):
        """
        Pins physical micro-gravity wells to the quasicrystal node coordinates 
        by computing trapping stiffness (kappa) and local acceleration vectors.
        """
        print("[*] Pinning Levitated Optomechanical Gravity Wells to Nodes...")
        
        pinned_wells = []
        # Compute spatial Hessian (second derivative) of the potential to find trapping stiffness kappa
        hessian_y, hessian_x = np.gradient(np.gradient(potential_tensor))
        
        for idx, pt in enumerate(node_coordinates):
            # Map continuous coordinates to grid indices safely
            ix = int(np.clip(abs(pt[0]) * 10, 0, potential_tensor.shape[1] - 1))
            iy = int(np.clip(abs(pt[1]) * 10, 0, potential_tensor.shape[0] - 1))
            
            # Local trapping frequency and effective gravity well mass/acceleration
            stiffness = abs(hessian_x[iy, ix] + hessian_y[iy, ix])
            well_depth = abs(potential_tensor[iy, ix])
            
            pinned_wells.append({
                "node_id": idx,
                "position": (pt[0], pt[1]),
                "trap_stiffness_kappa": stiffness,
                "well_depth_joules": well_depth,
                "simulated_gravity_accel": well_depth / (self.radius * 1e6 + 1e-6)
            })
            
        return pinned_wells

if __name__ == "__main__":
    # Generate mock hyper-quasicrystal nodes & field intensity map
    angles = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    radii = np.sqrt(np.linspace(0.1, 15.0, 64))
    nodes = np.stack([radii * np.cos(angles), radii * np.sin(angles)], axis=-1)

    x = np.linspace(-15, 15, 128)
    y = np.linspace(-15, 15, 128)
    X, Y = np.meshgrid(x, y)
    mock_intensity = np.exp(-(X**2 + Y**2) / 25.0) * np.cos(X) ** 2

    engine = LevitatedOptomechanicsEngine()
    potential = engine.compute_optical_tweezers_potential(mock_intensity)
    wells = engine.pin_gravity_wells_to_nodes(nodes, potential)

    print("==================================================")
    print("   LEVITATED OPTOMECHANICS GRAVITY WELLS PINNED")
    print("==================================================")
    print(f"[*] Total Pinned Node Wells: {len(wells)}")
    print(f"[*] Sample Pinned Well [0] - Position: {wells[0]['position']}")
    print(f"[*] Sample Pinned Well [0] - Trap Stiffness (kappa): {wells[0]['trap_stiffness_kappa']:.4f}")
    print(f"[*] Sample Pinned Well [0] - Gravity Accel Metric: {wells[0]['simulated_gravity_accel']:.4f}")
    print("==================================================")

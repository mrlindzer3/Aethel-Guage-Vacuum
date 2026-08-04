import numpy as np
import matplotlib.pyplot as plt

def run_fdtd_wave_propagation(eps_grid, steps=250):
    """
    Simulates 2D scalar wave propagation through the nested hyper-quasicrystal 
    permittivity matrix using an explicit FDTD scheme.
    """
    ny, nx = eps_grid.shape
    
    # Fields: Ez (electric field), Hx, Hy (magnetic fields - simplified scalar wave formulation)
    psi_prev = np.zeros((ny, nx))
    psi_curr = np.zeros((ny, nx))
    psi_next = np.zeros((ny, nx))
    
    # Speed of light in medium mapped to grid spacing
    c = 0.5
    dt = 0.5
    
    # Source position (simulate a diode firing near the center)
    src_x, src_y = nx // 2, ny // 2
    
    snapshots = []
    
    for t in range(steps):
        # Inject source (Gaussian pulse / Ricker wavelet)
        source_val = np.sin(2 * np.pi * 0.05 * t) * np.exp(-((t - 30)**2) / 100)
        psi_curr[src_y, src_x] += source_val
        
        # FDTD wave update equation incorporating local permittivity (eps = n^2)
        # Laplaciandiffusion divided by permittivity profile
        laplacian = (
            np.roll(psi_curr, 1, axis=0) + np.roll(psi_curr, -1, axis=0) +
            np.roll(psi_curr, 1, axis=1) + np.roll(psi_curr, -1, axis=1) - 
            4 * psi_curr
        )
        
        psi_next = 2 * psi_curr - psi_prev + (c**2 * dt**2 / eps_grid) * laplacian
        
        # Boundary damping (absorbing layer approximation)
        psi_next[0, :] = 0; psi_next[-1, :] = 0
        psi_next[:, 0] = 0; psi_next[:, -1] = 0
        
        # Step forward
        psi_prev = psi_curr.copy()
        psi_curr = psi_next.copy()
        
        # Capture snapshot mid-propagation
        if t in [50, 100, 180]:
            snapshots.append(psi_curr.copy())
            
    return snapshots

# Execute propagation simulation
wave_snapshots = run_fdtd_wave_propagation(eps_profile)

# Visualize the wave scattering across the aperiodic lattice
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='black')
for i, snap in enumerate(wave_snapshots):
    ax = axes[i]
    ax.set_facecolor('black')
    im = ax.imshow(snap, cmap='seismic', vmin=-0.2, vmax=0.2, origin='lower')
    ax.set_title(f"Wavefront Evolution Step {(i+1)*50 + 50}", color='white')
    ax.axis('off')

plt.tight_layout()
plt.show()

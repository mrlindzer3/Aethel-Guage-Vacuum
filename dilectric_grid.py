import numpy as np
import matplotlib.pyplot as plt

def create_dielectric_permittivity_grid(nested_layers, grid_size=512, box_size=20.0):
    """
    Converts point coordinates into a 2D spatial permittivity matrix (eps_grid)
    suitable for FDTD wave propagation modeling.
    """
    eps_grid = np.ones((grid_size, grid_size)) * 2.1  # Base substrate index (e.g., glass/polymer ~ 1.45^2)
    
    # Material parameters
    high_index_val = 6.25 # e.g., TiO2 (approx n = 2.5) -> n^2 = 6.25
    rod_radius = 2.5      # Radius in pixels
    
    # Map spatial coordinates to grid indices
    for lvl_idx, layer in enumerate(nested_layers):
        # Varying dielectric contrast per nested tier
        current_eps = high_index_val - (lvl_idx * 0.5) 
        
        for pt in layer:
            # Shift coordinates from centered physical space to grid space
            gx = int((pt[0] + box_size / 2) / box_size * grid_size)
            gy = int((pt[1] + box_size / 2) / box_size * grid_size)
            
            # Draw circular rod/inclusion on the grid
            Y, X = np.ogrid[:grid_size, :grid_size]
            dist_from_center = np.sqrt((X - gx)**2 + (Y - gy)**2)
            mask = dist_from_center <= rod_radius
            eps_grid[mask] = current_eps
            
    return eps_grid

# Generate permittivity profile from previous layers
eps_profile = create_dielectric_permittivity_grid(nested_quasicrystal_layers)

# Visualize the resulting photonic crystal refractive index map
plt.figure(figsize=(8, 8), facecolor='black')
plt.imshow(eps_profile, cmap='inferno', origin='lower')
plt.colorbar(label='Permittivity ($\epsilon = n^2$)')
plt.title("Spatial Permittivity Map for Wave Propagation", color='white')
plt.axis('off')
plt.show()

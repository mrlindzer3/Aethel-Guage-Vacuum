import numpy as np
import matplotlib.pyplot as plt

def generate_nested_hyper_quasicrystal(
    base_points=1500, 
    dim_high=4, 
    dim_low=2, 
    theta=np.pi/8, 
    nesting_levels=2, 
    scale_factor=1.4142
):
    """
    Generates a multi-scale nested hyper-quasicrystalline point lattice 
    designed for micro-diode optical extraction layers.
    """
    master_lattice = []
    
    # Generate base high-D hypercube coordinates
    np.random.seed(42)
    base_coords = np.random.uniform(-4, 4, size=(base_points, dim_high))
    
    # Rotation matrix for irrational slope (e.g., 8-fold symmetry projection)
    rot_matrix = np.array([
        [np.cos(theta), -np.sin(theta), np.cos(2*theta), 0],
        [np.sin(theta), np.cos(theta), 0, np.sin(2*theta)]
    ])
    rot_matrix /= np.linalg.norm(rot_matrix, axis=1, keepdims=True)

    # Recursive nesting loop to construct multi-scale photonic boundaries
    current_scale = 1.0
    for level in range(nesting_levels):
        projected_points = []
        for pt in base_coords:
            # Acceptance window filter in orthogonal complement space
            ortho_val = np.sum(pt[dim_low:])
            if abs(ortho_val) < 1.35: 
                p_2d = np.dot(rot_matrix, pt) * current_scale
                projected_points.append(p_2d)
                
        master_lattice.append(np.array(projected_points))
        current_scale /= scale_factor # Scale down for inner nested sub-lattice
        
    return master_lattice

# Execute multi-scale geometry generation
nested_quasicrystal_layers = generate_nested_hyper_quasicrystal()

# Visualization of the multi-scale optical matrix
plt.figure(figsize=(9, 9), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

colors = ['cyan', 'magenta', 'lime']
for i, layer in enumerate(nested_quasicrystal_layers):
    plt.scatter(
        layer[:, 0], layer[:, 1], 
        s=max(1, 15 - i*5), 
        c=colors[i % len(colors)], 
        alpha=0.75, 
        label=f'Nested Scale Level {i+1}'
    )

plt.title("Nested Hyper-Quasicrystal Diode Substrate Geometry", color='white', fontsize=12)
plt.xlabel("X Coordinate ($\mu$m)", color='white')
plt.ylabel("Y Coordinate ($\mu$m)", color='white')
plt.legend(facecolor='darkgray', edgecolor='none')
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
plt.tight_layout()
plt.show()

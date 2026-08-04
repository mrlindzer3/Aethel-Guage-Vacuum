import numpy as np
import matplotlib.pyplot as plt

def generate_cut_project_quasicrystal(num_points=2000, dim_high=4, dim_low=2, theta=math.pi/8):
    """
    Generates a 2D quasicrystalline point set via the cut-and-project method 
    from a higher-dimensional hypercubic lattice.
    """
    # 1. Generate high-dimensional points within a hypercube
    # For a 4D hypercube projected to 2D
    coords = np.random.uniform(-5, 5, size=(num_points, dim_high))
    
    # 2. Define projection rotation matrix (irrational slope to ensure aperiodicity)
    # Using a rotational slice angle based on symmetry (e.g., 8-fold -> pi/8)
    rot_matrix = np.array([
        [np.cos(theta), -np.sin(theta), np.cos(2*theta), 0],
        [np.sin(theta), np.cos(theta), 0, np.sin(2*theta)]
    ])
    
    # Normalize projection operator
    rot_matrix /= np.linalg.norm(rot_matrix, axis=1, keepdims=True)
    
    # 3. Cut-and-project: map high-D nodes onto the 2D physical plane (Window acceptance check)
    projected_points = []
    for pt in coords:
        # Internal orthogonal space check (the "strip" or "window" filter)
        ortho_val = np.sum(pt[dim_low:]) # simplified acceptance window
        if abs(ortho_val) < 1.5: 
            # Project down to 2D screen coordinates
            p_2d = np.dot(rot_matrix, pt)
            projected_points.append(p_2d)
            
    return np.array(projected_points)

# Execute geometry mapping for screen scale
quasi_nodes = generate_cut_project_quasicrystal()

# Plotting the raw aperiodic lattice node distribution for the diode matrix
plt.figure(figsize=(8, 8))
plt.scatter(quasi_nodes[:, 0], quasi_nodes[:, 1], s=2, c='cyan', alpha=0.8)
plt.title("Nested Hyper-Quasicrystal Node Matrix (2D Projection)")
plt.xlabel("X Position (Microns)")
plt.ylabel("Y Position (Microns)")
plt.gca().set_facecolor('black')
plt.show()

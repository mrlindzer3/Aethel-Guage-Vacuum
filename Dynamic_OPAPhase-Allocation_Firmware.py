import numpy as np
import matplotlib.pyplot as plt

def compute_opa_phase_matrix(nested_layers, target_angle_deg=15.0, wavelength_um=0.55):
    """
    Computes the real-time phase-delay driving matrix (PWM/voltage offsets) 
    for the aperiodic diode nodes to achieve dynamic OPA beam steering.
    """
    primary_nodes = nested_layers[0]
    
    # Convert target angle to radians
    theta = np.radians(target_angle_deg)
    k = 2 * np.pi / wavelength_um  # Wave number
    
    # Calculate required phase shift for each node based on its spatial position (r * k * sin(theta))
    phases = []
    for pt in primary_nodes:
        # Spatial projection along the steering vector
        spatial_projection = pt[0] * np.sin(theta)
        # Phase calculation modulo 2*pi
        phase_delay = (k * spatial_projection) % (2 * np.pi)
        phases.append(phase_delay)
        
    phases = np.array(phases)
    
    # Visualization of the phase-delay distribution across the screen substrate
    fig, ax = plt.subplots(figsize=(9, 9), facecolor='black')
    ax.set_facecolor('black')
    
    sc = ax.scatter(
        primary_nodes[:, 0], primary_nodes[:, 1], 
        c=phases, cmap='hsv', s=25, alpha=0.85
    )
    
    cbar = plt.colorbar(sc)
    cbar.set_label('Drive Phase Delay (Radians)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    
    plt.title(f"Dynamic OPA Phase Map (Steering Angle: {target_angle_deg}°)", color='white', fontsize=14)
    plt.xlabel("X Position ($\mu$m)", color='white')
    plt.ylabel("Y Position ($\mu$m)", color='white')
    plt.grid(color='gray', linestyle=':', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return phases

# Execute OPA phase allocation for a 15-degree steering vector
opa_phase_table = compute_opa_phase_matrix(nested_hyper_quasicrystal_layers)

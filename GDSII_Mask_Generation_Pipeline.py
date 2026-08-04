import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def export_fabrication_mask(nested_layers, wafer_size_um=100.0):
    """
    Generates a clean vector layout of the nested hyper-quasicrystal 
    suitable for photolithographic mask generation (e.g., GDSII pipeline).
    """
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.set_facecolor('white')
    
    # Define color/radius hierarchy for different nested tiers (representing etch holes or pillars)
    tier_styles = [
        {'color': 'black', 'radius': 0.8},  # Primary high-index pillars
        {'color': 'dimgray', 'radius': 0.5}, # Secondary nested sub-lattice
        {'color': 'gray', 'radius': 0.3}     # Tertiary fractal nodes
    ]
    
    for lvl_idx, layer in enumerate(nested_layers):
        style = tier_styles[lvl_idx % len(tier_styles)]
        
        for pt in layer:
            # Draw circle representing a single dielectric rod/pore feature
            circle = patches.Circle(
                (pt[0], pt[1]), 
                radius=style['radius'], 
                facecolor=style['color'], 
                edgecolor='none',
                alpha=0.9
            )
            ax.add_patch(circle)
            
    # Set physical boundaries matching display pixel pitch scale
    ax.set_xlim(-wafer_size_um/2, wafer_size_um/2)
    ax.set_ylim(-wafer_size_um/2, wafer_size_um/2)
    ax.set_aspect('equal')
    
    plt.title("Photolithographic Mask Layer: Nested Hyper-Quasicrystal", color='black', fontsize=14)
    plt.xlabel("X Position ($\mu$m)", color='black')
    plt.ylabel("Y Position ($\mu$m)", color='black')
    plt.grid(True, linestyle=':', alpha=0.5)
    
    # Save vector layout for fabrication
    plt.savefig("hyper_quasicrystal_mask.svg", format='svg', bbox_inches='tight')
    plt.show()

# Execute mask generation
export_fabrication_mask(nested_quasicrystal_layers)

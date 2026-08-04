import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def generate_voronoi_routing_grid(nested_layers):
    """
    Computes the Voronoi tessellation over the quasicrystal nodes 
    to establish the active-matrix (AM-TFT) sub-pixel isolation and routing boundaries.
    """
    # Flatten the primary and secondary layers into a single coordinate set for partitioning
    primary_nodes = nested_layers[0]
    
    # Compute Voronoi diagram for irregular node distribution
    vor = Voronoi(primary_nodes)
    
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('black')
    
    # Plot Voronoi ridges (electrical isolation/barrier lines)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='cyan', 
                    line_width=1.0, line_alpha=0.6, point_size=3)
    
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    
    plt.title("Active-Matrix Voronoi Routing & Diode Isolation Grid", color='white', fontsize=14)
    plt.xlabel("X Coordinate ($\mu$m)", color='white')
    plt.ylabel("Y Coordinate ($\mu$m)", color='white')
    plt.grid(color='gray', linestyle=':', alpha=0.2)
    
    plt.tight_layout()
    plt.show()

# Execute Voronoi driver routing layout
generate_voronoi_routing_grid(nested_quasicrystal_layers)

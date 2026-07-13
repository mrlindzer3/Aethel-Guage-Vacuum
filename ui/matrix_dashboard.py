# ──────────────────────────────────────────────────────────────────────────
# FILE: ui/matrix_dashboard.py
# ROLE: 2D Juxtaposition ASCII Surface Topology Visualizer
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MatrixDashboard")

class MatrixDashboard:
    def __init__(self, display_size: int = 40):
        self.size = display_size

    def render_surface_topology(self, planar_coordinates: np.ndarray, ternary_states: np.ndarray):
        """
        Renders a 2D equidistant visualization map of the 640 nodes 
        split across the three concentric tertiary interaction zones.
        """
        logger.info("🎨 DASHBOARD: Generating real-time geometric alignment plot...")
        
        # Initialize an empty terminal text character grid
        grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
        
        # Center point of the display grid
        center = self.size // 2
        
        # Normalize and scale coordinate positions to fit perfectly within the display grid bounds
        max_coord = np.max(np.abs(planar_coordinates)) if np.max(np.abs(planar_coordinates)) > 0 else 1.0
        scale_factor = (center - 2) / max_coord

        for i, (x, y) in enumerate(planar_coordinates):
            grid_x = int(center + x * scale_factor)
            grid_y = int(center + y * scale_factor)
            
            # Bound checking to ensure node coordinates stay inside grid limits
            if 0 <= grid_x < self.size and 0 <= grid_y < self.size:
                state = ternary_states[i]
                
                # Assign distinct ASCII markers based on ternary zone state values
                if state == -1:
                    marker = "."  # Inner Horizon (-1)
                elif state == 0:
                    marker = "O"  # Toroidal Backbone (0)
                else:
                    marker = "X"  # Outer Wyrd Envelope (+1)
                    
                grid[grid_y][grid_x] = marker

        # Compile and output the resulting spatial visual rendering string
        logger.info("📊 PRINTING JUXTAPOSED SURFACE ALIGNMENT MAP:")
        print("\n" + "═" * (self.size + 2))
        for row in grid:
            print("║" + "".join(row) + "║")
        print("═" * (self.size + 2) + "\n")

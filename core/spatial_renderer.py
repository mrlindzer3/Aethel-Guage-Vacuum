# ──────────────────────────────────────────────────────────────────────────
# FILE: core/spatial_renderer.py
# ROLE: Volumetric Spatial Density Display Projection Engine
# ARCHITECTURE: Viewport Raster Reduction Matrix for Terminal Tracking
# ──────────────────────────────────────────────────────────────────────────

import numpy as np

class SpatialRenderer:
    def __init__(self, width: int = 60, height: int = 22):
        self.width = width
        self.height = height
        # Density ramp characters for tracking node distribution intensity
        self.density_ramp = " .:-=+*#%@"

    def generate_ascii_viewport(self, positions: np.ndarray) -> str:
        """
        Projects 3D node locations down onto a 2D viewport grid,
        rendering local cluster densities using structural ASCII gradients.
        """
        # Initialize an empty canvas buffer matrix
        canvas = np.zeros((self.height, self.width), dtype=np.int32)
        
        # Normalize positions down to fit perfectly inside our viewport limits
        x_coords = positions[:, 0]
        y_coords = positions[:, 1]
        
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()
        
        # Avoid zero-range division faults on static matrices
        x_span = (x_max - x_min) if (x_max - x_min) > 0 else 1.0
        y_span = (y_max - y_min) if (y_max - y_min) > 0 else 1.0
        
        for i in range(positions.shape[0]):
            # Map coordinates to grid spaces
            grid_x = int(((x_coords[i] - x_min) / x_span) * (self.width - 1))
            grid_y = int(((y_coords[i] - y_min) / y_span) * (self.height - 1))
            
            # Accumulate density weightings at intersection points
            if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                canvas[grid_y, grid_x] += 1

        # Translate numerical array density values into raw character rows
        view_lines = ["┌" + "─" * self.width + "┐"]
        for row in range(self.height):
            line_chars = []
            for col in range(self.width):
                density_val = canvas[row, col]
                char_index = min(density_val, len(self.density_ramp) - 1)
                line_chars.append(self.density_ramp[char_index])
            view_lines.append("│" + "".join(line_chars) + "│")
        view_lines.append("└" + "─" * self.width + "┘")
        
        return "\n".join(view_lines)

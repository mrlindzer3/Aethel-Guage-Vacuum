# ──────────────────────────────────────────────────────────────────────────
# FILE: core/optimized_console.py
# ROLE: Double-Buffered Low-Overhead Terminal Delta Rasterizer
# ARCHITECTURE: ANSI Escape-Accelerated Viewport Matrix
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import sys

class OptimizedConsole:
    def __init__(self, width: int = 65, height: int = 20):
        self.width = width
        self.height = height
        self.density_ramp = " .:-=+*#%@"
        
        # Double-buffering data structures
        self.current_buffer = np.full((self.height, self.width), " ", dtype="<U1")
        self.previous_buffer = np.full((self.height, self.width), " ", dtype="<U1")
        
        # Clear terminal screen and hide cursor for smooth streaming
        sys.stdout.write("\033[2J\033[?25l")
        sys.stdout.flush()

    def update_frame(self, positions: np.ndarray):
        """
        Calculates spatial layout density and writes only modified characters
        directly to the terminal screen buffer using ANSI cursor coordinates.
        """
        # Reset current frame canvas workspace
        self.current_buffer[:] = " "
        
        # Project 3D space vectors onto 2D view limits
        x, y = positions[:, 0], positions[:, 1]
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()
        
        x_span = (x_max - x_min) if (x_max - x_min) > 0 else 1.0
        y_span = (y_max - y_min) if (y_max - y_min) > 0 else 1.0
        
        # Count spatial density distributions via a 2D histogram lookup matrix
        grid_x = ((x - x_min) / x_span * (self.width - 1)).astype(np.int32)
        grid_y = ((y - y_min) / y_span * (self.height - 1)).astype(np.int32)
        
        # Map accumulated counts inside valid bounding limits
        valid_mask = (grid_x >= 0) & (grid_x < self.width) & (grid_y >= 0) & (grid_y < self.height)
        counts = np.zeros((self.height, self.width), dtype=np.int32)
        
        for gx, gy in zip(grid_x[valid_mask], grid_y[valid_mask]):
            counts[gy, gx] += 1
            
        # Convert localized frequency counts into character vectors
        ramp_indices = np.minimum(counts, len(self.density_ramp) - 1)
        for r in range(self.height):
            for c in range(self.width):
                self.current_buffer[r, c] = self.density_ramp[ramp_indices[r, c]]
                
        # DELTA BLITTING: Pinpoint modified screen locations
        diff_mask = self.current_buffer != self.previous_buffer
        rows, cols = np.where(diff_mask)
        
        # Stream character changes to stdout using targeted ANSI coordinates
        write_buffer = []
        for r, c in zip(rows, cols):
            char = self.current_buffer[r, c]
            # \033[{row};{col}H shifts terminal cursor directly to cell position
            write_buffer.append(f"\033[{r + 2};{c + 2}H{char}")
            
        sys.stdout.write("".join(write_buffer))
        sys.stdout.flush()
        
        # Flip frame buffer spaces
        self.previous_buffer[:] = self.current_buffer

    def close(self):
        """Restores terminal configuration state gracefully on process termination."""
        sys.stdout.write("\033[?25h\033[2J\033[1;1H")
        sys.stdout.flush()

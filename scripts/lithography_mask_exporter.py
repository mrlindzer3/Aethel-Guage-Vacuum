#!/usr/bin/env python3
"""
Aethel-Gauge-Vacuum: Lithography Mask Exporter
Generates scalable vector graphics (SVG) photomasks from aperiodic quasicrystal 
node coordinates for cleanroom microfabrication.
"""

import numpy as np
import os

class LithographyMaskExporter:
    def __init__(self, canvas_size_mm=50.0, wavelength_nm=550.0):
        self.canvas_size = canvas_size_mm
        self.wavelength = wavelength_nm

    def generate_svg_mask(self, node_coordinates, filename="opa_lithography_mask.svg"):
        """Exports an array of 2D coordinates as an SVG vector layout."""
        # Scale coordinates to fit canvas (assuming inputs are normalized roughly to [-15, 15])
        scale_factor = (self.canvas_size * 0.8) / 30.0
        center = self.canvas_size / 2.0

        svg_elements = []
        svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.canvas_size} {self.canvas_size}" width="100%" height="100%">')
        svg_elements.append('  <rect width="100%" height="100%\" fill="black"/>')  # Opaque darkfield background
        svg_elements.append('  <g fill="white" stroke="none">')

        for pt in node_coordinates:
            # Map world coords to canvas space in millimeters
            cx = center + (pt[0] * scale_factor)
            cy = center + (pt[1] * scale_factor)
            # Aperture radius scaled relative to optical wavelength
            radius = max(0.15, (self.wavelength / 1000.0) * 0.5)
            
            svg_elements.append(f'    <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{radius:.4f}" />')

        svg_elements.append('  </g>')
        svg_elements.append('</svg>')

        output_path = os.path.join(os.path.dirname(__file__), '..', filename)
        with open(output_path, 'w') as f:
            f.write('\n'.join(svg_elements))
        
        print(f"[✓] Lithography mask successfully exported to: {filename}")

if __name__ == "__main__":
    # Generate mock quasicrystal coordinates
    angles = np.linspace(0, 2 * np.pi, 512, endpoint=False)
    radii = np.sqrt(np.linspace(0.1, 15.0, 512))
    nodes = np.stack([radii * np.cos(angles), radii * np.sin(angles)], axis=-1)

    exporter = LithographyMaskExporter(canvas_size_mm=50.0)
    exporter.generate_svg_mask(nodes)

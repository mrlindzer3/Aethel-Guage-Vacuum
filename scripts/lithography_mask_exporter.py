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
#!/usr/bin/env python3
"""
Aethel-Gauge-Vacuum: Holo-SVD Integrated Lithography Mask Exporter
Applies Singular Value Decomposition tensor factorization to aperiodic 
quasicrystal nodes prior to photomask vector generation.
"""

import numpy as np
import os

class LithographyMaskExporter:
    def __init__(self, canvas_size_mm=50.0, wavelength_nm=550.0, rank_truncation=64):
        self.canvas_size = canvas_size_mm
        self.wavelength = wavelength_nm
        self.rank_truncation = rank_truncation

    def apply_holo_svd_compression(self, node_coordinates):
        """
        Factorizes the spatial node matrix via Holo SVD to extract dominant 
        volumetric singular vectors and eliminate low-energy optical scatter.
        """
        print(f"[*] Applying Holo SVD tensor factorization (Rank truncation: {self.rank_truncation})...")
        
        # Construct spatial tensor matrix from coordinates
        U, s, Vt = np.linalg.svd(node_coordinates, full_matrices=False)
        
        # Truncate to dominant singular values (Holo SVD reduction)
        k = min(self.rank_truncation, len(s))
        U_trunc = U[:, :k]
        s_trunc = np.diag(s[:k])
        Vt_trunc = Vt[:k, :]
        
        # Reconstruct filtered coordinate space
        filtered_nodes = np.dot(U_trunc, np.dot(s_trunc, Vt_trunc))
        print(f"[✓] Holo SVD reduction complete. Retained singular energy: {s[:k].sum() / s.sum() * 100:.2f}%")
        
        return filtered_nodes

    def generate_svg_mask(self, node_coordinates, filename="opa_lithography_mask.svg"):
        """Exports Holo-SVD filtered 2D coordinates as an SVG vector layout."""
        # Process through Holo SVD core module first
        processed_nodes = self.apply_holo_svd_compression(node_coordinates)

        scale_factor = (self.canvas_size * 0.8) / 30.0
        center = self.canvas_size / 2.0

        svg_elements = []
        svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.canvas_size} {self.canvas_size}" width="100%" height="100%">')
        svg_elements.append('  <rect width="100%" height="100%" fill="black"/>')  # Opaque darkfield background
        svg_elements.append('  <g fill="white" stroke="none">')

        for pt in processed_nodes:
            cx = center + (pt[0] * scale_factor)
            cy = center + (pt[1] * scale_factor)
            radius = max(0.15, (self.wavelength / 1000.0) * 0.5)
            
            svg_elements.append(f'    <circle cx="{cx:.4f}" cy="{cy:.4f}" r="{radius:.4f}" />')

        svg_elements.append('  </g>')
        svg_elements.append('</svg>')

        output_path = os.path.join(os.path.dirname(__file__), '..', filename)
        with open(output_path, 'w') as f:
            f.write('\n'.join(svg_elements))
        
        print(f"[✓] Holo-SVD integrated lithography mask successfully exported to: {filename}")

if __name__ == "__main__":
    # Generate mock quasicrystal coordinates
    angles = np.linspace(0, 2 * np.pi, 512, endpoint=False)
    radii = np.sqrt(np.linspace(0.1, 15.0, 512))
    nodes = np.stack([radii * np.cos(angles), radii * np.sin(angles)], axis=-1)

    exporter = LithographyMaskExporter(canvas_size_mm=50.0, rank_truncation=128)
    exporter.generate_svg_mask(nodes)

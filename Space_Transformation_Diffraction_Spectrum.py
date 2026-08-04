import numpy as np
import matplotlib.pyplot as plt

def analyze_reciprocal_space(eps_grid):
    """
    Computes the 2D Fast Fourier Transform (FFT) of the dielectric matrix 
    to reveal the k-space momentum distribution and reciprocal lattice symmetry.
    """
    # Shift zero-frequency to center
    fft_transformed = np.fft.fft2(eps_grid - np.mean(eps_grid))
    fft_shifted = np.fft.fftshift(fft_transformed)
    
    # Calculate power spectrum (intensity of scattering vectors)
    power_spectrum = np.abs(fft_shifted)**2
    
    # Apply logarithmic scaling to visualize faint multi-scale diffraction rings
    log_spectrum = np.log(power_spectrum + 1)
    
    return log_spectrum

# Execute reciprocal space mapping
k_space_map = analyze_reciprocal_space(eps_profile)

# Visualize the k-space signature
plt.figure(figsize=(8, 8), facecolor='black')
plt.imshow(k_space_map, cmap='nipy_spectral', origin='lower')
plt.colorbar(label='Log Reciprocal Intensity ($\log |E(\mathbf{k})|^2$)')
plt.title("Reciprocal Space ($\mathbf{k}$-Space) Momentum Distribution", color='white')
plt.xlabel("k_x Momentum Vector", color='white')
plt.ylabel("k_y Momentum Vector", color='white')
plt.axis('off')
plt.show()

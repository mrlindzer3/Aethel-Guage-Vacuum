# Hardware-in-the-Loop Driver for Aethel-Gauge-Vacuum OPA Matrix
# Target: MicroPython / ESP32 / Raspberry Pi Pico SPI/PWM Bridge

import math
import struct

class OPALatticeHardwareDriver:
    def __init__(self, num_channels=256, max_dac_resolution=65535):
        self.num_channels = num_channels
        self.max_dac = max_dac_resolution

    def radians_to_pwm_counts(self, phase_radians):
        """
        Maps continuous phase values [0, 2*pi] to discrete DAC/PWM duty cycle counts.
        """
        normalized = phase_radians / (2.0 * math.pi)
        normalized = max(0.0, min(1.0, normalized)) # Clamp boundary
        return int(normalized * self.max_dac)

    def compile_hardware_frame(self, phase_array):
        """
        Serializes phase float array into a packed binary payload for SPI streaming.
        """
        payload = bytearray()
        for phase in phase_array:
            pwm_val = self.radians_to_pwm_counts(phase)
            # Pack as 16-bit unsigned integer little-endian
            payload.extend(struct.pack('<H', pwm_val))
        return payload

# --- Example Execution Test ---
if __name__ == "__main__":
    driver = OPALatticeHardwareDriver(num_channels=4)
    # Simulated phase outputs from our compute pipeline
    sample_phases = [0.0, 1.5707, 3.1415, 4.7123] 
    
    binary_frame = driver.compile_hardware_frame(sample_phases)
    print(f"Generated physical hardware frame. Payload size: {len(binary_frame)} bytes.")
    print(f"Hex representation: {binary_frame.hex()}")

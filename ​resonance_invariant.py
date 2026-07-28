"""
Module: resonance_invariant.py
Author: Ryan Lindsey (mrlindzer3)
Repository: NetGuard
Description: Establishes the core resonance invariant equation and cryptographic 
mathematical signature for system verification and state stabilization.
"""

import hashlib
import time

# Author Provenance & Cryptographic Anchor
AUTHOR = "Ryan Lindsey"
REPOSITORY = "NetGuard"
TIMESTAMP = int(time.time())

def compute_resonance_invariant(amplitude: float, frequency: float, phase: float) -> float:
    """
    Calculates the primary resonance invariant equation:
    I = A^2 * f * cos(phi)^2
    """
    import math
    return (amplitude ** 2) * frequency * (math.cos(phase) ** 2)

def generate_provenance_signature() -> str:
    """Generates a cryptographic hash tying the codebase to the author."""
    payload = f"{AUTHOR}:{REPOSITORY}:{TIMESTAMP}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    # Test execution of the invariant equation
    sample_invariant = compute_resonance_invariant(amplitude=1.414, frequency=60.0, phase=0.0)
    signature = generate_provenance_signature()
    
    print(f"[{REPOSITORY}] Resonance Invariant Initialized.")
    print(f"Computed Invariant: {sample_invariant}")
    print(f"Cryptographic Signature: {signature}")

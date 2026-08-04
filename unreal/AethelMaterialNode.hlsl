// Inputs to the Custom Node in UE5 Material Editor:
// - UV: Texture coordinates (UV)
// - NodeCount: Integer total of active aperiodic nodes (e.g., 4096)

// Note: _PhaseBuffer is bound via the C++ RDG system or Material Parameter Collection
uint Index = floor(UV.x * NodeCount);
if (Index >= NodeCount) {
    return float4(0, 0, 0, 1);
}

// Sample the computed phase value from our compute pass buffer
float PhaseVal = _PhaseBuffer[Index];

// Map the phase radians [0, 2*pi] into an RGB interference color spectrum
float3 InterferenceColor = sin(PhaseVal + float3(0.0, 2.094, 4.188)) * 0.5 + 0.5;

return float4(InterferenceColor, 1.0);

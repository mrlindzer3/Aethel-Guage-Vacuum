#version 430 core

// Define local workgroup size (e.g., 256 threads per workgroup)
layout(local_size_x = 256, local_size_y = 1, local_size_z = 1) in;

// Shader Storage Buffer Objects (SSBOs) for data binding
layout(std430, binding = 0) readonly buffer NodeBuffer {
    vec2 node_positions[];
};

layout(std430, binding = 1) writeonly buffer PhaseBuffer {
    float phase_outputs[];
};

// Engine Uniforms
uniform float u_steering_angle; // Target beam steering angle in radians
uniform float u_wavelength;     // Emitted light wavelength (e.g., 0.55 um)

void main() {
    uint index = gl_GlobalInvocationID.x;
    if (index >= node_positions.length()) return;

    vec2 pos = node_positions[index];
    
    // Wave number calculation
    float k = 6.28318530718 / u_wavelength;
    
    // Real-time spatial projection along steering vector
    float spatial_projection = pos.x * sin(u_steering_angle);
    
    // Compute wrapped phase delay [0, 2*pi]
    float phase_delay = mod(k * spatial_projection, 6.28318530718);
    
    phase_outputs[index] = phase_delay;
}

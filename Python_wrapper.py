import moderngl
import numpy as np

# 1. Initialize ModernGL Context (Headless / Offscreen Compute)
ctx = moderngl.create_standalone_context()

# 2. Define the GLSL Compute Shader Source
compute_shader_source = """
#version 430
layout(local_size_x = 256) in;

layout(std430, binding = 0) readonly buffer NodeBuffer {
    vec2 node_positions[];
};

layout(std430, binding = 1) writeonly buffer PhaseBuffer {
    float phase_outputs[];
};

uniform float u_steering_angle;
uniform float u_wavelength;

void main() {
    uint index = gl_GlobalInvocationID.x;
    if (index >= node_positions.length()) return;

    vec2 pos = node_positions[index];
    float k = 6.28318530718 / u_wavelength;
    float spatial_projection = pos.x * sin(u_steering_angle);
    float phase_delay = mod(k * spatial_projection, 6.28318530718);
    
    phase_outputs[index] = phase_delay;
}
"""

# Compile compute shader
compute_shader = ctx.compute_shader(compute_shader_source)

# 3. Generate sample node data (from our nested quasicrystal coordinates)
num_nodes = 4096
node_data = np.random.uniform(-15.0, 15.0, size=(num_nodes, 2)).astype('f4')

# Create GPU storage buffers
node_buffer = ctx.buffer(node_data.tobytes())
phase_buffer = ctx.buffer(reserve=num_nodes * 4) # 4 bytes per float32

# Bind buffers to shader storage binding points
node_buffer.bind_to_storage_buffer(0)
phase_buffer.bind_to_storage_buffer(1)

# Set uniforms
compute_shader['u_steering_angle'].value = np.radians(15.0) # 15 degree steering
compute_shader['u_wavelength'].value = 0.55                 # 550nm green light

# 4. Dispatch Compute Workgroups (e.g., 4096 nodes / 256 threads per group = 16 workgroups)
workgroups = (num_nodes + 255) // 256
compute_shader.run(workgroups=workgroups, x=1, y=1)

# 5. Retrieve processed phase outputs back from GPU memory
output_phases = np.frombuffer(phase_buffer.read(), dtype='f4')

print(f"Successfully computed phase shifts for {num_nodes} nodes on GPU.")
print(f"First 5 computed phase values (radians): {output_phases[:5]}")

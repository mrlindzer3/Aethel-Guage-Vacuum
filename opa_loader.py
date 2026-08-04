import moderngl
import numpy as np

def load_shader_source(filepath):
    """Utility to load external GLSL shader files for formal engine compilation."""
    with open(filepath, 'r') as f:
        return f.read()

# 1. Initialize Engine Context
ctx = moderngl.create_standalone_context()

# 2. Load the decoupled GLSL file from disk
shader_source = load_shader_source("opa_phase_kernel.glsl")
compute_shader = ctx.compute_shader(shader_source)

# 3. Setup data buffers (representing your node matrix)
num_nodes = 4096
node_data = np.random.uniform(-15.0, 15.0, size=(num_nodes, 2)).astype('f4')

node_buffer = ctx.buffer(node_data.tobytes())
phase_buffer = ctx.buffer(reserve=num_nodes * 4)

node_buffer.bind_to_storage_buffer(0)
phase_buffer.bind_to_storage_buffer(1)

# 4. Set Uniforms & Dispatch
compute_shader['u_steering_angle'].value = np.radians(15.0)
compute_shader['u_wavelength'].value = 0.55

workgroups = (num_nodes + 255) // 256
compute_shader.run(workgroups=workgroups, x=1, y=1)

# 5. Read back outputs (ready to feed into material graph or vertex attributes)
output_phases = np.frombuffer(phase_buffer.read(), dtype='f4')
print(f"Loaded external shader. Processed {num_nodes} nodes. Sample phase: {output_phases[0]:.4f}")

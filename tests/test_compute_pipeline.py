import numpy as np
import moderngl
import pytest

def test_opa_compute_kernel():
    # 1. Initialize Headless Context
    ctx = moderngl.create_standalone_context()
    
    # 2. Minimal compute shader for testing
    shader_src = """
    #version 430
    layout(local_size_x = 64) in;
    layout(std430, binding = 0) readonly buffer NodeBuffer { vec2 nodes[]; };
    layout(std430, binding = 1) writeonly buffer PhaseBuffer { float phases[]; };
    uniform float u_steering_angle;
    uniform float u_wavelength;
    
    void main() {
        uint idx = gl_GlobalInvocationID.x;
        if (idx >= nodes.length()) return;
        float k = 6.2831853 / u_wavelength;
        phases[idx] = mod(k * nodes[idx].x * sin(u_steering_angle), 6.2831853);
    }
    """
    
    shader = ctx.compute_shader(shader_src)
    
    # 3. Test data setup
    num_nodes = 128
    node_data = np.array([[1.0, 2.0], [-3.0, 4.0]] * 64, dtype='f4')
    
    node_buf = ctx.buffer(node_data.tobytes())
    phase_buf = ctx.buffer(reserve=num_nodes * 4)
    
    node_buf.bind_to_storage_buffer(0)
    phase_buf.bind_to_storage_buffer(1)
    
    shader['u_steering_angle'].value = np.radians(15.0)
    shader['u_wavelength'].value = 0.55
    
    # 4. Run execution
    shader.run(workgroups=2, x=1, y=1)
    
    # 5. Assertions
    output_phases = np.frombuffer(phase_buf.read(), dtype='f4')
    assert len(output_phases) == num_nodes
    assert not np.isnan(output_phases).any(), "Compute shader returned NaN values."
    assert np.all(output_phases >= 0.0), "Phase values dropped below zero wrapping boundary."

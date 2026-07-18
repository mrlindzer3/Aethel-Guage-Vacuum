// Vertex Shader: Semantic Light-Point Interpretation
#version 450 core
layout(location = 0) in vec4 semantic_node; // x, y, z, weight

uniform mat4 model_view_projection;
out float v_semantic_weight;

void main() {
    // Offset vertex based on semantic weight (representing local connectivity density)
    vec3 animated_pos = semantic_node.xyz + (semantic_node.w * 0.05 * sin(float(gl_VertexID)));
    
    gl_Position = model_view_projection * vec4(animated_pos, 1.0);
    gl_PointSize = 2.0 + semantic_node.w; // Nodes with higher connectivity appear brighter/larger
    v_semantic_weight = semantic_node.w;
}

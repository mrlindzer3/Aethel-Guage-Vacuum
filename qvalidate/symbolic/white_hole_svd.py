import sympy as sp

def white_hole_surface_svd(interaction_matrix):
    """
    Perform Singular Value Decomposition (SVD) on the holographic white hole 
    interaction matrix to extract principal topological modes and singular values.
    """
    # Compute U, singular values (S), and V^T symbolically
    U, S, V = interaction_matrix.singular_value_decomposition()
    return {
        "unitary_u": sp.simplify(U),
        "singular_values": sp.simplify(S),
        "unitary_v_transpose": sp.simplify(V),
        "is_invertible": sp.simplify(interaction_matrix.det() != 0)
    }

def isomorphic_white_hole_rendering_pipeline(metric_tensor, coupling_matrix):
    """
    Master pipeline integrating the optical white hole surface equation with 
    SVD mode filtering for high-fidelity holographic projection.
    """
    svd_results = white_hole_surface_svd(coupling_matrix)
    filtered_metric = sp.simplify(metric_tensor * svd_results["singular_values"])
    
    return {
        "svd_decomposition": svd_results,
        "rendered_surface_metric": filtered_metric
    }

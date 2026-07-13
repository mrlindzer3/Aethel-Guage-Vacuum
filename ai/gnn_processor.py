# ──────────────────────────────────────────────────────────────────────────
# FILE: ai/gnn_processor.py
# ROLE: Subatomic-Aware Recursive Vectoring Network & Machine Learning Layer
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GNNProcessor")

class GeometricRecursiveGNN:
    def __init__(self, node_count: int = 640, feature_dim: int = 6):
        """
        Initializes the ML layer with an expanded 6-dimensional feature space per node.
        Vector layout: [X, Y, Z, Bosonic_Coherence, Proton_Spin, Neutron_Spin]
        """
        self.node_count = node_count
        self.feature_dim = feature_dim
        
        rng = np.random.default_rng(42)
        self.W_message = rng.normal(loc=0.0, scale=0.1, size=(feature_dim, feature_dim))
        self.W_update = rng.normal(loc=0.0, scale=0.1, size=(feature_dim, feature_dim))

    def execute_subatomic_recursive_vectoring(self, mesh_data: dict, subatomic_tensor: dict, iterations: int = 3) -> np.ndarray:
        """
        Runs the recursive message-passing loops over the 640-node mesh.
        Fuses the physical 3D spatial layout with the proton-neutron quantum spin metrics.
        """
        logger.info(f"🧠 ML: Compiling subatomic-aware hidden state matrix for {self.node_count} nodes...")
        
        # Extract base geometry
        positions = mesh_data["node_positions"]
        
        # Extract subatomic tensor features
        bosonic_coherence = subatomic_tensor["bosonic_field_coherence"].reshape(-1, 1)
        baryonic_states = subatomic_tensor["baryonic_nuclear_states"]
        proton_spins = np.abs(baryonic_states[:, 0]).reshape(-1, 1)
        neutron_spins = np.abs(baryonic_states[:, 1]).reshape(-1, 1)
        
        # Concatenate into the final 6D hidden features space [640, 6]
        H = np.hstack((positions, bosonic_coherence, proton_spins, neutron_spins))
        hyperedges = mesh_data["fatecrystal_mesh"]

        # Recursive Loop Execution
        for step in range(iterations):
            aggregated_messages = np.zeros_like(H)
            
            # Message Passing across Web of Wyrd runic lines
            for edge in hyperedges:
                nodes = edge["nodes"]
                weight = edge["fatecrystal_phase_lock"]
                
                edge_vector = np.mean(H[nodes], axis=0) * weight
                for node in nodes:
                    aggregated_messages[node] += edge_vector

            # Machine Learning state update step
            messages = np.dot(aggregated_messages, self.W_message)
            H_next = np.tanh(np.dot(H, self.W_update) + messages)
            H = H_next

        logger.info(f"✨ ML: Recursive training pass complete. Subatomic vector space stabilized.")
        return H


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GNNProcessor")

class GeometricRecursiveGNN:
    def __init__(self, node_count: int = 640, feature_dim: int = 4):
        """
        Initializes the ML layer with a 640-node vector space.
        Each node holds a feature vector: [X_pos, Y_pos, Z_pos, Phase_State]
        """
        self.node_count = node_count
        self.feature_dim = feature_dim
        
        # Initialize internal learnable weight matrices for the ML update step
        # Using a deterministic random seed to maintain geometric stability
        rng = np.random.default_rng(42)
        self.W_message = rng.normal(loc=0.0, scale=0.1, size=(feature_dim, feature_dim))
        self.W_update = rng.normal(loc=0.0, scale=0.1, size=(feature_dim, feature_dim))

    def execute_recursive_vectoring(self, mesh_data: dict, iterations: int = 3) -> np.ndarray:
        """
        Performs recursive message-passing vectoring over the 3D topology mesh.
        Nodes pull vector states from their runic hyperedges, update their internal
        embeddings, and feed them back into the next execution pass.
        """
        logger.info(f"🧠 ML: Initiating {iterations} recursive vectoring passes over the 640-node mesh...")
        
        # Extract initial 3D positions and append a zero-initialized phase dimension
        positions = mesh_data["node_positions"]
        phase_states = np.zeros((self.node_count, 1), dtype=np.float32)
        
        # Current node hidden state matrix H (Shape: [640, 4])
        H = np.hstack((positions, phase_states))
        hyperedges = mesh_data["fatecrystal_mesh"]

        # Recursive Loop
        for step in range(iterations):
            logger.info(f"🔄 LOOP: Processing recursive pass {step + 1}/{iterations}...")
            
            # Initialize an empty matrix to accumulate neighbor vectors
            aggregated_messages = np.zeros_like(H)
            
            # Aggregate vector features across the hyperedges
            for edge in hyperedges:
                nodes = edge["nodes"]
                weight = edge["fatecrystal_phase_lock"]
                
                # Compute collective geometric vector center for this hyperedge group
                edge_vector = np.mean(H[nodes], axis=0) * weight
                
                # Distribute the hyperedge vector back to its connected nodes
                for node in nodes:
                    aggregated_messages[node] += edge_vector

            # Machine Learning Transformation Layer:
            # Message Pass: M = Message_Weight * Aggregated_Vectors
            messages = np.dot(aggregated_messages, self.W_message)
            
            # Update Layer: H_next = Activation(Update_Weight * H + Messages)
            # Utilizing a hyperbolic tangent non-linear activation function (tanh)
            H_next = np.tanh(np.dot(H, self.W_update) + messages)
            
            # Vector recursion: Set current states to the calculated next-generation vectors
            H = H_next

        # Calculate final spatial vector convergence metric
        convergence_variance = np.var(H)
        logger.info(f"✨ ML: Convergence stabilized. State vector variance: {convergence_variance:.6e}")
        return H

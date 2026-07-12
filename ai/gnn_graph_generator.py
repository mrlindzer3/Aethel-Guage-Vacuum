# ──────────────────────────────────────────────────────────────────────────
# FILE: ai/gnn_graph_generator.py
# ROLE: Fields-to-Graph Structural Data Converter for GNN Pipeline
# ENGINEER: Ryan Taylor Lindsey
# ──────────────────────────────────────────────────────────────────────────

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GNNGraphGenerator")

class GNNGraphGenerator:
    def __init__(self):
        logger.info("🕸️ GNN PREP: Initializing Graph Topology Converter...")

    def transform_field_to_graph(self, vacuum_field: np.ndarray, phase_mask: np.ndarray):
        """
        Converts active 2D field tensors into graph node features and edge indices.
        Each node retains local phase and field amplitude as a feature vector.
        """
        logger.info("🕸️ GNN PREP: Mapping field coordinates to node feature space...")
        rows, cols = vacuum_field.shape
        num_nodes = rows * cols
        
        # 1. Generate Node Features: [Real_Amplitude, Imag_Amplitude, Phase_Mask]
        node_features = []
        for r in range(rows):
            for c in range(cols):
                val = vacuum_field[r, c]
                mask_val = phase_mask[r, c] if r < phase_mask.shape[0] and c < phase_mask.shape[1] else 0.0
                node_features.append([val.real, val.imag, float(mask_val)])
        
        x = np.array(node_features, dtype=np.float32)
        
        # 2. Construct Edges (Nearest-Neighbor Spatial Coupling)
        edge_indices = []
        edge_attributes = []
        
        for r in range(rows):
            for c in range(cols):
                current_node = r * cols + c
                # Check neighbors (Right and Down to avoid duplicate undirected edges)
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if nr < rows and nc < cols:
                        neighbor_node = nr * cols + nc
                        edge_indices.append([current_node, neighbor_node])
                        # Edge weight represents spatial Euclidean distance step metric
                        edge_attributes.append([1.0]) 
                        
        edge_index = np.array(edge_indices, dtype=np.int64).T
        edge_attr = np.array(edge_attributes, dtype=np.float32)
        
        logger.info(f"📊 GNN PREP: Graph conversion complete. Nodes: {num_nodes}, Edges: {edge_index.shape[1]}")
        return {
            "x": x,                 # Node feature matrix
            "edge_index": edge_index, # Graph topology connectivity matrix
            "edge_attr": edge_attr   # Edge spatial properties
        }

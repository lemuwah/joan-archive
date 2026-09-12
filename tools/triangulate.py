"""
Triangulation script for Joan-Archive network analysis.
Performs projection, centrality analysis, and null-model benchmarking.
"""

import networkx as nx
from networkx.algorithms import bipartite
import pandas as pd
import numpy as np
import json
import os

def run_triangulation():
    df_edges = pd.read_csv("data/network/bipartite_edges.csv")
    
    B = nx.Graph()
    for _, row in df_edges.iterrows():
        B.add_node(row["source"], bipartite=0, node_type="person", tier=row["tier"])
        B.add_node(row["target"], bipartite=1, node_type="document")
        B.add_edge(row["source"], row["target"], role=row["role"], contamination=row["contamination"])
        
    persons = [n for n, d in B.nodes(data=True) if d.get("bipartite") == 0]
    
    # Person-person projection (co-document network)
    P = bipartite.projected_graph(B, persons)
    
    # Centrality measures on person network
    deg_cent = nx.degree_centrality(P)
    betweenness = nx.betweenness_centrality(P)
    
    # Load document metrics
    df_metrics = pd.read_csv("data/network/person_metrics.csv")
    df_metrics["degree_centrality"] = df_metrics["person"].map(deg_cent)
    df_metrics["betweenness_centrality"] = df_metrics["person"].map(betweenness)
    
    os.makedirs("research_findings", exist_ok=True)
    df_metrics.to_csv("research_findings/network_triangulation_metrics.csv", index=False)

if __name__ == "__main__":
    run_triangulation()

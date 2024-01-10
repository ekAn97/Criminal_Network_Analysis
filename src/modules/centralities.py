import numpy as np
import pandas as pd 
import networkx as nx
import operator
from modules.efficiency import harmonic_mean

def centralities(G, df0):

    df = pd.DataFrame()
    denom = len(G.nodes()) - 1
    # Add nodes
    df["Nodes"] = [node for node in G.nodes()]
    
    # Betweenness
    bet_d = nx.betweenness_centrality(G, weight="distance")
    df["Betweenness"] = [v1 for k1, v1 in bet_d.items()]
    
    # Pagerank
    pager_d = nx.pagerank(G, alpha=0.85, weight="weight")
    df["PR"] = [v1 for k1, v1 in pager_d.items()]
    
    if G.is_directed() == False:
        # Degree Centrality
        df["Degree"] = [nx.degree_centrality(G)[k1] for k1 in nx.degree_centrality(G)]
        # Strength Centrality
        strength_d = dict(nx.degree(G, weight="weight"))
        df["Strength"] = [strength_d[i] * harmonic_mean(G, "weight") for i in strength_d.keys()]
        # Eigenvector
        eigen_d = nx.eigenvector_centrality_numpy(G, weight="weight")
        df["Eigen"] = [v1 for k1, v1 in eigen_d.items()]
        # Harmonic
        harm_d = nx.harmonic_centrality(G, distance="distance")
        df["Harmonic"] = [v1 for k1, v1 in harm_d.items()]
        # Katz
        katz_d = nx.katz_centrality_numpy(G, weight="weight")
        df["Katz"] = [v1 for k1, v1 in katz_d.items()]
    	
    else:
        # Reversed Graph
        Grev = G.reverse(copy=True)
        # In-Degree
        in_deg = nx.in_degree_centrality(G)
        df["In-Degree"] = [v1 for k1, v1 in in_deg.items()]
        # Out-Degree
        out_deg = nx.out_degree_centrality(G)
        df["Out-Degree"] = [v1 for k1, v1 in out_deg.items()]
        # In Strength
        in_str = dict(G.in_degree(weight="weight"))
        for i in in_str.keys():
            in_str[i] = in_str[i] * harmonic_mean(G, "weight")
        df["In-Strength"] = [v1 for k1, v1 in in_str.items()]
        # Out Strength
        out_str = dict(G.out_degree(weight="weight"))
        for i in out_str.keys():
            out_str[i] = out_str[i] * harmonic_mean(G, "weight")
        df["Out-Strength"] = [v1 for k1, v1 in out_str.items()]
        # In Harmonic
        in_harm = nx.harmonic_centrality(G, distance="distance")
        df["In-Harmonic"] = [v1 for k1, v1 in in_harm.items()]
        # Out Harmonic
        out_harm = nx.harmonic_centrality(Grev, distance="distance")
        df["Out-Harmonic"] = [v1 for k1, v1 in out_harm.items()]
        
    return df


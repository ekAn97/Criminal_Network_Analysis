import pandas as pd
import networkx as nx
import numpy as np

from modules.efficiency import global_eff
from modules.efficiency import harmonic_mean
from modules.glob_eff import eff_un
def glob_metrics(G, mode):

    metrics = {"n": len(G.nodes()), "m": len(G.edges()), 
               "Density": nx.density(G), 
               "Cluster": nx.average_clustering(G, weight = "weight")}
    
    if mode == "undirected":
        metrics.update({"AssortD": nx.degree_pearson_correlation_coefficient(G,
                                                                             weight = None), 
                        "AssortS": nx.degree_pearson_correlation_coefficient(G,
                                                                             weight = "weight"),
        "Global Efficiency": eff_un(G, "distance"), 
        "LCC Size": len(max(nx.connected_components(G), key=len)),\
            "Av.Degree": (2*len(G.edges())) / len(G.nodes()),\
                "Max Degree": max([k[1] for k in nx.degree(G)])})
    elif mode == "directed":
        metrics.update({"InInAssortD":\
                        nx.degree_pearson_correlation_coefficient(G, \
                                                                  x="in",\
                                                                      y="in",\
                                                                          weight = None), 
                            "InOutAssortD": nx.degree_pearson_correlation_coefficient(G, 
                                                                                      x="in", 
                                                                                      y="out", 
                                                                                      weight = None), 
                            "OutOutAssortD": nx.degree_pearson_correlation_coefficient(G, 
                                                                                       x="out", 
                                                                                       y="out", 
                                                                                       weight = None),
                            "InInAssortS": nx.degree_pearson_correlation_coefficient(G,
                                                                                     x="in", 
                                                                                     y="in", 
                                                                                     weight = "weight"), 
                            "InOutAssortS": nx.degree_pearson_correlation_coefficient(G, 
                                                                                      x="in", 
                                                                                      y="out", 
                                                                                      weight = "weight"),
                            "OutOutAssortS":nx.degree_pearson_correlation_coefficient(G, 
                                                                                      x="out", 
                                                                                      y="out", 
                                                                                      weight = "weight"), 
                            "LCC Size(Strong)": len(max(nx.strongly_connected_components(G), 
                                                        key=len)), 
                            "LCC Size(Weak)": len(max(nx.weakly_connected_components(G), 
                                                      key=len)), 
                            "Av.Degree": len(G.edges()) / len(G.nodes()), 
                            "Max-In Deg": max([values *\
                                               (len(G.nodes()) - 1) for key,\
                                                   values in nx.in_degree_centrality(G).items()]), 
                                "Max-Out Deg": max([values *\
                                                    (len(G.nodes()) - 1) for key,\
                                                        values in nx.out_degree_centrality(G).items()]),
                                    "In-Global-Efficiency": global_eff(G, 
                                                                       "distance",
                                                                       "in"),
                                    "Out-Global-Efficiency": global_eff(G,
                                                                        "distance",
                                                                        "out")})
        
    return pd.Series(metrics)

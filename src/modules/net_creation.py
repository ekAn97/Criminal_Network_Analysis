import pandas as pd
import numpy as np
import networkx as nx


def net_creation(df:pd.DataFrame, method):
    ''' Creating the network from a dataframe, normalizing
    the weights and assigning a distance attribute
    
    Input
    -----
    df: pandas DataFrame (weighted matrix)
    method: nx.Graph or nx.DiGraph
    
    Output
    ------
    networkx object
    
    '''
    G = nx.from_pandas_adjacency(df, create_using = method)
    # Normalized Distance Attribute
    for key in list(G.edges):
        nx.set_edge_attributes(G, 
                               {key: 1 / nx.get_edge_attributes(G, 
                                                                "weight")[key]}, 
                               name = "distance")
    for u, v, d in G.edges(data = True):
        d["distance"] /= max(nx.get_edge_attributes(G, "distance").values())
    
    # Normalizing the weights
    for u, v, w in G.edges(data = True):
        w["weight"] /= max(nx.get_edge_attributes(G, "weight").values())
        
    return G

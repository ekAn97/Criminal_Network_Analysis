import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sb
import os
import copy
import statistics as st
import operator
import sys

# Custom libraries
sys.path.append('/home/kostasan00/Desktop/criminal_nets/src/modules/')

from modules.efficiency import global_eff
from modules.efficiency import harmonic_mean
from modules.gmetrics import glob_metrics
from modules.centralities import centralities

####################################### F U N C T I O N S ######################################

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
        nx.set_edge_attributes(G,\
                               {key: 1 / nx.get_edge_attributes(G,\
                                                                "weight")[key]},\
                                   name = "distance")
    for u, v, d in G.edges(data = True):
        d["distance"] /= max(nx.get_edge_attributes(G, "distance").values())
    
    # Normalizing the weights
    for u, v, w in G.edges(data = True):
        w["weight"] /= max(nx.get_edge_attributes(G, "weight").values())
        
    return G

def randomize(n, p, mode, i0):
    ''' Creates multiple ER networks, calculates
    Clustering Coefficient and AvSPL and gets 
    the mean values and standard deviations of 
    the calculations.
    
    
    
    INPUT
    -----
    n: int (number of nodes)
    p: float (probability threshold)
    mode: "undirected" or "directed"
    i0: int (number of desired iterations)
    
    OUTPUT
    ------
    '''
    clust_c = []
    av_spl = []
    
    for i in range(i0):
        G_rand = nx.erdos_renyi_graph(n, p, seed=None, directed=mode)
        clust_c.append(nx.average_clustering(G_rand))
        av_spl.append(nx.average_shortest_path_length(G_rand))
            
    df = pd.DataFrame({"Measure": ["Mean", "StDev"], 
                       "Clustering": [st.mean(clust_c), st.stdev(clust_c)], 
                       "AvSPL": [st.mean(av_spl), st.stdev(av_spl)]})
    
    return df
####################################### M A I N  S C R I P T ###################################
    
# Specify Folder
folder_path = "/home/kostasan00/Desktop/criminal_nets/data/"
s_path = "/home/kostasan00/Desktop/criminal_nets/results/time_averaged/"

# Dictionary that contains the files
file_d = {"undirected": "CAVIAR_FULL_Undirected.csv", 
          "directed": "CAVIAR_FULL_Directed.csv"}

for key, value in file_d.items():
    df = pd.read_csv(folder_path + value, header = 0, index_col = 0)
    df.fillna(0, inplace = True)
    df.index = df.index.astype("str")
    
    # U N D I R E C T E D  case
    if key == "undirected":
        G = net_creation(df, nx.Graph)
        Gcopy = copy.deepcopy(G) # Backup File (just in case)
        
        # Save Path
        spath = s_path + "undirected/structure/"       
        
    # D I R E C T E D  case    
    elif key == "directed":
        G = net_creation(df, nx.DiGraph)
        Gcopy = copy.deepcopy(G)
        
        # Save Path
        spath = s_path + "/directed/structure/"
    
    ### M E T R I C S  C A L C U L A T I O N ###    
    # Global Metrics
    g_metrics = glob_metrics(G, key)
    g_metrics.to_csv(spath + "GMetrics_" + key + ".csv", header=False,\
                     index=True)
    
    # Randomizations
    #randz = randomize(len(G.nodes()), 0.5, key, 1000)
    #randz.to_csv(spath + "Randz_" + key + ".csv", header=True, index=False)
    
    # Centralities(key-players)
    key_pl = centralities(G, df)
    key_pl.to_csv(spath + "Centralities_" + key + ".csv", header=True,\
                  index=False)
    


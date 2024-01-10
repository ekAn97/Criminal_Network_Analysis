import sys
import pandas as pd
import numpy as np
import networkx as nx
import copy
import operator
import random
import glob_eff


#------------------------------------------ F U N C T I O N S ---------------------------------

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
        nx.set_edge_attributes(G, {key: 1 / nx.get_edge_attributes(G, "weight")[key]}, name = "distance")
    for u, v, d in G.edges(data = True):
        d["distance"] /= max(nx.get_edge_attributes(G, "distance").values())
    
    # Normalizing the weights
    for u, v, w in G.edges(data = True):
        w["weight"] /= max(nx.get_edge_attributes(G, "weight").values())
        
    return G
    
    
def lcc(G, mode):
    ''' Returns the LCC. If network is directed, 
    it returns the Largest Weakly Connected Component.
    
    INPUT
    -----
    G: networkx Graph Object
    mode: "directed" or "undirected"
    
    OUTPUT
    ------
    LCC: graph object
    
    '''
    if mode == "directed":
        lcc = max(nx.strongly_connected_components(G), key = len)
    elif mode == "undirected":
        lcc = max(nx.connected_components(G), key = len)
        
    return G.subgraph(lcc)
    
    
def disruption(G, lcc_0, cc_0, eff_0, comp_0, lcc_df, cc_df, eff_df, comp_df, method, mode, gen):
    lcc_dict = {}
    cc_dict = {}
    eff_dict = {}
    comp_dict = {}
    i0 = 0
    rem_nodes = []
    
    while G.number_of_nodes() > n:
        i1 = 0
        
        if method == 1: # BLOCK
            rem_nodes = []
            lcc_dict[i0] = lcc(G, mode).number_of_nodes()
            cc_dict[i0] = nx.average_clustering(G, weight = "weight")
            eff_dict[i0] = glob_eff.global_efficiency(G, weight = "distance")
            comp_dict[i0] = nx.number_connected_components(G)
            
            rem_nodes = list(G.nodes)
            random.shuffle(rem_nodes)
        while i1 < n:
            if G.number_of_nodes() <= n:
                break
            if method == 2: # CASCADAL
                rem_nodes = []
                lcc_dict[i0] = lcc(G, mode).number_of_nodes()
                cc_dict[i0] = nx.average_clustering(G, weight = "weight")
                eff_dict[i0] = glob_eff.global_efficiency(G, weight = "distance")
                comp_dict[i0] = nx.number_connected_components(G)
                
                rem_nodes = list(G.nodes)
                random.shuffle(rem_nodes)
                
            G.remove_node(rem_nodes[0])
            rem_nodes.pop(0)
            i0 += 1
            i1 += 1
            
    lcc_df["Iteration"] = list(lcc_dict.keys())
    cc_df["Iteration"] = lcc_df["Iteration"]
    eff_df["Iteration"] = lcc_df["Iteration"]
    comp_df["Iteration"] = lcc_df["Iteration"]
    
    lcc_df[str(gen)] = list(lcc_dict.values())
    cc_df[str(gen)] = list(cc_dict.values())
    eff_df[str(gen)] = list(eff_dict.values())
    comp_df[str(gen)] = list(comp_dict.values())

    return lcc_df, cc_df, eff_df, comp_df

#----------------------------------------------- S C R I P T --------------------------------

arguments = len(sys.argv)
print("Number of Arguments:", arguments)
print("\nScript name:", sys.argv[0])
print("\nPassed arguments:", end = " ")
for _ in range(1, arguments):
    print(sys.argv[_], end = " ")
    
# Setting Variables
file_name = sys.argv[1]
mode = sys.argv[2]
b_percent = sys.argv[3]

# Network creation
df = pd.read_csv("Dataset/" + file_name + ".csv", header = 0, index_col = 0)
df.fillna(0, inplace = True)
df.index = df.index.astype("str")

if mode == "directed":
    G = net_creation(df, nx.DiGraph)
elif mode == "undirected":
    G = net_creation(df, nx.Graph)
    
# Copy of Graph
Gcopy = copy.deepcopy(G)

# Disruption
method = {1: "BLOCK", 2: "CASCADE"}
n = round((len(G.nodes()) * int(b_percent)) / 100)

lcc_0 = len(lcc(G, sys.argv[2]))
cc_0 = nx.average_clustering(G, weight = "weight")
eff_0 = glob_eff.global_efficiency(G, weight = "distance")
comp_0 = nx.number_connected_components(G)

for i, j in method.items():
    if i == 2:
        break
    
    lcc_df = pd.DataFrame()
    cc_df = pd.DataFrame()
    eff_df = pd.DataFrame()
    comp_df = pd.DataFrame()
    
    for k in range(1, 1000):
         lcc_df, cc_df, eff_df, comp_df = disruption(copy.deepcopy(Gcopy), lcc_0, cc_0, eff_0, comp_0, lcc_df, cc_df, eff_df, comp_df, i, mode, k)
         
    # Storing as .xlsx file
    xl_name = "Results_Rand_" + j + str(n) + ".xlsx"
    lcc_df.to_excel(xl_name, sheet_name = "LCC")
    
    with pd.ExcelWriter(xl_name, mode = "a") as writer:
        cc_df.to_excel(writer, sheet_name = "Clustering")
        eff_df.to_excel(writer, sheet_name = "Efficiency")
        comp_df.to_excel(writer, sheet_name = "Components #")

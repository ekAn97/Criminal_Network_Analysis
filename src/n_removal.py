import sys
import pandas as pd
import numpy as np
import networkx as nx
import copy
import operator
import glob_eff
import array

#--------------------------------------- F U N C T I O N S ------------------------------

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
    

def wdegree_c(G, weight):
    '''
    '''
    denom = len(G.nodes()) - 1
    
    if mode == "undirected":
        if weight == "None":
            return nx.degree_centrality(G)
        elif weight == "weight":
            return {nodes: d / denom for nodes, d in G.degree(weight = "weight")}
    elif mode == "directed":
        if weight == "None" and centr_name == "In_Degree":
            return nx.in_degree_centrality(G)
        elif weight =="None" and centr_name == "Out_Degree":
            return nx.out_degree_centrality(G)
        elif weight == "weight" and centr_name == "In_Strength":
            wdeg_in = {}
            for i in list(G.nodes()):
                wdeg_in[i] = sum(df.loc[:, i].values)
            return wdeg_in
        elif weight == "weight" and centr_name == "Out_Strength":
            wdeg_out = {}
            for i in list(G.nodes()):
                wdeg_out[i] = sum(df.loc[i, :].values)
            return wdeg_out
            

def key_players(G, centrality, key_pl, weight):
    ''' Finds the most prominent actor(s) in the network
    
    INPUT
    -----
    G: networkx Graph Object
    centrality: networkx centrality function
    weight: "weight" or "distance"
    
    OUTPUT
    ------
    key_pl: list with highest scoring actors
    
    '''
    # Centrality computation and sorting in descending order
    centr_dict = centrality(G, weight = weight)
    sorted_dict = sorted(centr_dict.items(), key = operator.itemgetter(1), reverse = True)
    
    # Gathering the names of the players
    for _ in sorted_dict:
        key_pl.append(_[0])
        
    return key_pl
    
    
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
    
    
def disruption(G, centrality, centr_name, lcc_0, cc_0, eff_0, comp_0, lcc_df, cc_df, eff_df, comp_df, method, weight, mode):
    '''
    Node removal process: either cascadal eiter per block. It 
    calculates the LCC size, Average Geodesic Length and Global Efficiency.
    
    INPUT
    -----
    G: networkx Graph Object
    
    OUTPUT
    ------
    lcc_df: pandas Dataframe (ITER, LCC SIZE)
    cc_df: pandas Dataframe (ITER, Clustering Coefficient)
    eff_df: pandas Dataframe (ITER, Global Efficiency)
    
    '''
    lcc_dict = {} # LCC size
    cc_dict = {}  # Clustering Coefficient
    eff_dict = {} # Global Efficiency
    comp_dict = {} # Number of components
    i0 = 0
    rem_nodes = []
    
    while G.number_of_nodes() > n:
        i1 = 0
        
        if method == 1: # BLOCK REMOVAL 
            rem_nodes = []
            
            lcc_dict[i0] = lcc(G, mode).number_of_nodes()
            cc_dict[i0] = nx.average_clustering(G, weight = "weight")
            eff_dict[i0] = glob_eff.global_efficiency(G, weight = "distance")
            comp_dict[i0] = nx.number_strongly_connected_components(G)
            
            if centr_name == "Out_Katz" or centr_name == "Out_Harmonic":
                Grev = G.reverse(copy = True)
                rem_nodes = key_players(Grev, centrality, rem_nodes, weight)
            else:
                rem_nodes = key_players(G, centrality, rem_nodes, weight)
                
        while i1 < n:
            if G.number_of_nodes() <= n:
                break
            if method == 2: # CASCADAL REMOVAL 
                rem_nodes = []
                lcc_dict[i0] = lcc(G, mode).number_of_nodes()
                cc_dict[i0] = nx.average_clustering(G, weight = "weight")
                eff_dict[i0] = glob_eff.global_efficiency(G, weight = "distance")
                comp_dict[i0] = nx.number_strongly_connected_components(G)
                
                if centr_name == "Out_Katz" or centr_name == "Out_Harmonic":
                    Grev = G.reverse(copy = True)
                    rem_nodes = key_players(Grev, centrality, rem_nodes, weight)
                else:
                    rem_nodes = key_players(G, centrality, rem_nodes, weight)
                    
            G.remove_node(rem_nodes[0])
            rem_nodes.pop(0)
            i0 += 1
            i1 += 1
            
    lcc_df["Iteration"] = list(lcc_dict.keys())
    cc_df["Iteration"] = lcc_df["Iteration"]
    eff_df["Iteration"] = lcc_df["Iteration"]
    comp_df["Iteration"] = lcc_df["Iteration"]
    
    lcc_df[centr_name] = list(lcc_dict.values())
    cc_df[centr_name] = list(cc_dict.values())
    eff_df[centr_name] = list(eff_dict.values())
    comp_df[centr_name] = list(comp_dict.values())
    
    return lcc_df, cc_df, eff_df, comp_df
    
#------------------------------------------ M A I N  S C R I P T ------------------------------

arguments = len(sys.argv)
print("Number of Arguments:", arguments)
print("\nScript name:", sys.argv[0])
print("\nPassed arguments:", end = " ")
for _ in range(1, arguments):
    print(sys.argv[_], end = " ")
    
# Setting Variables
file_name = sys.argv[1]
mode = sys.argv[2]
centr = eval(sys.argv[3])
centr_name = sys.argv[4]
attr = sys.argv[5]
b_percent = sys.argv[6]

# Network Creation
df = pd.read_csv("Dataset/" + file_name + ".csv", header = 0, index_col = 0)
df.fillna(0, inplace = True)
df.index = df.index.astype("str")

G = net_creation(df, nx.DiGraph)
Gcopy = copy.deepcopy(G)    

# Disruption Process
lcc_0 = len(lcc(G, mode))
cc_0 = nx.average_clustering(G, weight = "weight")
eff_0 = glob_eff.global_efficiency(G, weight = "distance")
comp_0 = nx.number_strongly_connected_components(G)

method = {1: "BLOCK", 2: "CASCADE"}
n = round((len(G.nodes()) * int(b_percent)) / 100)

for i, j in method.items():
    lcc_df = pd.DataFrame()
    cc_df = pd.DataFrame()
    eff_df = pd.DataFrame()
    comp_df = pd.DataFrame()
    
    lcc_df, cc_df, eff_df, comp_df = disruption(copy.deepcopy(Gcopy), centr, centr_name, lcc_0, cc_0, eff_0, comp_0, lcc_df, cc_df, eff_df, comp_df, i, attr, mode)
    
    # Storing results in Excel sheets
    xl_name = "Results_" + j + "_" + centr_name + ".xlsx"
    lcc_df.to_excel(xl_name, sheet_name = "LCC")
    
    with pd.ExcelWriter(xl_name, mode = "a") as writer:
        cc_df.to_excel(writer, sheet_name = "Clustering")
        eff_df.to_excel(writer, sheet_name = "Efficiency")
        comp_df.to_excel(writer, sheet_name = "Components #")

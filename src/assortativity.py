import sys
import pandas as pd
import numpy as np
import networkx as nx
import random
import operator
import copy
# Custom function
sys.path.append('/home/kostasan00/Desktop/criminal_nets/src/modules/')

from modules.net_creation import net_creation

#----------------------------------- F U N C T I O N S -----------------------------------

def st_errorj(obs_stat: float, sampled_stat: list):
    ''' Standard error calculation for the
    jackknife procedure.
    
    INPUT
    -----
    obs_stat: float -> The observed statistic
    sampled_stat: list -> List with the calculated statistics
    
    OUTPUT
    ------
    float
    '''
    radicand = sum([pow((i - obs_stat), 2) for i in sampled_stat])
    
    return np.sqrt(radicand)
    
    
 #------------------------------------- M A I N ------------------------------------------
 
arguments = len(sys.argv)
print("Number of Arguments:", arguments)
print("\nScript name:", sys.argv[0])
print("\nPassed arguments:", end = " ")
for _ in range(1, arguments):
    print(sys.argv[_], end = " ")
    
# Setting Variables
file_name = sys.argv[1]
mode = sys.argv[2]

# Network Creation
df = pd.read_csv("Dataset/" + file_name + ".csv", header = 0, index_col = 0)
df.fillna(0, inplace = True)
df.index = df.index.astype("str")

if mode == "directed":
    G = net_creation(df, nx.DiGraph)
    
    # Assortativity
    iideg_r0 = nx.degree_pearson_correlation_coefficient(G, x="in", y="in", weight=None)
    iodeg_r0 = nx.degree_pearson_correlation_coefficient(G, x="in", y="out", weight=None)
    oideg_r0 = nx.degree_pearson_correlation_coefficient(G, x="out", y="in", weight=None)
    oodeg_r0 = nx.degree_pearson_correlation_coefficient(G, x="out", y="out", weight=None)
    
    iideg_s0 = nx.degree_pearson_correlation_coefficient(G, x="in", y="in", weight="weight")
    iodeg_s0 = nx.degree_pearson_correlation_coefficient(G, x="in", y="out", weight="weight")
    oideg_s0 = nx.degree_pearson_correlation_coefficient(G, x="out", y="in", weight="weight")
    oodeg_s0 = nx.degree_pearson_correlation_coefficient(G, x="out", y="out", weight="weight")
    
    # Observed Assortativities
    obs_assort = [iideg_r0, iodeg_r0, oideg_r0, oideg_r0, oodeg_r0, iideg_s0, iodeg_s0, oideg_s0, oodeg_s0]
    
    # Jackknife
    jackknife_dict = {"In-In Deg": [], "In-Out Deg": [], "Out-In Deg": [], "Out-Out Deg": [], "In-In Str": [], "In-Out Str": [], "Out-In Str": [], "Out-Out Str": []}
    
    for i in list(G.edges()):
        Gcopy = copy.deepcopy(G)
        # Remove i-th edge
        Gcopy.remove_edge(i[0], i[1])
        # Calculate assortativities
        jackknife_dict["In-Out Deg"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="in", y="out", weight=None))
        jackknife_dict["In-Out Deg"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="in", y="out", weight=None))
        jackknife_dict["Out-In Deg"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="out", y="in", weight=None))
        jackknife_dict["Out-Out Deg"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="out", y="out", weight=None))
        
        jackknife_dict["In-In Str"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="in", y="in", weight="weight"))
        jackknife_dict["In-Out Str"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="in", y="out", weight="weight"))
        jackknife_dict["Out-In Str"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="out", y="in", weight="weight"))
        jackknife_dict["Out-Out Str"].append(nx.degree_pearson_correlation_coefficient(Gcopy, x="out", y="out", weight="weight"))

elif mode == "undirected":
    G = nc.net_creation(df, nx.Graph)
    
    # Assortativity
    obs_assort = [nx.degree_pearson_correlation_coefficient(G, weight=i) for i in [None, "weight"]]
    
    # Jackknife
    jackknife_dict = {"Deg": [], "Str": []}
    
    for i in list(G.edges()):
        Gcopy = copy.deepcopy(G)
        # Remove i-th edge
        Gcopy.remove_edge(i[0], i[1])
        # Sampled Assortativity
        jackknife_dict["Deg"].append(nx.degree_pearson_correlation_coefficient(Gcopy, weight=None))
        jackknife_dict["Str"].append(nx.degree_pearson_correlation_coefficient(Gcopy, weight="weight"))
        

# Data Frame with assortativities and errors
assort_dict = dict()    
for i, j in zip(jackknife_dict, obs_assort):
    assort_dict[i] = [j, st_errorj(j, jackknife_dict[i])]
    
assort_df = pd.DataFrame(assort_dict.values(), index=assort_dict.keys(), columns=["Value", "Error"])
assort_df.to_csv(f"Assortativities-{mode}.csv", header=True, index=True) 
        
        

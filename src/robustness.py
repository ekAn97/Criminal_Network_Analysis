#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 15:08:40 2023

@author: kostasan00
"""

##############################################################################
#                                                                            #
#                               L I B R A R I E S                            #
#                                                                            #
##############################################################################

import pandas as pd
import networkx as nx 
import numpy as np
import math


##############################################################################
#                                                                            #
#                          C U S T O M  F U N C T I O N S                    #
#                                                                            #
##############################################################################


def robust(n, t, values_1, values_2, max_removal):
    ''' Calculates the robustness
    measure, given a specific threshold 
    where NCC maximizes.
    
    INPUT
    -----
    n: int(number of nodes)
    t: int(threshold)
    values_1: list of values of LCC size
    values_2: list of number of removed nodes
    OUTPUT
    ------
    robustness: float

    '''
    values = []
    for _ in range(t):
        value = (1 / (n - values_2[_])) * values_1[_]
        values.append(value)
        
    return (1 / (max_removal + 1)) * sum(values)


##############################################################################
#                                                                            #
#                                    M A I N                                 #  
#                                                                            #
##############################################################################

df_adj = pd.read_csv("Dataset/CAVIAR_FULL_Undirected.csv",\
                     header=0, index_col=0)
df_adj.fillna(0, inplace = True)
df_adj.index = df_adj.index.astype("str")
# Network Creation
G = nx.from_pandas_adjacency(df_adj, create_using = nx.Graph)

# List with path-related content
folder_list = [("undirected", "/"), ("directed", "/strongly/"),
              ("directed", "/weakly/")]
method = ["Cascade", "Block_2", "Block_5"]

# Constants
N = len(G.nodes())

# Process for threshold and robustness calculation for every method 
for i0 in folder_list:
    for i1 in method:
        path = "Final_Results/Full_Network/" + i0[0] +\
            "/Node_removal" + i0[1]
        file_n = "Final_" + i1 + ".xlsx"
        # Creating DataFrames
        df_eff = pd.read_excel(path + file_n, sheet_name = "Efficiency")
        df_lcc = pd.read_excel(path + file_n, sheet_name = "LCC")
        df_ncc = pd.read_excel(path + file_n, sheet_name = "Components #")
        
        # Threshold calculation
        ncc_max = dict()
        for i2 in df_ncc.columns[2:]:
            max_val = max(df_ncc[i2].values)
            nodes_removed = int(df_ncc[df_ncc[i2] ==\
                                       max_val]["Iteration"].values[0])
            threshold = int(df_ncc[df_ncc[i2] ==\
                                   max_val]["Unnamed: 0"].values[0])
            ncc_max.update({
                i2: (nodes_removed, max_val, threshold)
            })
        thresholds, eff_at_max = [], [] # Storing thresholds and efficiencies
        robustness = [] # Storing robustness
        nodes_rem = []
        for i3 in ncc_max:
            t = ncc_max[i3][2]
            eff = float(df_eff[df_eff["Iteration"] ==\
                               ncc_max[i3][0]][i3].values[0])
            thresholds.append(t)
            eff_at_max.append(eff)
            robustness.append(robust(N, t, df_lcc[i3].values, 
                                     df_lcc["Iteration"].values,\
                                         ncc_max[i3][0]))
            nodes_rem.append(ncc_max[i3][0])
        
        # Save results
        results = pd.DataFrame({
            "Centrality": list(df_ncc.columns[2:]),
            "Robustness": robustness,
            "Efficiency": eff_at_max,
            "Nodes Removed": nodes_rem,
            "Threshold": thresholds
        })
        
        file_name = "Robust_" + i1
        results.to_csv(path + file_name + ".csv", index=False)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 02:01:29 2024

@author: kostasan00
"""

import networkx as nx
import pandas as pd
import numpy as np
import net_creation as nc


def harmonic_mean(graph, weight):
    ''' Calculates the harmonic
    mean of the edges of a network.
    
    INPUT
    -----
    g: networkx Graph object
    weight: str or None
    
    OUTPUT
    ------
    float (calculated harmonic mean)
    
    '''
    M = len(graph.edges)
    if weight == None:
        return float(1)
    else:
        if len(graph.edges) == 0:
            return float(0)
        # Calculate the denominator
        sum_values = [1 / graph.edges()[key][weight] for key in graph.edges]
        
        return M / sum(sum_values)

def global_eff(graph, weight, direction):
    n = len(graph.nodes)
    out_local_eff = dict()
    in_local_eff = dict()
    lengths = []
    gl_eff = 0
    
    if direction == "in":
        # Incoming distances calculation
        for node in graph.nodes:
            for other in graph.nodes:
                try:
                    lengths.append(nx.shortest_path_length(graph, 
                                                           source = other, 
                                                           target = node, 
                                                           weight = weight))
                    
                except nx.NetworkXNoPath:
                    pass
                
            distances = [1 / x for x in lengths if x != 0]
            in_local_eff.update({node: (harmonic_mean(graph, 
                                                       weight) *\
                                         sum(distances)) / (n - 1)})
            lengths = []
            
        # Global efficiency
        for i in in_local_eff.values():
            gl_eff += i
                  
    elif direction == "out":
        # Outcoming distances calculation
        for node in graph.nodes:
            for other in graph.nodes:
                try:
                    lengths.append(nx.shortest_path_length(graph, 
                                                           source = node, 
                                                           target = other, 
                                                           weight = weight))
                    
                except nx.NetworkXNoPath:
                    pass
                
            distances = [1 / x for x in lengths if x != 0]
            out_local_eff.update({node: (harmonic_mean(graph,
                                                      weight) *\
                                        sum(distances)) / (n - 1)})
            
            lengths = []
        
        # Global efficiency
        for i in out_local_eff.values():
            gl_eff += i
            
    return gl_eff / n

import pandas as pd
import numpy as np
import networkx as nx

def centralizations(df: pd.DataFrame, method: str, n: int):
    '''
    Function that calculates centralizations
    
    INPUT
    df: Pandas DataFrame, dataframe with calculated centralities
    method: str, preferred centrality value
    n: int, number of nodes
    
    OUTPUT
    
    centralization value: float
    '''
    # Max centrality value
    max_centr = df[method].max()
    
    # Numerator
    differences = [max_centr - i for i in df[method].values]
    numerator = sum(differences)
    
    # Denominator (changes according to selected centrality)
    if method in {"In-Degree", "Out-Degree", "Degree", "In-Strength", "Out-Strength", "Strength"}:
        denominator = n - 2
    elif method in {"Betweenness", "Clustering"}:
        denominator = n - 1
    elif method in {"In-Close", "Out-Close", "Closeness", "In-Harmonic", "Out-Harmonic", "Harmonic"}:
        denominator = ((n - 1) * (n - 2)) / (2 * n - 3)
    
    return numerator / denominator

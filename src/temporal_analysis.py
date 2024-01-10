# Libraries
import pandas as pd
import sys
import numpy as np
import networkx as nx
import glob

import matplotlib.pyplot as plt
import seaborn as sb
import scipy.stats as stat 
from natsort import natsorted

# Custom functions
sys.path.append('/home/kostasan00/Desktop/criminal_nets/src/modules/')

from modules.net_creation import net_creation
from modules.efficiency import global_eff
from modules.efficiency import harmonic_mean
from modules.centralizations import centralizations
from modules.centralities import centralities
from modules.glob_eff import eff_un


def graph_entropy(df, method:str, n: int):
    '''
    Network entropy
    '''
    return stat.entropy(df[method].values, base = 2) / np.log2(n-1)
    
#################################  S C R I P T ##########################
'''This scipt loads temporal data and calculates
   the change of some network topology metrics 
   and centralities with time. Results are saved
   as CSV files
'''

direction = sys.argv[1]
dir_path = "/home/kostasan00/Desktop/criminal_nets/"
i = 1 # Iterator

if direction == "undirected":
    # List of centralities
    centralities_list = ["Degree", "Betweenness"]
    # Metrics
    metrics = {"Degree Centralization": [], "Betweenness Centralization": [],\
               "Global Efficiency": [], "Degree Entropy": []}
    
else:
    # List of centralities
    centralities_list = ["In-Degree", "Out-Degree", "Betweenness"]
    # Metrics
    metrics = {"In-Degree Centralization": [],\
               "Out-Degree Centralization": [],\
                   "Betweenness Centralization": [],\
                   "In-Global Efficiency": [],\
                   "Out-Global Efficiency": [],\
                   "In-Degree Entropy": [],\
                       "Out-Degree Entropy": []}
          
# Additional metrics
metrics.update({"Average Clustering": []})

# Number of nodes
nodes = []    
# Import data
for file_name in natsorted(glob.glob(dir_path + "data/TempData/" +\
                                     'CAVIAR*.csv')):
    df = pd.read_csv(file_name, header=0, index_col="Unnamed: 0")
    df.fillna(0, inplace=True)
    df.index = df.index.astype("str")
    
    if direction == "undirected":
        # Creating a symmetric dataframe
        for i0 in range(0, len(df.columns)):
            for i1 in range(i0 + 1, len(df.columns)):
                df.iat[i0, i1] = df.iat[i0, i1] + df.iat[i1, i0]
                df.iat[i1, i0] = df.iat[i0, i1]
        
        # Network construction
        G = net_creation(df, nx.Graph)
    else:
        # Network construction
        G = net_creation(df, nx.DiGraph)
        G_rev = nx.reverse(G, copy = True)
 
    # Number of nodes
    N = len(G.nodes())
    nodes.append(N)
    
    # Compute centralities
    centralities_df = centralities(G, df)
    centralities_df.to_csv("results/temporal/Phase-{}.csv".format(i), 
                           index=False)
    
    # Compute global metrics
    for iter1, iter2 in zip(centralities_list, metrics):
        metrics[iter2].append(centralizations(centralities_df, iter1, 
                                                     N))
    
    metrics["Average Clustering"].append(nx.average_clustering(G,\
                                                               weight="weight"))
    if direction == "undirected":
        metrics["Global Efficiency"].append(eff_un(G, "distance"))
        metrics["Degree Entropy"].append(graph_entropy(centralities_df,\
                                                           "Degree", N))
    elif direction == "directed":
        metrics["In-Global Efficiency"].append(global_eff(G, "distance",\
                                                              "in"))
        metrics["Out-Global Efficiency"].append(global_eff(G, "distance",\
                                                                   "out"))
        metrics["In-Degree Entropy"].append(graph_entropy(centralities_df,\
                                                      "In-Degree", N))
        metrics["Out-Degree Entropy"].append(graph_entropy(centralities_df,\
                                                       "Out-Degree", N))
      
    i += 1
    
# Storing Data Frame    
metrics_df = pd.DataFrame(metrics, index=[_ for _ in range(1, 12)])
metrics_df.to_csv("results/temporal/Metrics_Temp.csv", index=False)

# Plotting network growth
sb.set(style="whitegrid")
plt.figure(figsize = (12, 6))

sb.lineplot(x = [_ for _ in range(2, 24, 2)], y = nodes)
plt.xlabel("Stage of investigation (Months)",\
           fontdict = {"fontweight": "bold"})
plt.ylabel("Number of nodes")
plt.title("Network growth in time", fontdict = {"fontsize": 14,
                                                  "fontweight": "bold",
                                                  "fontstyle": "italic"})
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Storing plot as a jpg image
plt.tight_layout()
plt.savefig("results/temporal/NetworkGrowth.png", dpi=300)

# Plotting global indicators
sb.set(style="whitegrid")
n_col = len(metrics_df.columns)
plt.figure(figsize = (12, 6))
for col in metrics_df.columns:
    xvals = [_ for _ in range(2, 24, 2)]
    yvals = metrics_df[col]
    #Plot
    sb.lineplot(x = xvals, y = yvals, label = col)

plt.xlabel("Stage of investigation (Months)",\
           fontdict = {"fontweight": "bold"})
plt.ylabel("Values")
plt.title("Time Series Data", fontdict = {"fontsize": 14, 
                                            "fontweight": "bold", 
                                            "fontstyle": "italic"})
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))


plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=4)


# Storing plot as a jpg image
plt.tight_layout()
plt.savefig("results/temporal/TimeSeries_Metrics.png", dpi=300)

import networkx as nx 

def harmonic_mean(G, weight):
	''' Calculates the harmonic mean of
	the edges of a network.
	
	Input
	-----
	G: networkx Graph
	weight: str or None 
	
	Returns
	-------
	harmonic_mean: float
	
	'''
	m = len(G.edges())
	if weight == None:
		return float(1)
	else:
		if len(G.edges()) == 0:
			return float(0)
		denom = 0
		for key in G.edges():
			inverse = 1 / G.edges()[key][weight]
			denom += inverse
			
		return m / denom
		
		

def eff_un(G, weight):
	''' Calculates the global efficiency
	of a network
	
	Input
	-----
	G: networkx Graph
	weight: str or None
	
	Output
	------
	global_efficiency: float
	
	Notes
	-----
	The function covers nearly all cases of networks; undirected,
	directed, unweighted and weighted(with positive weights). The 
	normalizing factor in the weighted version of the networks has been 
	refined by using the harmonic mean of the edges, since a weighted 
	network with small distances can outperform the corresponding
	fully connected network.
	
	
	References
	----------
	.. [1] Latora, V., and Marchiori, M. (2001). Efficient behavior of small-world networks.
	       Physical Review Letters 87.
	.. [2] Gutfraind A (2010). Optimizing Topological Cascade Resilience Based on the 
	       Structure of Terrorist Networks. PLoS ONE 5(11): e13448. 
	       https://doi.org/10.1371/journal.pone.0013448
 	   [3] Eisenman, L. Functions to compute global and local efficiency as defined
	       by Latora and Marchiori
	'''
	n = len(G.nodes())
	inv_distances = []
	for node in G:
		if weight == None:
			distances = nx.single_source_shortest_path_length(G, node)
		else:
			distances = nx.single_source_dijkstra_path_length(G, node, weight = weight)
			
		inverses = [1 / x for x in distances.values() if x != 0]
		inv_distances.extend(inverses)
	
	normal_coeff = harmonic_mean(G, weight) / (n * (n - 1))
	
	return normal_coeff * sum(inv_distances)			

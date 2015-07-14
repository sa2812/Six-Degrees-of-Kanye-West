import networkx as nx
import sys


G = nx.read_gpickle('graph.pkl')

temp = nx.shortest_path(G, "Kanye West", "JAY Z")

print temp

edges = []
ii = 0
while ii < len(temp)-1:
    edges.append((temp[ii], temp[ii+1]))
    ii += 1
for jj in edges:
    print G.get_edge_data(*jj)
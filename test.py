import networkx as nx
from networkx.readwrite import json_graph
import json

G = nx.MultiGraph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4)])

data = json_graph.node_link_data(G)

s = json.dumps(data)

print nx.shortest_path(G, 1, 3)
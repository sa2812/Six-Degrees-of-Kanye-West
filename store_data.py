from db_conn import *
from itertools import permutations
import networkx as nx
import spotify
import matplotlib.pyplot as plt
import random


def featured_info(artist, graph, g):
    """Adds featured artists and their songs to the database."""
    graph.add_node(artist.name)
    for ii in artist.song_features:
        artist_ids  = []
        artist_list = []
        for jj in ii['artists']:
            artist_ids.append(jj['id'])
            artist_list.append(jj['name'])
            graph.add_node(jj['name'])
            g.add_node(jj['name'])
        perms = permutations(artist_list, 2)
        for pair in perms:
            graph.add_edge(*pair, song_name=ii['name'], song_id=ii['id'])
            g.add_edge(*pair, song_name=ii['name'], song_id=ii['id'])
        artist_ids  = ",".join(artist_ids)
        artist_list = ",".join(artist_list)

try:
    G = nx.read_gpickle("graph.pkl")
    g = nx.read_gpickle("graph1.pkl")
except IOError:
    G = nx.MultiDiGraph()
    g = nx.Graph()
artist = spotify.TrackCollector(name="Jay Z")
featured_info(artist, G, g)
nx.write_gpickle(G, "graph.pkl")
nx.write_gpickle(G, "graph1.pkl")

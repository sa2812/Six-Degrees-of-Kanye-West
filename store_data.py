import networkx as nx
from networkx.readwrite import json_graph
import json
import spotify
import matplotlib.pyplot as plt
import gc

from db_conn import *
from itertools import permutations


def populate_graph(artist, mgraph):
    """Adds featured artists and their songs to the database."""
    mgraph.add_node(artist.artist_uri)
    for ii in artist.song_features:
        artist_list = []
        for jj in ii['artists']:
            artist_list.append(jj['uri'])
            mgraph.add_node(jj['uri'])
        perms = permutations(artist_list, 2)
        for pair in perms:
            mgraph.add_edge(*pair, song_id=ii['id'])

    return mgraph

@db_wrapper
def get_artist_info(c):
    c.execute("SELECT artist_list.'artist', artist_list.'uri' FROM artist_list WHERE artist_list.'done' IS NULL")
    return c.fetchall()

@db_wrapper
def mark_as_done(c, artist):
    c.execute("UPDATE artist_list SET done=1 WHERE uri='{}'".format(artist))
    return

artist_list = get_artist_info()
remaining = len(artist_list)
print "Artists remaining: {}".format(remaining)

try:
    multi_graph = nx.read_gpickle("multi.pkl")
except IOError:
    multi_graph = nx.MultiGraph()
    nx.write_gpickle(multi_graph, "multi.pkl")

count = 0
for ii in artist_list:
    try:
        try:
            artist = spotify.TrackCollector(name=ii[0])
        except IndexError:
            continue
    except MemoryError:
        continue
    mgraph = populate_graph(artist, multi_graph)
    json_data = json_graph.node_link_data(mgraph)
    with open('multi.json', 'wb') as jsonfile:
        json.dump(json_data, jsonfile)
    nx.write_gpickle(mgraph, "multi.pkl")
    mark_as_done(ii[1])
    count += 1
    print "Artists remaining: {}".format(remaining - count)

    gc.collect()

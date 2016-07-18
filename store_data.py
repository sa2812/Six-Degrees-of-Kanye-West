import networkx as nx
import spotify 
import pickle
import sys
import gc

from db_conn import *
from itertools import permutations


def populate_graph(artist, mgraph):
    """Adds featured artists and their songs to the database."""
    mgraph.add_node(artist.artist_uri)
    for ii in artist.song_features:
        artist_list = []
        for jj in ii['artists']:
            artist_list.append(jj['name'])
            mgraph.add_node(jj['name'])
        perms = permutations(artist_list, 2)
        for pair in perms:
            mgraph.add_edge(*pair, song_id=ii['name'])

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
    try:
        with open('multi.pkl', 'rb') as f:
            multi_graph = pickle.load(f)
    except KeyError:
        print "This is broken, investigate further"
        sys.exit("There is an error")
except IOError:
    multi_graph = nx.MultiGraph()
    with open('multi.pkl', 'wb') as f:
        pickle.dump(multi_graph, f)

count = 0
for ii in artist_list:
    try:
        try:
            artist = spotify.TrackCollector(name=ii[0])
        except (IndexError, ValueError) as e:
            continue
    except MemoryError:
        continue
    mgraph = populate_graph(artist, multi_graph)
    try:
        with open('multi.pkl', 'wb') as f:
            pickle.dump(mgraph, f)
    except KeyError:
        continue
    mark_as_done(ii[1])
    count += 1
    print "Artists remaining: {}".format(remaining - count)

    gc.collect()

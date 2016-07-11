from itertools import permutations
import matplotlib.pyplot as plt
import networkx as nx
from db_conn import *
import spotify
import json
import gc


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
    c.execute("""SELECT artist_list.'artist', artist_list.'uri'
                 FROM artist_list
                 WHERE artist_list.'done' IS NULL""")
    return c.fetchall()


@db_wrapper
def mark_as_done(c, uri):
    c.execute("UPDATE artist_list SET done=1 WHERE uri='{}'".format(uri))
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
for artist, uri in artist_list:
    try:
        try:
            spotify_artist = spotify.ArtistInfo(name=artist)
            multi_graph    = populate_graph(spotify_artist, multi_graph)
            nx.write_gpickle(multi_graph, "multi.pkl")
            mark_as_done(uri)
        except IndexError:
            continue
    except MemoryError:
        continue
    print "Artists remaining: {}".format(remaining - count)
    count += 1

    # gc.collect()

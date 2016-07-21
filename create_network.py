import networkx as nx
import spotify 
import pickle
import gc

from db_conn import *
from itertools import combinations


def populate_graph(artist, graph):
    """
    Adds featured artists and their songs to the NetworkX graph.
    """
    graph.add_node(artist.artist_uri)
    for song in artist.song_features:
        artist_list = []
        for ft_artist in song['artists']:
            artist_list.append(ft_artist['uri'])
            graph.add_node(ft_artist['uri'], name=ft_artist['name'])
        combs = combinations(artist_list, 2)
        for pair in combs:
            graph.add_edge(*pair, id=song['id'], track=song['name'])

    return graph

@db_wrapper
def get_artist_info(c):
    c.execute("""SELECT artist_list.'artist', artist_list.'uri'
                 FROM artist_list
                 WHERE artist_list.'done' IS NULL""")
    return c.fetchone()

@db_wrapper
def mark_as_done(c, artist):
    c.execute("""UPDATE artist_list
                 SET done=1
                 WHERE uri='{}'""".format(artist))
    return

while count < 10:
    artist_list = get_artist_info()
    try:
        with open('multi.pkl', 'rb') as f:
            graph = pickle.load(f)
    except IOError:
        graph = nx.MultiGraph()
        with open('multi.pkl', 'wb') as f:
            pickle.dump(multi_graph, f)

    for ii in artist_list:
        artist = spotify.TrackCollector(name=ii[0])
        graph = populate_graph(artist, graph)
        with open('multi.pkl', 'wb') as f:
            pickle.dump(graph, f)
        mark_as_done(ii[1])
        count += 1
        print "Artists completed: {}".format(count)
        print "Last artist completed: {}".format(ii[0])

        gc.collect()

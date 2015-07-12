from db_conn import *
from itertools import permutations
import networkx as nx
import spotify
import matplotlib.pyplot as plt
import random


@db_wrapper
def featured_info(c, artist, graph):
    """Adds featured artists and their songs to the database."""
    # try:
    #     c.execute("""CREATE TABLE ft_songs (song_name text, 
    #                                         song_id text, 
    #                                         song_artists text, 
    #                                         song_artists_ids text)""")
    #     c.execute("""CREATE TABLE ft_artists (artist text,
    #                                           artist_uri text, 
    #                                           featured_names text,
    #                                           featured_uri text)""")
    # except sqlite3.OperationalError:
    #     pass

    graph.add_node(artist.name)

    # c.execute("SELECT artist FROM ft_artists WHERE artist=\'"+artist.name+"\'")
    # result = c.fetchall()
    # if len(result) != 0:
    #     return

    for ii in artist.song_features:
        artist_ids  = []
        artist_list = []
        for jj in ii['artists']:
            artist_ids.append(jj['id'])
            artist_list.append(jj['name'])
            graph.add_node(jj['name'])
        perms = permutations(artist_list, 2)
        for pair in perms:
            graph.add_edge(*pair, song_name=ii['name'], song_id=ii['id'])
        artist_ids  = ",".join(artist_ids)
        artist_list = ",".join(artist_list)
        # c.execute("""INSERT INTO ft_songs (song_name, 
        #                                    song_id, 
        #                                    song_artists, 
        #                                    song_artists_ids)
        #              VALUES (?, ?, ?, ?)""",
        #           (ii['name'], ii['id'], artist_list, artist_ids))


    ft_uris  = ",".join(artist.ft_uris)
    ft_names = ",".join(artist.ft_names)
    # c.execute("""INSERT INTO ft_artists (artist,
    #                                      artist_uri,
    #                                      featured_names,
    #                                      featured_uri)
    #              VALUES (?, ?, ?, ?)""",
    #           (artist.name, artist.artist_uri, ft_names, ft_uris))


try:
    G = nx.read_gpickle("graph.pkl")
except IOError:
    G = nx.Graph()
artist = spotify.TrackCollector(name="Vic Mensa")
featured_info(artist, G)
nx.write_gpickle(G, "graph.pkl")
list_artists = G.nodes()
num_songs   = len(G.edges())
a = random.choice(list_artists)
b = random.choice(list_artists)
print a
print b
try:
    temp = nx.shortest_path(G, source=a, target=b)
    edges = []
    ii = 0
    while ii < len(temp)-1:
        edges.append((temp[ii], temp[ii+1]))
        ii += 1
    for jj in edges:
        print G.get_edge_data(*jj)
    try:
        print "The shortest path is %d and is: %s" % (len(temp), ", ".join(temp).encode('utf-8'))
    except UnicodeEncodeError:
        print "The shortest path is %d \#encodeerror" % len(temp)
except nx.exception.NetworkXNoPath:
    print "No path between %s and %s" % (a, b)


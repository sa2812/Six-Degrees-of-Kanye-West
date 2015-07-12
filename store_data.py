from db_conn import *
from itertools import permutations
import networkx as nx
import spotify
import matplotlib.pyplot as plt


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


G = nx.read_gpickle("graph.pkl")
artist = spotify.TrackCollector(name="Paul McArtney")
featured_info(artist, G)
nx.spring_layout(G)
nx.draw_networkx(G, node_size=10, node_color='b', node_shape='x', width=0.2, with_labels=True)
plt.show()
nx.write_gpickle(G, "graph.pkl")
# print G.nodes()


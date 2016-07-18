import networkx as nx
import pickle
import spotipy
import random

f = open('multi-old.pkl', 'rb')
g = pickle.load(f)

sp = spotipy.Spotify()

kanye_uri = "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x"
targeturi = "spotify:artist:3nFkdlSjzX9mRTtwJOzDYB"

# shortest_path = nx.shortest_path(g, source=kanye_uri, target=targeturi)

group_size = 2
overlap    = 1
# pairs = [shortest_path[i:i+group_size-overlap+1] for i in xrange(len(shortest_path)-1)]

# print [sp.artist(ii)['name'] for ii in shortest_path]

# print [sp.track(g.get_edge_data(*e)[random.choice(g.get_edge_data(*e).keys())]['song_id'])['name'] for e in pairs]

# a = pairs[0]
# b = g.get_edge_data(*a)
# key = random.choice(b.keys())
# print sp.track(b[key]['song_id'])['name']
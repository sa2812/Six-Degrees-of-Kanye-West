import networkx as nx
import pickle
import spotipy

f = open('multi.pkl', 'rb')
g = pickle.load(f)

sp = spotipy.Spotify()

kanye_uri = "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x"

for ii in nx.all_neighbors(g, kanye_uri):
	print sp.artist(ii)['name']

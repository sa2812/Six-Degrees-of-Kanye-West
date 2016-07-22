import spotipy
import sys
import time


sp = spotipy.Spotify()


class TrackCollector:
	"""
	Collects all the albums, songs and featured artists for an artist.
	"""
	def __init__(self, name=None, uri=None):
		if name:
			self.name = sp.search(q='artist:' + name,
								  type='artist')['artists']['items'][0]['name']
			self.artist_uri = sp.search(q='artist:' + name,
										type='artist')['artists']['items'][0]['uri']
		else:
			raise TypeError

		self.albums = self.get_all_albums()
		self.song_features = self.get_all_features()

	def get_all_albums(self):
		"""
		Gets all of the artist's releases on Spotify.
		"""
		results = sp.artist_albums(self.artist_uri)
		albums = {}
		for album in results['items']:
			albums[album['id']] = 1
		while results['next']:
			results = sp.next(results)
			for album in results['items']:
				albums[album['id']] = 1

		return albums.keys()

	def get_all_features(self):
		"""
		Gets all the songs which have featured artists on them.
		"""
		tracks = {}
		for album in self.albums():
			results = album['tracks']['items']
			for track in results:
				if len(track['artists']) > 1:
					current_track = {}
					for artist in track['artists']:
						current_track[artist['uri']] = 1
					try:
						current_track[self.artist_uri]
						tracks[track['id']] = 1
					except KeyError:
						pass

		return tracks.keys()

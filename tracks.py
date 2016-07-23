import spotipy
import sys
import time


sp = spotipy.Spotify()


class TrackCollector:
	"""
	Collects all the albums, songs and featured artists for an artist.
	"""
	def __init__(self, uri=None):
		artist = sp.artist(uri)
		self.name = artist['name']
		self.artist_uri = uri

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
		for a in self.albums:
			try:
				album = sp.album(a)
			except ValueError:
				continue
			results = album['tracks']
			for track in results['items']:
				if len(track['artists']) > 1:
					current_track = {}
					for artist in track['artists']:
						current_track[artist['uri']] = 1
					try:
						current_track[self.artist_uri]
						tracks[track['id']] = 1
					except KeyError:
						pass
			while results['next']:
				results = sp.next(results)
				for track in results['items']:
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

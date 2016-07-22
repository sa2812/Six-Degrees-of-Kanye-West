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

		self.albums = []
		self.all_songs     = self.get_all_album_tracks()
		self.song_features = self.get_song_features()

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
				
		self.albums = albums.keys()

	def get_all_album_tracks(self):
		"""
		Gets all the songs in each album.
		"""
		all_songs = []
		ft_artists = {}
		for album in self.albums:
			all_tracks = album['tracks']
			tracks = {}
			for track in all_tracks:
				if self.name in track['artists']:
					

		for ii in self.albums:
			results = sp.album_tracks(ii['uri'])
			album_songs = results['items']
			while results['next']:
				album_songs.extend(results['items'])
			ii['tracklist'] = album_songs
			all_songs.extend(album_songs)

		return all_songs

	def get_song_features(self):
		"""
		Gets all the songs which have featured artists on them.
		"""
		song_features = []
		for ii in self.all_songs:
			if len(ii['artists']) > 1:
				song_features.append(ii)

		return song_features

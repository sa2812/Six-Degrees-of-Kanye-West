import spotipy
import sys
import time


sp = spotipy.Spotify()


class TrackCollector:
	"""
	Collects all the albums, songs and featured artists for an artist.
	"""
	def __init__(self, name=None, identity=None, uri=None):
		if uri:
			self.name = sp.search(q='uri:' + uri,
				                  type='artist')['artists']['items'][0]['name']
			self.artist_uri = uri
		elif name:
			self.name = sp.search(q='artist:' + name,
				                  type='artist')['artists']['items'][0]['name']
			self.artist_uri = sp.search(q='artist:' + name,
			                            type='artist')['artists']['items'][0]['uri']
		elif identity:
			self.name = sp.search(q='id:' + identity,
				                  type='artist')['artists']['items'][0]['name']
			self.artist_uri = sp.search(q='id:' + identity,
				                        type='artist')['artists']['items'][0]['uri']
		else:
			raise TypeError
		self.albums        = self.get_all_albums()
		self.all_songs     = self.get_all_album_tracks()
		self.song_features = self.get_song_features()
		# self.ft_artists, self.ft_names, self.ft_uris = self.get_all_featured_artists()

	def get_all_albums(self):
		"""Gets all of the artist's releases on Spotify."""
		results = sp.artist_albums(self.artist_uri,
			                       album_type='album')
		albums = results['items']
		while results['next']:
			results = sp.next(results)
			albums.extend(results['items'])

		album_names = []
		non_dupl_albums = []
		for ii in albums:
			if ii['name'] not in album_names:
				album_names.append(ii['name'])
				non_dupl_albums.append(ii)
				
		return non_dupl_albums

	def get_all_album_tracks(self):
		"""Gets all the songs in each album."""
		all_songs = []
		for ii in self.albums:
			results = sp.album_tracks(ii['uri'])
			album_songs = results['items']
			while results['next']:
				album_songs.extend(results['items'])
			ii['tracklist'] = album_songs
			all_songs.extend(album_songs)

		return all_songs

	def get_song_features(self):
		"""Gets all the songs which have featured artists on them."""
		song_features = []
		for ii in self.all_songs:
			if len(ii['artists']) > 1:
				song_features.append(ii)

		return song_features

	# def get_all_featured_artists(self):
	# 	"""Gets all the artists who have featured on album songs."""
	# 	featured_artists_names = []
	# 	featured_artists_uris  = []
	# 	featured_artists       = []
	# 	for ii in self.all_songs:
	# 		if len(ii['artists']) > 1:
	# 			for jj in ii['artists']:
	# 				if jj['name'] != self.name:
	# 					if jj['name'] not in featured_artists_names:
	# 						featured_artists_names.append(jj['name'])
	# 						featured_artists_uris.append(jj['uri'])
	# 						featured_artists.append(jj)

	# 	return featured_artists, featured_artists_names, featured_artists_uris
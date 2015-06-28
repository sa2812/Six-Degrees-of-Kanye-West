import sys
import config
import spotipy
import spotipy.util as util

scope = 'user-library-read'

SPOTIPY_CLIENT_ID = config.spotify_id
SPOTIPY_CLIENT_SECRET = config.spotify_secret
SPOTIPY_REDIRECT_URI='https://github.com/sa2812/Six-Degrees-of-Kanye-West'

username = "amrat.sunny"

token = util.prompt_for_user_token(username,
	                               scope,
	                               client_id = SPOTIPY_CLIENT_ID,
	                               client_secret = SPOTIPY_CLIENT_SECRET,
	                               redirect_uri = SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

class TrackCollector:
	def __init__(self, name):
		self.name = name
		self.artist_uri = sp.search(q='artist:' + name, type='artist')['artists']['items'][0]['uri']
		self.albums = self.get_albums()

	def get_albums(self):
		results = sp.artist_albums(self.artist_uri, album_type='album')
		albums = results['items']
		while results['next']:
			results = sp.next(results)
			albums.extend(results['items'])

		return albums

a = TrackCollector("Kanye West")
print a.albums
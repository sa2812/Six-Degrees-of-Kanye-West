import spotipy

sp = spotipy.Spotify()

kanye_uri = "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x"
targeturi = "spotify:artist:3nFkdlSjzX9mRTtwJOzDYB"

results = sp.artist_albums(kanye_uri)

artists = []
count = 0
while results['next']:
	for ii in results['items']:
		a = sp.album(ii['id'])
		b = a['tracks']['items']
		for jj in b:
			print jj['name']

		print ""

	break
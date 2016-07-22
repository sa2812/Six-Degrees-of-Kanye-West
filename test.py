import spotipy
import tracks
import pprint

sp = spotipy.Spotify()

# targeturi = "spotify:artist:3nFkdlSjzX9mRTtwJOzDYB"

# results = sp.artist_albums(kanye_uri)

# print results

kw = tracks.TrackCollector(name="Kanye West")

album = sp.album(kw.albums[0])

pprint.pprint(album['tracks'])
from db_conn import *
import spotipy

sp = spotipy.Spotify()

@db_wrapper
def get_track(c):
	c.execute("""SELECT kanye_degree.'track'
				 FROM kanye_degree
				 WHERE kanye_degree.'track_done'=0
				 ORDER BY kanye_degree.'gen' ASC""")
	return c.fetchone()

@db_wrapper
def get_artist_not_done(c):
	c.execute("""SELECT kanye_degree.'id'
				 FROM kanye_degree
				 WHERE kanye_degree.'popularity'=NULL
				 ORDER BY kanye_degree.'gen' ASC""")
	return c.fetchone()

@db_wrapper
def set_track_name(c, track_name, track):
	c.execute("""UPDATE kanye_degree
				 SET track_name=?, track_done=1
				 WHERE track=?""", (track_name, track))

@db_wrapper
def set_popularity(c, popularity, _id):
	c.execute("""UPDATE kanye_degree
				 SET popularity=?
				 WHERE id=?""", (popularity, _id))

while True:
	artist_id, = get_artist_not_done()
	popularity = sp.artist(artist_id)['popularity']
	print artist_id
	set_popularity(popularity, artist_id)

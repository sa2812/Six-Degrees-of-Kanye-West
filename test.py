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
def set_track_name(c, track_name, track):
	c.execute("""UPDATE kanye_degree
				 SET track_name=?, track_done=1
				 WHERE track=?""", (track_name, track))

while True:
	track, = get_track()
	track_name = sp.track(track)['name']
	print track_name
	set_track_name(track_name, track)

from db_conn import *
import spotipy

sp = spotipy.Spotify()

@db_wrapper
def get_track(c, track):
	c.execute("""SELECT kanye_degree.'track_name'
				 FROM kanye_degree
				 WHERE kanye_degree.'track'=?""", [track])
	return c.fetchone()

def track_handler(track):
	name = get_track(track)[0]
	if name:
		return name
	else:
		return sp.track(track)['name']

# @db_wrapper
# def set_track_name(c, track_name, track):
# 	c.execute("""UPDATE kanye_degree
# 				 SET track_name=?, track_done=1
# 				 WHERE track=?""", (track_name, track))

# while True:
# 	track, = get_track()
# 	track_name = sp.track(track)['name']
# 	print track_name.encode('utf-8')
# 	set_track_name(track_name, track)

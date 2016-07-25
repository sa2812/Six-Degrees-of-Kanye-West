from db_conn import *
import spotipy

sp = spotipy.Spotify()

kanye_id     = "5K4W6rqBFWDnAN6FQUkS6x"
sean_paul_id = "3Isy6kedDrgPYoTS1dazA9"

@db_wrapper
def get_connection(c, _id):
	c.execute("""SELECT ancestor, track
				 FROM kanye_degree
				 WHERE id=?""", [_id])
	return c.fetchone()

@db_wrapper
def get_name_from_id(c, _id):
	c.execute("""SELECT name
				 FROM kanye_degree
				 WHERE id=?""", [_id])
	return c.fetchone()

def get_path(_id, path=None, tracks=[]):
	if not path:
		path = [_id]
	ancestor, track = get_connection(_id)
	ancestor_id = ancestor[15:]
	path.append(ancestor_id)
	tracks.append(track)
	while ancestor_id != kanye_id:
		return get_path(ancestor_id, path, tracks)
	return path, tracks

path, tracks = get_path(sean_paul_id)

print path
print [get_name_from_id(i)[0] for i in path]
print tracks
print [sp.track(i)['name'] for i in tracks]

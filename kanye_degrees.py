from tracks import *
from db_conn import *
import gc


@db_wrapper
def create_table(c):
	try:
		c.execute("""CREATE TABLE kanye_degree (name text PRIMARY KEY,
												id text ,
												uri text,
												gen integer,
												ancestor text,
												track text,
												done integer,
												track_done integer,
												track_name text,
												popularity integer)""")
		kanye_uri = "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x"
		seed_artist = sp.artist(kanye_uri)
		c.execute("""INSERT INTO kanye_degree
					 VALUES (?, ?, ?, ?, NULL, NULL, ?, ?, NULL, ?)""",
				  (seed_artist['name'], seed_artist['id'], seed_artist['uri'], 0, 0, 1, seed_artist['popularity']))
	except:
		pass

@db_wrapper
def get_artist_not_done(c):
	c.execute("""SELECT kanye_degree.'name', kanye_degree.'uri', kanye_degree.'gen'
				 FROM kanye_degree
				 WHERE kanye_degree.'done'=0
				 ORDER BY kanye_degree.'gen' ASC, kanye_degree.'popularity' DESC""")
	return c.fetchone()

@db_wrapper
def update_table_new_artist(c, name, _id, uri, gen, ancestor, track, track_name):
	try:
		c.execute("""INSERT INTO kanye_degree
					 VALUES (?, ?, ?, ?, ?, ?, 0, 1, ?, NULL)""",
				  (name, _id, uri, gen, ancestor, track, track_name))
	except sqlite3.IntegrityError:
		pass

@db_wrapper
def update_popularity(c, uri, popularity):
	c.execute("""UPDATE kanye_degree
				 SET popularity=?
				 WHERE uri=?""", (popularity, uri))

@db_wrapper
def mark_as_done(c, uri):
	c.execute("""UPDATE kanye_degree
				 SET done=1
				 WHERE uri='{}'""".format(uri))

@db_wrapper
def mark_as_error(c, uri):
	c.execute("""UPDATE kanye_degree
				 SET done=2
				 WHERE uri='{}'""".format(uri))

create_table()

gen = 0
while gen < 4:
	current_name, current_uri, current_gen = get_artist_not_done()
	gen = current_gen + 1
	try:
		print current_uri
		current = TrackCollector(uri=current_uri)
		song_features = current.song_features
		update_popularity(current_uri, current.popularity)
		for s in song_features:
			try:
				song = sp.track(s)
			except ValueError:
				continue
			for artist in song['artists']:
				if artist['uri'] != current_uri:
					update_table_new_artist(artist['name'],
											artist['id'],
											artist['uri'],
											gen,
											current_uri,
											song['id'],
											song['name'])
					print artist['name'].encode('utf-8')
		mark_as_done(current_uri)
		print "\nMarked as done\n"
	except (IndexError, TypeError) as e:
		print "{} could not be added".format(current_name)
		mark_as_error(current_uri)

# 161 in gen=1	

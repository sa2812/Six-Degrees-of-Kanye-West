from db_conn import *
import spotify


artist   = spotify.TrackCollector(name="Kanye West")
featured = artist.ft_artists


@db_wrapper
def store_data_fn(c):
	try:
		c.execute("""CREATE TABLE albums (song_name text, 
			                              song_id text, 
			                              song_artists text, 
			                              song_artists_ids text)""")
	except:
		pass

	for ii in featured:
		artist_ids  = []
		artist_list = []
		for jj in ii['artists']:
			artist_ids.append(jj['id'])
			artist_list.append(jj['name'])
		artist_ids  = ", ".join(artist_ids)
		artist_list = ", ".join(artist_list)
		c.execute("""INSERT INTO albums (song_name, 
			                             song_id, 
			                             song_artists, 
			                             song_artists_ids) VALUES (?, ?, ?, ?)""",
		          (ii['name'], ii['id'], artist_list, artist_ids))


store_data_fn()

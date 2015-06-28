import spotify
import sqlite3

artist = spotify.TrackCollector("Kanye West")
a = artist.ft_artists

conn = sqlite3.connect('%s.db' % artist.id)

c = conn.cursor()

c.execute('''DROP TABLE albums''')

c.execute('''CREATE TABLE albums (song_name text, song_id text, song_artists text, song_artists_ids text)''')

for ii in a:
	artist_ids  = []
	artist_list = []
	for jj in ii['artists']:
		artist_ids.append(jj['id'])
		artist_list.append(jj['name'])
	artist_ids  = ", ".join(artist_ids)
	artist_list = ", ".join(artist_list)
	c.execute("INSERT INTO albums (song_name, song_id, song_artists, song_artists_ids) VALUES (?, ?, ?, ?)", (ii['name'], ii['id'], artist_list, artist_ids))

conn.commit()

conn.close()


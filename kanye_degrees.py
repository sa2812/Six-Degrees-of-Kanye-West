from spotify import *
from db_conn import *


@db_wrapper
def create_table(c):
    try:
        c.execute("""CREATE TABLE kanye_degree (name text PRIMARY KEY,
                                                id text ,
                                                uri text,
                                                gen integer,
                                                ancestor text,
                                                track text,
                                                done integer)""")
        kanye_uri = "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x"
        seed_artist = sp.artist(kanye_uri)
        c.execute("""INSERT INTO kanye_degree VALUES (?, ?, ?, ?, NULL, NULL, ?)""",
                  (seed_artist['name'], seed_artist['id'], seed_artist['uri'], 0, 0))
    except:
        pass

@db_wrapper
def get_artist_not_done(c):
    c.execute("""SELECT kanye_degree.'name', kanye_degree.'uri', kanye_degree.'gen'
                 FROM kanye_degree
                 WHERE kanye_degree.'done'=0
                 ORDER BY kanye_degree.'gen' ASC""")
    return c.fetchone()

@db_wrapper
def update_table_new_artist(c, name, _id, uri, gen, ancestor, track):
    try:
        c.execute("""INSERT INTO kanye_degree
                     VALUES (?, ?, ?, ?, ?, ?, 0)""",
                  (name, _id, uri, gen, ancestor, track))
    except sqlite3.IntegrityError:
        pass

@db_wrapper
def mark_as_done(c, uri):
    c.execute("""UPDATE kanye_degree
                 SET done=1
                 WHERE uri='{}'""".format(uri))

create_table()

gen = 0
while gen < 7:
    current_name, current_uri, current_gen = get_artist_not_done()
    gen = current_gen + 1
    song_features = TrackCollector(name=current_name).song_features
    for song in song_features:
        for artist in song['artists']:
            if artist['uri'] != current_uri:
                update_table_new_artist(artist['name'],
                                        artist['id'],
                                        artist['uri'],
                                        gen,
                                        current_uri,
                                        song['id'])
    mark_as_done(current_uri)

from spotify import *
from db_conn import *
import csv


@db_wrapper
def gen_artist_list(c, name):
    """Generates a list of related artists given a seed."""
    try:
        c.execute("CREATE TABLE artist_list (artist text, id text, uri text)")
    except:
        pass

    artist = sp.search(q='artist:' + name,
                       type='artist')['artists']['items'][0]

    artists = [{'name'      : artist['name'],
                'id'        : artist['id'],
                'uri'       : artist['uri'],
                'done'      : False,
                'generation': 0}]
    c.execute("INSERT INTO artist_list VALUES (?, ?, ?, ?)",
              (artist['name'], artist['id'], artist['uri'], generation))
    artist_names = [artist['name']]
    max_gen = 0

    for jj in artists:
        if jj['done']:
            continue
        related = sp.artist_related_artists(jj['id'])
        new_gen = jj['generation'] + 1
        if new_gen > max_gen:
            max_gen += 1
            print "Maximum generation: {}".format(max_gen)
            print "Number of artists: {}".format(len(artist_names))
        for ii in related['artists']:
            add_to  = True
            if ii['name'] in artist_names:
                add_to = False
            if add_to:
                artists.append({'name': ii['name'],
                                'id': ii['id'],
                                'uri': ii['uri'],
                                'done': False,
                                'generation': new_gen})
                c.execute("INSERT INTO artist_list VALUES (?, ?, ?)",
                          (ii['name'], ii['id'], ii['uri']))
                artist_names.append(ii['name'])
        jj['done'] = True

        if max_gen > 7:
            break

kanye_uri = "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x"
gen_artist_list("Kanye West")

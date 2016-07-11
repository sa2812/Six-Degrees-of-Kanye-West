from db_conn import *
from featured import *
import logging
import pickle
import csv

logging.basicConfig(filename='logs\\artist_list_gen.log', level=logging.DEBUG)


@db_wrapper
def gen_artist_list(c, name, gen_limit=7, start=0):
    """Generates a list of related artists given a seed."""
    try:
        c.execute("""CREATE TABLE artist_list (artist TEXT,
                                               id TEXT,
                                               degree INTEGER)""")
    except:
        pass

    current_artist = sp.search(q='artist:' + name,
                               type='artist')['artists']['items'][0]

    _artist = {'name'       : current_artist['name'],
                'id'        : current_artist['id'],
                'uri'       : current_artist['uri'],
                'done'      : False,
                'generation': 0}
    with open('gen0.pkl', 'ab') as pklfile:
        pickle.dump(_artist, pklfile)

    c.execute("INSERT INTO artist_list VALUES (?, ?, ?, ?)",
              (current_artist['name'], current_artist['id'], current_artist['uri'], 0))
    try:
        artist_details = pickle.load(open('artist_details.pkl', 'rb'))
    except IOError:
        artist_details = {current_artist['name']: 1}
    max_gen = 0

    # for artist in artists:
    f = open('gen{}.pkl'.format(start), 'rb')
    while True:
        try:
            artist = pickle.load(f)
            try:
                if artist_details[artist['name']] == 1:
                    artist_info = ArtistInfo(name=artist['name'])
                    related = artist_info.ft_artists
                    new_gen = artist['generation'] + 1
                    if new_gen > max_gen:
                        max_gen = new_gen
                        logging.info("Maximum generation: {}".format(max_gen))
                        logging.info("Number of artists: {}".format(len(artist_details.keys())))
                        if max_gen > gen_limit:
                            pickle.dump(artist_details, open('artist_details.pkl', 'wb'))
                            return
                    for ii in related:
                        try:
                            trial = artist_details[ii['name']]
                        except KeyError:
                            _artist = {'name'      : ii['name'],
                                       'id'        : ii['id'],
                                       'uri'       : ii['uri'],
                                       'done'      : False,
                                       'generation': new_gen}
                            with open('gen{}.pkl'.format(new_gen), 'ab') as pklfile:
                                pickle.dump(_artist, pklfile)
                            c.execute("INSERT INTO artist_list VALUES (?, ?, ?, ?)",
                                      (ii['name'], ii['id'], ii['uri'], new_gen))
                            artist_details[ii['name']] = 1
                            pickle.dump(artist_details, open('artist_details.pkl', 'wb'))
                artist_details[artist['name']] == 2
                pickle.dump(artist_details, open('artist_details.pkl', 'wb'))
            except KeyError:
                raise KeyError("How did this happen?")
        except EOFError:
            pickle.dump(artist_details, open('artist_details.pkl', 'wb'))
            break

gen_artist_list("Kanye West")

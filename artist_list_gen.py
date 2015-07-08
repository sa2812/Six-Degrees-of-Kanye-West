from spotify import *
import sqlite3
import csv

def gen_list(name):
    conn = sqlite3.connect('release_info.db')
    c = conn.cursor()

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
    c.execute("INSERT INTO artist_list VALUES (?, ?, ?)",
              (artist['name'], artist['id'], artist['uri']))
    artist_names = [artist['name']]

    not_done = filter(lambda artist: artist['done'] == False, artists)

    for jj in artists:
        if jj['done']:
            continue
        related = sp.artist_related_artists(jj['id'])
        new_gen = jj['generation'] + 1
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
        if len(artists) > 10:
            break

    conn.commit()
    conn.close()

def gen_list_n(n):
    conn = sqlite3.connect('release_info.db')
    c = conn.cursor()

    try:
        c.execute("CREATE TABLE artist_list (artist text, id text, uri text)")
    except:
        pass

    name   = "Kanye West"
    artist = sp.search(q='artist:' + name,
                       type='artist')['artists']['items'][0]

    artists = [{'name'      : artist['name'],
                'id'        : artist['id'],
                'uri'       : artist['uri'],
                'done'      : False,
                'generation': 0}]
    c.execute("INSERT INTO artist_list VALUES (?, ?, ?)",
              (artist['name'], artist['id'], artist['uri']))
    artist_names = [artist['name']]

    not_done = filter(lambda artist: artist['done'] == False, artists)

    for jj in artists:
        if jj['done']:
            continue
        related = sp.artist_related_artists(jj['id'])
        new_gen = jj['generation'] + 1
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
        if len(artists) > n:
            break

    conn.commit()
    conn.close()

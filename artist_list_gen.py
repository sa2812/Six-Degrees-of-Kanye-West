from spotify import *
import csv

name   = "Kanye West"
artist = sp.search(q='artist:' + name,
			       type='artist')['artists']['items'][0]

artists = [{'name': artist['name'], 'id': artist['id'], 'uri': artist['uri']}]

rel = sp.artist_related_artists(artist['id'])
for ii in rel['artists']:
	artists.append({'name': ii['name'], 'id': ii['id'], 'uri': ii['uri'], 'done': False})
rel['done'] = True
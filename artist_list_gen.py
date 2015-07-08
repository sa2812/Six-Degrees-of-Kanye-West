from spotify import *
import csv

name   = "Kanye West"
artist = sp.search(q='artist:' + name,
			       type='artist')['artists']['items'][0]

artists = [{'name': artist['name'], 'id': artist['id'], 'uri': artist['uri'], 'done': False, 'generation': 0}]
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
			artists.append({'name': ii['name'], 'id': ii['id'], 'uri': ii['uri'], 'done': False, 'generation': new_gen})
			artist_names.append(ii['name'])
	jj['done'] = True
	if len(artists) > 100:
		break
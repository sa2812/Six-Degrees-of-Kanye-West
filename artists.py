"""
Discogs client connect
"""
import discogs_client
import json
import math
import config
import requests
import time
import fileinput

ITEMS_PER_PAGE = 50.

d = discogs_client.Client('Networker/0.1', user_token=config.token)

me = d.identity()

artist_name = "Danny Brown"
print artist_name
results = d.search(artist_name)

artist = results[0]
print "Discogs Name: "+artist.name
print "Artist ID: "+str(artist.id)
count = artist.releases.count
pages = int(math.ceil(count/ITEMS_PER_PAGE))
print count
print pages

all_releases = []
for ii in range(1, pages+1):
    all_releases += artist.releases.page(ii)

artist_releases = {}
for ii in all_releases:
    try:
        try:
            if (artist in ii.artists):
                artist_releases[ii.id] = {"title": ii.title,
                                          "artists": [jj.id for jj in ii.artists],
                                          "tracks": [{kk.title: [ll.id for ll in kk.artists]} for kk in ii.tracklist]}
        except AttributeError:
            if (artist in ii.main_release.artists):
                artist_releases[ii.id] = {"title": ii.title,
                                          "artists": [jj.id for jj in ii.main_release.artists],
                                          "tracks": [{kk.title: [ll.id for ll in kk.artists]} for kk in ii.tracklist]}
    except requests.exceptions.SSLError:
        pass

with open(artist_name+'.json', 'w') as outfile:
    json.dump(artist_releases, outfile)

print "All done"

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

artist_name = "Childish Gambino"
print artist_name
results = d.search(artist_name)

artist = results[0]
print artist.name
count = artist.releases.count
pages = int(math.ceil(count/ITEMS_PER_PAGE))
print 'Total pages: '+str(pages)

all_releases = []
for ii in range(1, pages+1):
    all_releases += artist.releases.page(ii)

artist_releases = {}

for jj in all_releases:
    try:
        try:
            if artist in jj.artists:
                print "Release: "+jj.title
                artist_releases[jj.id] = [jj.title, {"artists":[artist.id for artist in jj.artists]}, {"tracks": [track.title for track in jj.tracklist]}]
        except AttributeError:
            rel = jj.main_release
            if artist in rel.artists:
                print "Master:  "+rel.title
                artist_releases[rel.id] = [rel.title, {"artists":[artist.id for artist in rel.artists]}, {"tracks": [track.title for track in rel.tracklist]}]
    except (requests.exceptions.SSLError, UnicodeEncodeError):
        pass

with open(artist_name+'.txt', 'w') as outfile:
    json.dump(artist_releases, outfile)
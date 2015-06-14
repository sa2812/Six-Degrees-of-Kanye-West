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

d = discogs_client.Client('Networker/0.1', user_token=config.token)

me = d.identity()

artist_name = "Danny Brown"
print artist_name

results = d.search(artist_name)

artist = results[0]
count = artist.releases.count
pages = int(math.ceil(count/50.))
print 'Total pages: '+str(pages)

artist_releases = {}

ii = 0
while ii <= pages:
    try:
        a = artist.releases.page(ii)
        print "Current Page: "+str(ii)
        for jj in a:
            if hasattr(jj, "main_release"):
                try:
                    rel = jj.main_release
                    artist_releases[rel.id] = [rel.title, {"artists":[artist.id for artist in rel.artists]}, {"tracks": [track.title for track in rel.tracklist]}]
                except (requests.exceptions.SSLError, UnicodeEncodeError):
                    pass
            elif artist in jj.artists:
                try:
                    artist_releases[jj.id] = [jj.title, {"artists":[artist.id for artist in jj.artists]}, {"tracks": [track.title for track in jj.tracklist]}]
                except (requests.exceptions.SSLError, UnicodeEncodeError):
                    pass
    except requests.exceptions.SSLError:
        pass
    time.sleep(5)
    ii += 1

with open(artist_name+'.txt', 'w') as outfile:
    json.dump(artist_releases, outfile)
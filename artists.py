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
print artist.name, artist.id
count = artist.releases.count
pages = int(math.ceil(count/ITEMS_PER_PAGE))

all_releases = []
for ii in range(1, pages+1):
    all_releases += artist.releases.page(ii)

all_rel = []
for ii in all_releases:
    all_rel.append(ii.title)

with open(artist_name+'_releases.txt', 'w') as outfile:
    json.dump(all_rel, outfile)

print "Releases done"

all_artists = {}
for ii in all_releases:
    try:
        try:
            all_artists[ii.title] = [jj.name for jj in ii.artists]
        except AttributeError:
            all_artists[ii.title] = [jj.name for jj in ii.main_release.artists]
    except requests.exceptions.SSLError:
        pass

with open(artist_name+'_artists.txt', 'w') as outfile:
    json.dump(all_artists, outfile)

print "Artists done"

artist_releases = {}

# for jj in all_releases:
#     # try:
#     if hasattr(jj, "artists"):
#         if artist in jj.artists:
#             print "Release: "+jj.title
#             artist_releases[jj.id] = [jj.title,
#                                       {"artists":[artist.id for artist in jj.artists]},
#                                       {"tracks": [track.title.encode('ascii', 'ignore') for track in jj.tracklist]}]
#     elif hasattr(jj, "main_release"):
#         rel = jj.main_release
#         if artist in rel.artists:
#             print "Master:  "+rel.title
#             artist_releases[rel.id] = [rel.title,
#                                        {"artists":[artist.id for artist in rel.artists]},
#                                        {"tracks": [track.title.encode('ascii', 'ignore') for track in rel.tracklist]}]
#     else:
#         print "Unhandled: "+jj.title.encode('ascii', 'ignore')
#     # except (requests.exceptions.SSLError):
#     #     print "Failed: "+jj.title
#     time.sleep(1)

# with open(artist_name+'.txt', 'w') as outfile:
#     json.dump(artist_releases, outfile)
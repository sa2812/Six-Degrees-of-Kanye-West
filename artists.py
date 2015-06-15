"""
Discogs client connect
"""
import discogs_client
import json
import math
import config
import requests
import time
import numpy as np
import fileinput
import os.path
import pickle, pprint

ITEMS_PER_PAGE = 50.

d = discogs_client.Client('Networker/0.1', user_token=config.token)

artist_name = "Childish Gambino"
print artist_name
results = d.search(artist_name)

artist = results[0]
artist_name = artist.name
print "Discogs Name: "+artist.name
print "Artist ID: "+str(artist.id)
count = artist.releases.count
pages = int(math.ceil(count/ITEMS_PER_PAGE))
print "Number of items: "+str(count)
print "Number of pages: "+str(pages)

if os.path.exists('matched_releases\\'+artist_name+'.pkl') == False:
    all_releases = []
    matched_releases = []
    print "Creating all releases"
    retries = 0
    while retries < 10:
        try:
            for ii in range(1, pages+1):
                all_releases += artist.releases.page(ii)
            print "Writing releases to disk"
            for ii in all_releases:
                try:
                    if artist in ii.artists:
                        matched_releases.append(ii)
                except AttributeError:
                    if artist in ii.main_release.artists:
                        matched_releases.append(ii.main_release)
            retries += 100
        except requests.exceptions.SSLError:
            pass
        retries += 1
    print retries
    output1 = open('all_releases\\'+artist_name+'.pkl', 'wb')
    pickle.dump(all_releases, output1, -1)
    output1.close()
    output2 = open('matched_releases\\'+artist_name+'.pkl', 'wb')
    pickle.dump(matched_releases, output2, -1)
    output2.close()
else:
    print "Release list exists"
    _input = open('matched_releases\\'+artist_name+'.pkl', 'rb')
    all_releases = pickle.load(_input)
    pprint.pprint(all_releases)
    _input.close()
    print "Release list parsed in"

print all_releases

print "Release list step complete"


artist_releases = {}
MAX = len(all_releases)
progress = [int(ii) for ii in np.linspace(MAX/10, MAX, 10)]
pp = 0
while pp < MAX:
    ii = all_releases[pp]
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
    if pp in progress:
        print str((progress.index(pp)+1)*10)+"%"

    pp += 1

with open('release_info\\'+artist_name+'.json', 'w') as outfile:
    json.dump(artist_releases, outfile)

print "All done"

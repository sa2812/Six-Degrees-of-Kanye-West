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
import sys
import pickle

ITEMS_PER_PAGE = 50.

d = discogs_client.Client('Networker/0.1', user_token=config.token)

artist_name = "Nas"
print artist_name

results = d.search(artist_name)

basic_done = False
while not basic_done:
    try:
        artist = results[0]
        artist_name = artist.name
        count = artist.releases.count
        pages = int(math.ceil(count/ITEMS_PER_PAGE))
        print "Discogs Name: "+artist.name
        print "Artist ID: "+str(artist.id)
        print "Number of items: "+str(count)
        print "Number of pages: "+str(pages)
        basic_done = True
    except requests.exceptions.SSLError:
        pass

all_releases = []
matched_releases = []

if os.path.exists('all_releases\\'+artist_name+'.pkl') == False:
    success = False
    while not success:
        print "Compiling all associated releases"
        try:
            for ii in range(1, pages+1):
                all_releases += artist.releases.page(ii)
            success = True
        except requests.exceptions.SSLError:
            pass
    print "All releases compiled"

    output = open('all_releases\\'+artist_name+'.pkl', 'wb')
    pickle.dump(all_releases, output, -1)
    output.close()

else:
    _input = open('all_releases\\'+artist_name+'.pkl', 'rb')
    all_releases = pickle.load(_input)
    _input.close()
    print "All releases imported from file"

if os.path.exists('matched_releases\\'+artist_name+'.pkl') == False:
    success = False
    while not success:
        print "Compiling releases by artist"
        for ii in all_releases:
            try:
                try:
                    if artist in ii.artists:
                        matched_releases.append(ii)
                except AttributeError:
                    if artist in ii.main_release.artists:
                        matched_releases.append(ii.main_release)
                success = True
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
                pass

    print "Releases by artist compiled"
    output = open('matched_releases\\'+artist_name+'.pkl', 'wb')
    pickle.dump(matched_releases, output, -1)
    output.close()
else:
    print "Release list exists"
    _input = open('matched_releases\\'+artist_name+'.pkl', 'rb')
    matched_releases = pickle.load(_input)
    _input.close()
    print "Release list parsed in"

print "Release list step complete"

artist_releases = {}
MAX = len(matched_releases)
progress = [int(ii) for ii in np.linspace(MAX/10, MAX, 10)]
pp = 0
while pp < MAX:
    ii = matched_releases[pp]
    step_complete = False
    while not step_complete:
        try:
            try:
                artist_releases[ii.id] = {"title": ii.title,
                                          "artists": [jj.id for jj in ii.artists],
                                          "tracks": [{kk.title: [ll.id for ll in kk.artists]} for kk in ii.tracklist]}
                step_complete = True
            except AttributeError:
                artist_releases[ii.id] = {"title": ii.title,
                                          "artists": [jj.id for jj in ii.main_release.artists],
                                          "tracks": [{kk.title: [ll.id for ll in kk.artists]} for kk in ii.tracklist]}
                step_complete = True
        except requests.exceptions.SSLError:
            pass
    if pp in progress:
        print str((progress.index(pp)+1)*10)+"%"

    pp += 1

with open('release_info\\'+artist_name+'.json', 'w') as outfile:
    json.dump(artist_releases, outfile)

print "All done"

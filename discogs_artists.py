"""
Discogs client connect
"""
import discogs_client
import numpy as np
import fileinput
import requests
import os.path
import config
import pickle
import json
import math
import time
import sys

d = discogs_client.Client('Networker/0.1', user_token=config.discogs_token)

artist_name = "Outkast"
print artist_name

class Artist:
    def __init__(self, query):
        self.artist = None
        results     = d.search(query)
        basic_done  = False
        while not basic_done:
            try:
                self.artist = results[0]
                self.count  = self.artist.releases.count
                self.pages  = int(math.ceil(self.count/50.)) # 50 Items per page
                print "Discogs Name:    "+self.artist.name
                print "Artist ID:       "+str(self.artist.id)
                print "Number of items: "+str(self.count)
                print "Number of pages: "+str(self.pages)
                basic_done = True
            except requests.exceptions.SSLError:
                pass
        self.all_releases     = []
        self.matched_releases = []
        self.artist_releases  = {}

        self.all_releases_check     = (os.path.exists('all_releases\\'+self.artist.name+'.pkl'),
                                       "all_releases",
                                       self.all_releases,
                                       "all releases")
        self.matched_releases_check = (os.path.exists('matched_releases\\'+self.artist.name+'.pkl'),
                                       "matched_releases",
                                       self.matched_releases,
                                       "artist releases")

        if self.all_releases_check[0]:
            self.input_releases(self.all_releases_check)
        else:
            self.output_all_releases()

        if self.matched_releases_check[0]:
            self.input_releases(self.matched_releases_check)
        else:
            self.output_all_releases()

        self.create_release_info()

    def input_releases(self, check):
        _input = open(check[1]+'\\'+self.artist.name+'.pkl', 'rb')
        k = 0
        if check[3] == "all releases":
            self.all_releases = pickle.load(_input)
        else:
            self.matched_releases = pickle.load(_input)
            k = 1
        _input.close()
        print check[3]+" imported from file"
        if k:
            print "Release list step complete"

    def output_all_releases(self):
        print "Compiling all associated releases"
        ii = 1
        while ii <= self.pages:
            try:
                self.all_releases += self.artist.releases.page(ii)
                ii += 1
            except requests.exceptions.SSLError:
                pass
        print "All releases compiled"

        output = open('all_releases\\'+self.artist.name+'.pkl', 'wb')
        pickle.dump(self.all_releases, output, -1)
        output.close()

    def output_matched_releases(self):
        print "Compiling releases by artist"
        success = False
        while not success:
            for ii in self.all_releases:
                try:
                    try:
                        if artist in ii.artists:
                            self.matched_releases.append(ii)
                    except AttributeError:
                        if artist in ii.main_release.artists:
                            self.matched_releases.append(ii.main_release)
                    success = True
                except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
                    pass

        print "Releases by artist compiled"
        output = open('matched_releases\\'+self.artist.name+'.pkl', 'wb')
        pickle.dump(self.matched_releases, output, -1)
        output.close()
        print "Release list step complete"

    def create_release_info(self):
        if os.path.exists('release_info\\'+self.artist.name+'.json'):
            print "All done"
        else:
            MAX = len(self.matched_releases)
            progress = [int(ii) for ii in np.linspace(MAX/10, MAX, 10)]
            pp = 0
            while pp < MAX:
                ii = self.matched_releases[pp]
                step_complete = False
                while not step_complete:
                    try:
                        try:
                            self.artist_releases[ii.id] = {"title": ii.title,
                                                           "artists": [jj.id for jj in ii.artists],
                                                           "tracks": [{kk.title: [ll.id for ll in kk.artists]} for kk in ii.tracklist]}
                            step_complete = True
                        except AttributeError:
                            self.artist_releases[ii.id] = {"title": ii.title,
                                                           "artists": [jj.id for jj in ii.main_release.artists],
                                                           "tracks": [{kk.title: [ll.id for ll in kk.artists]} for kk in ii.tracklist]}
                            step_complete = True
                    except requests.exceptions.SSLError:
                        pass
                if pp in progress:
                    print str((progress.index(pp)+1)*10)+"%"

                pp += 1

            with open('release_info\\'+self.artist.name+'.json', 'w') as outfile:
                json.dump(self.artist_releases, outfile)

            print "All done"

a = Artist(artist_name)
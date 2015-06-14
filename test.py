"""
Tester

Connects to discogs to allow data extraction in the Python shell
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
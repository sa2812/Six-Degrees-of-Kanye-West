"""
Discogs client connect
"""
import discogs_client
import csv
import math
import config
import requests
import time
import fileinput

d = discogs_client.Client('Networker/0.1', user_token=config.token)

me = d.identity()

artist_name = "Childish Gambino"
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
                    if artist in rel.artists:
                        artist_releases[rel.id] = [rel.title, rel.artists, rel.tracklist]
                except (requests.exceptions.SSLError, UnicodeEncodeError):
                    pass
            elif artist in jj.artists:
                try:
                    artist_releases[rel.id] = [rel.title, rel.artists, rel.tracklist]
                except (requests.exceptions.SSLError, UnicodeEncodeError):
                    pass
    except requests.exceptions.SSLError:
        pass
    time.sleep(5)
    ii += 1

# with open(artist_name+'.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     ii = 0
#     while ii <= pages:
#         try:
#             a = artist.releases.page(ii)
#             print "Current Page: "+str(ii)
#             for jj in a:
#                 if hasattr(jj, "main_release"):
#                     try:
#                         rel = jj.main_release
#                         # if rel.artists[0].id == artist.id:
#                         if artist in rel.artists:
#                             write = [rel.title, rel.id]
#                             writer.writerow(write)
#                     except (requests.exceptions.SSLError, UnicodeEncodeError):
#                         pass
#                 elif artist in jj.artists:
#                     try:
#                         write = [jj.title, jj.id]
#                         writer.writerow(write)
#                     except (requests.exceptions.SSLError, UnicodeEncodeError):
#                         pass
#         except requests.exceptions.SSLError:
#             pass
#         time.sleep(5)
#         ii += 1


seen = set() # set for fast O(1) amortized lookup
for line in fileinput.FileInput(artist_name+'.csv', inplace=1):
    if line in seen: continue # skip duplicate

    seen.add(line)
    print line # standard output is now redirected to the file
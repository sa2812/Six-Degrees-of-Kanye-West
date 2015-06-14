"""
Discogs client connect
"""
import discogs_client
import config
import csv
import json
import math
import requests
import time
import fileinput

d = discogs_client.Client('Networker/0.1', user_token=config.token)

me = d.identity()
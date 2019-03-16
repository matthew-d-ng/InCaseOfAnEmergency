import time

import atoma, requests


""" Checks the Atom feed from USGS every 15 minutes """

WAIT_TIME = 900  # 900 seconds = 15 minutes, can just change this to less if we want
FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.atom"

def monitor_feed():

    latest_quakes_title_list = []
    response = requests.get(FEED)
    latest_quakes = atoma.parse_atom_bytes(response.content)
    latest_quakes_title_list = []
    for listing in latest_quakes.entries:
        latest_quakes_title_list.append(listing.title.value)

    return latest_quakes_title_list

    
# Infinitely loop, sleep for WAIT_TIME seconds after every iteration
while True: 
    earthquakeList = monitor_feed()

    time.sleep(WAIT_TIME)
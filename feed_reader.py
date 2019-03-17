import time

import atoma, requests

FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.atom"

def get_latest_quakes():

    latest_quakes_title_list = []
    response = requests.get(FEED)
    latest_quakes = atoma.parse_atom_bytes(response.content)
    latest_quakes_title_list = []
    for listing in latest_quakes.entries:
        latest_quakes_title_list.append(listing.title.value)

    return latest_quakes_title_list


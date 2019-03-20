import time

from earthquake import Earthquake
import atoma, requests, re


FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.atom"

def parse_listing(listing):
    """ Return Earthquake object """

    title = listing.title.value
    magnitude = float(re.search(r"\d*\.\d+|\d+", title).group())
    details = listing.summary.value

    timestamp = re.search(r"\d+-\d+-\d+ \d+:\d+:\d+", details).group()
    location = re.findall(r"(\d*\.\d+|\d+)&deg", details)
    latitude = location[0]
    longitude = location[1]

    depth = re.findall(r"(\d*\.\d+|\d+) km", details)[0]
    new_quake = Earthquake(title, magnitude, '', timestamp, latitude, longitude, depth)
    return new_quake

def get_latest_quakes():
    response = requests.get(FEED)
    latest_quakes = atoma.parse_atom_bytes(response.content)
    latest_quakes_title_list = []
    for listing in latest_quakes.entries:
        eq = parse_listing(listing)
        entry = "" + eq.timestring + " : " + eq.title
        print(entry)
        latest_quakes_title_list.append(eq)

    return latest_quakes_title_list


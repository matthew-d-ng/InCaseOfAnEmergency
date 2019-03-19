import time

from earthquake import Earthquake
import atoma, requests, re


FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.atom"

def parse_listing(listing):
    """ Return Earthquake object """

    title = listing.title.value
    magnitude = float(re.search(r"\d*\.\d+|\d+", title).group())
    details = listing.summary.value

    datetime = re.search(r"\d+-\d+-\d+ \d+:\d+:\d+", details).group().split(" ")
    date = datetime[0]
    time = datetime[1]

    location = re.findall(r"(\d*\.\d+|\d+)&deg", details)
    latitude = location[0]
    longitude = location[1]

    depth = re.findall(r"(\d*\.\d+|\d+) km", details)[0]

    new_quake = Earthquake(title, magnitude, time, date, latitude, longitude, depth)
    return new_quake

def get_latest_quakes():
    response = requests.get(FEED)
    latest_quakes = atoma.parse_atom_bytes(response.content)
    latest_quakes_title_list = []
    for listing in latest_quakes.entries:
        eq = parse_listing(listing)
        latest_quakes_title_list.append(str(str(eq.timestamp), " :", eq.place))

    return latest_quakes_title_list

get_latest_quakes()
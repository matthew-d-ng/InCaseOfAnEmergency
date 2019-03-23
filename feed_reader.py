from earthquake import Earthquake
import requests, json
from datetime import datetime


FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"

def parse_listing(listing):
    """ Return Earthquake object """

    db_id = listing["id"]
    properties = listing["properties"]

    title = properties["title"]
    magnitude = properties["mag"]

    raw_time = properties["time"] // 1000  # integer div by 1000 because it's in ms
    timestamp = datetime.utcfromtimestamp(raw_time)

    location = listing["geometry"]["coordinates"]
    latitude = location[0]
    longitude = location[1]
    depth = location[2]

    new_quake = Earthquake(db_id, title, magnitude, timestamp, latitude, longitude, depth)
    return new_quake


def get_latest_quakes():
    response = requests.get(FEED)
    latest_quakes = json.loads(response.text)
    latest_quakes_title_list = []
    for listing in latest_quakes["features"]:
        eq = parse_listing(listing)
        entry = "" + eq.timestring + " : " + eq.title
        print(entry)
        latest_quakes_title_list.append(eq)

    return latest_quakes_title_list


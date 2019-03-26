from earthquake import Earthquake
import requests, json, geocoder
from datetime import datetime
import math

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
        latest_quakes_title_list.append(eq)

    return latest_quakes_title_list

def get_latest_quakes_filtered(magnitude, location):
    response = requests.get(FEED)
    latest_quakes = json.loads(response.text)
    latest_quakes_title_list = []
    for listing in latest_quakes["features"]:
        eq = parse_listing(listing)
        if(listing.magnitude >= magnitude):
            location = geocoder.google(location)
            coords = location.latlng
            is_within = is_within_radius(coords[0], coords[1], 100, listing.latitude, listing.longitude)
            if(is_within):
                latest_quakes_title_list.append(eq)

    return latest_quakes_title_list
    

def is_within_radius(centre_lat, centre_long, radius, input_lat, input_long):
    distance = math.sqrt((input_lat - centre_lat)**2 + (input_long - centre_long)**2)
    if(distance <= radius):
        return True
    else:
        return False
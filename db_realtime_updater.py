import time
# import the sql connector we're using too
import requests, json
from datetime import datetime
from earthquake import Earthquake
from feed_reader import parse_listing

""" Checks the Atom feed from USGS every 15 minutes """

WAIT_TIME = 900  # 900 seconds = 15 minutes, can just change this to less if we want
FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"


def db_has_earthquake(earthquake):
    """ Return boolean """

    # sql query code - is there a result for this ID?
    # *We need to check that the IDs are actually consistent
    return False


def add_to_db(earthquake):

    # sql insert to Earthquake table code
    pass     # placeholder, remove return when body written


def notify_mailing_list(earthquake):

    # mailing list code
    pass    # placeholder, remove return when body written


def monitor_feed():
    # Infinitely loop, sleep for WAIT_TIME seconds after every iteration
    while True:

        response = requests.get(FEED)
        latest_quakes = json.loads(response.text)
        # print(latest_quakes)

        for listing in latest_quakes["features"]:

            earthquake = parse_listing(listing)
            if earthquake.magnitude >= 5 and not db_has_earthquake(earthquake):
                add_to_db(earthquake)
                notify_mailing_list(earthquake)

        time.sleep(WAIT_TIME)


def test_feed():
    response = requests.get(FEED)
    data = json.loads(response.text)

    for listing in data["features"]:
        # print(listing)
        earthquake = parse_listing(listing)
        print(earthquake.id)
        print(earthquake.title)
        print(earthquake.timestring)
        print(earthquake.magnitude)
        print(earthquake.latitude)
        print(earthquake.longitude)
        print(earthquake.depth, "\n")





import time
# import the sql connector we're using too
import atoma, requests
import re
from earthquake import Earthquake

""" Checks the Atom feed from USGS every 15 minutes """

WAIT_TIME = 900  # 900 seconds = 15 minutes, can just change this to less if we want
FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.atom"


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


def monitor_feed():
    # Infinitely loop, sleep for WAIT_TIME seconds after every iteration
    while True:

        response = requests.get(FEED)
        latest_quakes = atoma.parse_atom_bytes(response.content)
        # print(latest_quakes)
        
        for listing in latest_quakes.entries:

            earthquake = parse_listing(listing)
            if earthquake.magnitude >= 5 and not db_has_earthquake(earthquake):
                add_to_db(earthquake)
                notify_mailing_list(earthquake)
        
        time.sleep(WAIT_TIME)


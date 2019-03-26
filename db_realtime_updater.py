import time
# pip install feedparser
import feedparser as fp
from earthquake import Earthquake
# import the sql connector we're using too

""" Checks the Atom feed from USGS every 15 minutes """

WAIT_TIME = 900  # 900 seconds = 15 minutes, can just change this to less if we want
FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.atom"
# ^ this feed is for richter 4.5+, add extra checks within our code to filter for only 5+
# unless we decide to just use 4.5+

def db_has_earthquake(earthquake):
    """ Return boolean """

    # sql query code - is there a result for this ID?
    # *We need to check that the IDs are actually consistent
    return True


def add_to_db(earthquake):

    # sql insert to Earthquake table code
    return None     # placeholder, remove return when body written


def notify_mailing_list(earthquake):

    # mailing list code
    return None    # placeholder, remove return when body written


def parse_listing(earthquake):
    """ Return Earthquake object """

    # code
    return None


def monitor_feed():
    # Infinitely loop, sleep for WAIT_TIME seconds after every iteration
    while True:

        latest_quakes = fp.parse(FEED)
        for listing in latest_quakes['entries']:

            # print listing['title']
            # The "Updated" field is not actually the time of the earthquake
            # The real time is within 'summary_detail' somewhere, needs to be parsed out

            print(listing['summary_detail'], "\n")

            earthquake = parse_listing(listing)

            if not db_has_earthquake(earthquake):

                add_to_db(earthquake)
                notify_mailing_list(earthquake)

        time.sleep(WAIT_TIME)

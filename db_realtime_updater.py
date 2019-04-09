import time
from earthquake import Earthquake
import requests, json
from feed_reader import parse_listing
from emails import send_emails
import threading
import mysql.connector
import config
# import the sql connector we're using too

""" Checks the GeoJSON feed from USGS every 15 minutes """

FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"
WAIT_TIME = 900  # 900 seconds = 15 minutes, can just change this to less if we want
MIN_MAG = 5

icoe = mysql.connector.connect(user=config.user, password=config.password,\
                                host=config.host, database=config.db,\
                                auth_plugin='mysql_native_password')

class db_realtime(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        monitor_feed()

def db_has_earthquake(earthquake):
    """ Return boolean """
    # SELECT EXISTS(SELECT * from ExistsRowDemo WHERE ExistId=105);
    cursor = icoe.cursor() 
    try:    
        sql_insert_query = """ SELECT * from earthquakes WHERE id=%s """
        insert_tuple = (earthquake.id,)
        cursor.execute(sql_insert_query, insert_tuple)
        result = cursor.fetchall()
    except (mysql.connector.Error) as error:
        icoe.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if icoe.is_connected():
            cursor.close()

    return len(result) > 0


def insert_to_db(earthquake):

    print("Updating db")
    cursor = icoe.cursor()
    try:
        sql_insert_query = """ INSERT INTO `earthquakes`
                            (`timestamp`, `latitude`, `longitude`, `depth`, `mag`, `id`, `title`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        insert_tuple = (earthquake.time_string(), earthquake.latitude, earthquake.longitude, earthquake.depth, earthquake.magnitude, earthquake.id, earthquake.title)
        cursor.execute(sql_insert_query, insert_tuple)
        icoe.commit()
    except (mysql.connector.Error) as error:
        icoe.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if icoe.is_connected():
            cursor.close()
    

def notify_mailing_list(earthquake):
    send_emails()

def monitor_feed():
    # Infinitely loop, sleep for WAIT_TIME seconds after every iteration
    while True:
        print("Checking feed")
        response = requests.get(FEED)
        latest_quakes = json.loads(response.text)
        for listing in latest_quakes['features']:

            earthquake = parse_listing(listing)
            if earthquake.magnitude >= MIN_MAG and not db_has_earthquake(earthquake):
                insert_to_db(earthquake)
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
        print(earthquake.time_string())
        print(earthquake.magnitude)
        print(earthquake.latitude)
        print(earthquake.longitude)
        print(earthquake.depth, "\n")
        print(db_has_earthquake(earthquake))


if __name__ == "__main__":
    test_feed()
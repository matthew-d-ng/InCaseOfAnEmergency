# CSV COLUMNS:
#   time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type,
#   horizontalError,depthError,magError,magNst,status,locationSource,magSource

# Columns for Earthquakes table:
'''
  `timestamp` text NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `depth` double NOT NULL,
  `mag` double NOT NULL,
  `id` text NOT NULL,
  `title` text NOT NULL
'''

""" POPULATE DATABASE WITH SAMPLE DATA FROM A FILE """
# pip install mysql-connector-python
# ^ somehow different to pip install mysql-connector

import mysql.connector
import config
import csv
import getpass
import sys
import urllib
import datetime
import requests
import json
from feed_reader import parse_listing
from dateutil import relativedelta
MIN_MAG = "4.5"
OLDEST_RECORD = 1900

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
# https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=yyyy-dd-mm&endtime=yyyy-dd-mm&minmagnitude=x

icoe = mysql.connector.connect(user=config.user, password=config.password,\
                                                host=config.host, database=config.db,\
                                                auth_plugin='mysql_native_password')

# for each line in all_week.csv:
#   insert to table Earthquake
def insert_to_db(earthquake):
    """
    `timestamp` text NOT NULL,
    `latitude` double NOT NULL,
    `longitude` double NOT NULL,
    `depth` double NOT NULL,
    `mag` double NOT NULL,
    `id` text NOT NULL,
    `title` text NOT NULL
    """
    try:
        cursor = icoe.cursor()
        sql_insert_query = """ INSERT INTO `earthquakes`
                            (`timestamp`, `latitude`, `longitude`, `depth`, `mag`, `id`, `title`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        insert_tuple = (earthquake.time_string(), earthquake.latitude, earthquake.longitude, earthquake.depth, earthquake.magnitude, earthquake.id, earthquake.title)
        cursor.execute(sql_insert_query, insert_tuple)
        icoe.commit()
    
    except (mysql.connector.Error) as error:
        icoe.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    
    finally:
        #closing database connection.
        if(icoe.is_connected()):
            cursor.close()
            # icoe.close()
            print("MySQL connection is closed")


def get_quakes():
    request = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2019-01-26&endtime=2019-03-26&minmagnitude=4.5'
    response = requests.get(request)
    latest_quakes = json.loads(response.text)
    #print(latest_quakes)
    for listing in latest_quakes["features"]:
        earthquake = parse_listing(listing)
        print(earthquake.id)
        print(earthquake.title)
        print(earthquake.timestamp)
        print(earthquake.magnitude)
        print(earthquake.latitude)
        print(earthquake.longitude)
        print(earthquake.depth, "\n")
        insert_to_db(earthquake)


def grab_data():
    min_date = datetime.datetime.strptime("1900-01-01", "%Y-%m-%d")
    enddate = datetime.datetime.today()

    while enddate > min_date:

        startdate = enddate - relativedelta.relativedelta(months=3)
        # convert to string
        starttime = startdate.strftime('%Y-%m-%d')
        endtime = enddate.strftime('%Y-%m-%d')
        # query api
        request = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime="+starttime+"&endtime="+endtime+"&minmagnitude="+MIN_MAG
        response = requests.get(request)
        latest_quakes = json.loads(response.text)

        for listing in latest_quakes["features"]:
            earthquake = parse_listing(listing)
            insert_to_db(earthquake)
            print(earthquake.id)
            print(earthquake.title)
            print(earthquake.time_string())
            print(earthquake.magnitude)
            print(earthquake.latitude)
            print(earthquake.longitude)
            print(earthquake.depth, "\n")
            

        enddate = startdate

if __name__ == "__main__":
    # print(icoe.is_connected())
    grab_data()
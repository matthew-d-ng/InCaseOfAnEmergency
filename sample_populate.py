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
  `magType` text NOT NULL,
  `id` text NOT NULL,
  `place` text NOT NULL,
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
MINMAG = 4.5
OLDEST_RECORD = 1900

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
# https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=yyyy-dd-mm&endtime=yyyy-dd-mm&minmagnitude=x

# for each line in all_week.csv:
#   insert to table Earthquake
def insert_to_db():
    return True

#contents = urllib.request.urlopen("http://example.com/foo/bar").read()

def get_quakes():
    request = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2019-01-26&endtime=2019-03-26&minmagnitude=4.5'
    response = requests.get(request)
    latest_quakes = json.loads(response.text)
    print(latest_quakes)

    for listing in latest_quakes["features"]:
        earthquake = parse_listing(listing)
        print(earthquake.id)
        print(earthquake.title)
        print(earthquake.timestring)
        print(earthquake.magnitude)
        print(earthquake.latitude)
        print(earthquake.longitude)
        print(earthquake.depth, "\n")

    

def main():
    now = datetime.datetime.now()
    current_year = now.year
    if len(sys.argv) == 5:
        startYear = sys.argv[1]
        startMonth = sys.argv[2]
        endYear = sys.argv[3]
        endMonth = sys.argv[4]
        try:
            startYear = int(startYear)
            startMonth = int(startMonth)
            endYear = int(endYear)
            endMonth = int(endMonth)
        except:
            print("You must enter 4 integer values.")
            return False
        if startMonth > 12 | startMonth < 0 | endMonth > 12 | endMonth < 0:
            print("Month values must be within the range, 0-12.")
            return False
        if startYear > current_year | startYear < OLDEST_RECORD | endYear > current_year | endYear < OLDEST_RECORD:
            print("Year values must be within the range, ",current_year,"-",OLDEST_RECORD,".")
            return False
        if startMonth > 12 | startMonth < 0 | endMonth > 12 | endMonth < 0:
            print("Month values must be withint the range, 0-12")
            return False
        if startYear < endYear:
            print("startYear must be > then endYear.")
            return False
        if startMonth < endMonth:
            print("startMonth must be > then endMonth.")
            return False
    else:
        print("You must enter 4 parameters: 'python sample_populate.py yyyy mm yyyy mm'(startYear startMonth endYear endMonth).")
    
    '''
    icoe = mysql.connector.connect(user=config.user, password=config.password,\
                                                    host=config.host, database=config.db,\
                                                    auth_plugin='mysql_native_password')
    cursor = icoe.cursor()
    cursor.execute("show databases")
    print('hello?')
    for i in cursor:
        print(i)

    addRow = ("INSERT INTO earthquakes " "(timestamp,latitude,longitude,depth,mag,magType,id,place,)""VALUES (%s, %d, %d, %d, %d, %s, %s, %s)")
    with open(csvFilename+".csv") as csvfile:
        csvRow = csv.reader(csvfile, delimiter='\n')
    for row in csvRow:
        csvField = csv.reader(csvfile, delimiter=',')
    cursor.execute('addRow')
    icoe.close()
    '''

#main()
get_quakes()

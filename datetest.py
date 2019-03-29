import datetime
from dateutil import relativedelta
import requests
import json
from feed_reader import parse_listing

min_date = datetime.datetime.strptime("1900-01-01", "%Y-%m-%d")
enddate = datetime.datetime.today()

while enddate > min_date:

  startdate = enddate - relativedelta.relativedelta(months=3)
  # convert to string
  starttime = startdate.strftime('%Y-%m-%d')
  endtime = enddate.strftime('%Y-%m-%d')
  # query api
  request = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime="+starttime+"&endtime="+endtime+"&minmagnitude=4.5"
  response = requests.get(request)
  latest_quakes = json.loads(response.text)

  for listing in latest_quakes["features"]:
      earthquake = parse_listing(listing)
      print(earthquake.id)
      print(earthquake.title)
      print(earthquake.time_string())
      print(earthquake.magnitude)
      print(earthquake.latitude)
      print(earthquake.longitude)
      print(earthquake.depth, "\n")

  enddate = startdate

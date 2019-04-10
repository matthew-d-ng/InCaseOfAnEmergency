# InCaseOfAnEmergency

This system revolves around a webpage visualisation of a MySQL database of earthquake data from 1900 to the present day. The webpage displays a map. A user may enter a search query for any location and earthquakes around the given location will appear as markers on the map. Each marker will display specific information about the earthquake if clicked. Users may subscribe to a mailing list, and receive realtime updates on occurring earthquakes around a subscribed location. The realtime system will also automatically update the database for future map queries.

# Usage

Involves setting the FLASK_APP environment variable to main, and then running flask.
Your Google API key must also be passed as an environment variable, in order to use the geocoding service.

```
export GOOGLE_API_KEY= <your key here>
export FLASK_APP="main.py"
flask run
```

# Technical Details

## Webpage

The webpage contains:
- An interactive map (from Google Maps)
- A subscription service (For our "realtime" email system)
- A search bar (Which receives a user query and converts it to a map location using the geocoder API)
- A live feed of earthquakes around the world (Source of information is the GeoJSON feed from the realtime system)

Queries the MySQL database to retrieve map markers around the location query.

### APIs/Services used:
- [Python Flask](http://flask.pocoo.org/)
- [Geocoder](https://developers.google.com/maps/documentation/geocoding/intro)
- [wtforms](https://wtforms.readthedocs.io/en/stable/)

## Realtime system

[db_realtime_updater.py](https://github.com/matthew-d-ng/InCaseOfAnEmergency/blob/master/db_realtime_updater.py) is the core of the realtime system. 
It is started as a thread when [main.py](https://github.com/matthew-d-ng/InCaseOfAnEmergency/blob/master/main.py) is run, and will query the GeoJSON feed from the USGS service every 15 minutes. Each earthquake in the live feed will be checked against our database, and if they are not already in it, we insert a new entry into the database. At the same time we insert the new entry, an email will be sent to those users who have subscribed to the area in which the earthquake occurred.

### APIs/Services used:
- [USGS GeoJSON Feed](https://earthquake.usgs.gov/earthquakes/feed/)
- [yagmail](https://pypi.org/project/yagmail/)

## Historical Database

The MySQL database contains historical earthquake data from 1900-present.

### APIs/Services used:
- MySQL
- [ANSS Comprehensive Earthquake Catalogue (ComCat)](https://earthquake.usgs.gov/data/comcat/)

### Setting up the Mailing System
Change HOST_DNS in emails.py to the actual DNS of the server the website is running on.

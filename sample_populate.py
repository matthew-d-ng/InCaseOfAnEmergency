# CSV COLUMNS:
#   time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type,
#   horizontalError,depthError,magError,magNst,status,locationSource,magSource

""" POPULATE DATABASE WITH SAMPLE DATA FROM A FILE """

# pip install mysql-connector-python
# ^ somehow different to pip install mysql-connector
import mysql.connector
import config

def insert_to_db:
    return None

icoe = mysql.connector.connect(user=config.user, password=config.password,
                                                    host=config.host, database=config.db,
                                                    auth_plugin='mysql_native_password')

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

# for each line in all_week.csv:
#   insert to table Earthquake


icoe.close()
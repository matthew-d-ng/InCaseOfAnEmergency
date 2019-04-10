
import mysql.connector
import config

# DO NOT RUN UNLESS YOUR COLUMNS ARE INCORRECT
# DO NOT RUN ON SULLA'S SERVER, THOSE COLUMNS ARE CORRECT
# ONLY RUN IF YOUR LOCAL MACHINE DATA IS WRONG

icoe = mysql.connector.connect(user=config.user, password=config.password,\
                              host=config.host, database=config.db,\
                              auth_plugin='mysql_native_password')


cursor = icoe.cursor()

sql_alter = "ALTER TABLE `earthquakes` CHANGE COLUMN `latitude` `lat` double NOT NULL"
cursor.execute(sql_alter)
icoe.commit()

sql_alter = "ALTER TABLE `earthquakes` CHANGE COLUMN `longitude` `long` double NOT NULL"
cursor.execute(sql_alter)
icoe.commit()

sql_alter = "ALTER TABLE `earthquakes` CHANGE COLUMN `lat` `longitude` double NOT NULL"
cursor.execute(sql_alter)
icoe.commit()

sql_alter = "ALTER TABLE `earthquakes` CHANGE COLUMN `long` `latitude` double NOT NULL"
cursor.execute(sql_alter)
icoe.commit()

cursor.close()
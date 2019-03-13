LOAD DATA
LOCAL INFILE '/Users/conogolaoghaire/Desktop/ncedc-earthquakes-dataset/earthquakes.txt' INTO TABLE Earthquakes
COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\r\n'; 
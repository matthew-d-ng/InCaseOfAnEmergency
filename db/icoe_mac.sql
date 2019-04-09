CREATE DATABASE icoe;

CREATE TABLE `earthquakes` (
  `timestamp` datetime NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `depth` double NOT NULL,
  `mag` double NOT NULL,
  `id` varchar(64) NOT NULL,
  `title` text NOT NULL,
  PRIMARY KEY (`id`)
)
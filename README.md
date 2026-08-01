# Namazu

Earthquake Data Analysis Platform for Japan

## Create database

install postgresql and command and execute the following commands
CREATE USER earthquakes_user WITH PASSWORD '1234';
CREATE DATABASE earthquakes OWNER earthquakes_user;

# create test table for unittest

CREATE DATABASE test_db_earthquakes OWNER earthquakes_user;

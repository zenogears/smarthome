#!/usr/bin/python3
#! -*- coding: utf8 -*-

import sqlite3
import sys
import Adafruit_DHT
import configparser
import time

config = configparser.RawConfigParser()
config.read("/home/pi/global_config.conf")

databasename = "mydatabase.db"

mytime = time.strftime("%Y %m %d %H:%M:%S", time.gmtime(time.time()))

conn = sqlite3.connect(databasename) # или :memory: чтобы сохранить в RAM

# Parse command line parameters.

sensor = Adafruit_DHT.DHT11
pin = config.getint("temp_pins" , "temp1")

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print ('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print ('Failed to get reading. Try again!')
    sys.exit(1)



cursor = conn.cursor()
# Создание таблицы
#cursor.execute("""CREATE TABLE tempdata
#                  (time, temp, humidity)
#               """)
#conn.commit()

#print("INSERT INTO tempdata VALUES ({0},{1},{2})".format(mytime,temperature,humidity))
cursor.execute("""INSERT INTO tempdata VALUES ("{0}",{1},{2})""".format(mytime,temperature,humidity))

conn.commit()

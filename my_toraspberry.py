#!/usr/bin/python3
#! -*- coding: utf8 -*-

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, SmallInteger
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from app import app, db
from config import Config

#from config import Config

#app = Flask(__name__)
#app.config.from_object(Config)

import datetime
import sys
import configparser
import time
import os

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'] , echo=True)

#config = configparser.RawConfigParser()
#config.read("/home/pi/global_config.conf")

mytime = time.strftime("%Y %m %d %H:%M:%S", time.gmtime(time.time()))

#conn = sqlite3.connect(databasename) # или :memory: чтобы сохранить в RAM

# Parse command line parameters.

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
# if humidity is not None and temperature is not None:
#     print ('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
# else:
#     print ('Failed to get reading. Try again!')
#     sys.exit(1)

metadata = MetaData()
Raspb3B = Table('Raspb3B', metadata,
    Column('id', Integer, primary_key = True),
    Column('type', String, index = True),
    Column('number', String, index = True),
    Column('pin_info', String),
    Column('connected', String),
    )

RasModels = Table('RasModels', metadata,
    Column('id',Integer, primary_key = True),
    Column('mname',String, index = True),
    Column('mpins',Integer, index = True),
    )

ins = RasModels.insert().values(nmane='', mpins='')
print(ins)
print(ins.compile().params)

conn = engine.connect()
result = conn.execute(ins)

s = select([Temp])
result = conn.execute(s)

for row in result:
	print(row)

#!/usr/bin/python3
import sys
import datetime
from sqlalchemy import create_engine, DateTime, SmallInteger, Integer, Table, Column, MetaData, ForeignKey, select
import os
import Adafruit_DHT

basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/..', 'smarthome.db')



engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def timetoutc(mytime):
  UTC_OFFSET_TIMEDELTA = datetime.datetime.now() - datetime.datetime.utcnow()
  result_utc_datetime = mytime + UTC_OFFSET_TIMEDELTA
  return result_utc_datetime.strftime("%Y %m %d %H:%M:%S")

def update_temphum():
  sensor = Adafruit_DHT.DHT11
  pin = 2
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

  metadata = MetaData()
  Temp = Table('Temp', metadata,
        Column('id', Integer, primary_key=True),
        Column('time', DateTime),
        Column('temperature', SmallInteger),
        Column('humidity', SmallInteger),
    )

  ins = Temp.insert().values(time=datetime.datetime.utcnow(), temperature=temperature, humidity=humidity)
  conn = engine.connect()
  result = conn.execute(ins)

  s = select([Temp])
  result = conn.execute(s)

def getlastinfo():
  returnfetch = []
  metadata = MetaData()
  Temp = Table('Temp', metadata,
          Column('id', Integer, primary_key=True),
          Column('time', DateTime),
          Column('temperature', SmallInteger),
          Column('humidity', SmallInteger),
      )

  s = select([Temp]).order_by('-id').limit(1)

  conn = engine.connect()
  result = conn.execute(s)
  for item in result:
    returnfetch.append((item[0],timetoutc(item[1]),item[2],item[3]))

  return(returnfetch)

def getinfo(items=50):
  returnfetch = []
  metadata = MetaData()
  Temp = Table('Temp', metadata,
          Column('id', Integer, primary_key=True),
          Column('time', DateTime),
          Column('temperature', SmallInteger),
          Column('humidity', SmallInteger),
      )

  s = select([Temp]).order_by('-id').limit(items)

  conn = engine.connect()
  result = conn.execute(s)
  for item in result:
    returnfetch.append((item[0],timetoutc(item[1]),item[2],item[3]))

  return(returnfetch)

def getgraphinfo():
  returnfetch = {}
  returnfetch['temp'] = []
  returnfetch['humi'] = []
  returnfetch['time'] = []
  metadata = MetaData()
  Temp = Table('Temp', metadata,
          Column('id', Integer, primary_key=True),
          Column('time', DateTime),
          Column('temperature', SmallInteger),
          Column('humidity', SmallInteger),
      )

  s = select([Temp])

  conn = engine.connect()
  result = conn.execute(s)
  for item in result:
    returnfetch['time'].append(item[1])
    returnfetch['temp'].append(item[2])
    returnfetch['humi'].append(item[3])

  return(returnfetch)

if __name__ == '__main__':
  getinfo()
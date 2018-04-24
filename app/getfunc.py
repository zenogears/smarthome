#!/usr/bin/python3
import sys
import datetime
from sqlalchemy import create_engine, DateTime, SmallInteger, Integer, Table, Column, MetaData, ForeignKey, select
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def timetoutc(mytime):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.now() - datetime.datetime.utcnow()
    result_utc_datetime = mytime + UTC_OFFSET_TIMEDELTA
    return result_utc_datetime.strftime("%Y %m %d %H:%M:%S")

def getinfo():
  returnfetch = []
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
    returnfetch.append((item[0],timetoutc(item[1]),item[2],item[3]))

  return(returnfetch)

if __name__ == '__main__':
  getinfo()
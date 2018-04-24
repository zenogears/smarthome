#!/usr/bin/python3
import sqlite3
import sys
import pytz, datetime

def timetoutc(mytime):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.now() - datetime.datetime.utcnow()
    local_datetime = datetime.datetime.strptime(mytime, "%Y %m %d %H:%M:%S")
    result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA

    return result_utc_datetime.strftime("%Y %m %d %H:%M:%S")

def getinfo():
  conn = sqlite3.connect(SQLALCHEMY_DATABASE_URI)
  cursor = conn.cursor()

  sql = "SELECT * FROM tempdata"

  cursor.execute(sql)
  myfetch = cursor.fetchall()
  returnfetch = []
  for item in myfetch:
    returnfetch.append((timetoutc(item[0]),item[1],item[2]))


  return(returnfetch)

if __name__ == '__main__':
  getinfo()

#!/usr/bin/python3
import sqlite3
import sys
import pytz, datetime

<<<<<<< HEAD
def timetoutc(mytime):
    UTC_OFFSET_TIMEDELTA = datetime.datetime.now() - datetime.datetime.utcnow()
    local_datetime = datetime.datetime.strptime(mytime, "%Y %m %d %H:%M:%S")
    result_utc_datetime = local_datetime + UTC_OFFSET_TIMEDELTA
    
    return result_utc_datetime.strftime("%Y %m %d %H:%M:%S")
=======


def timetoutc(mytime):
    local = pytz.timezone("Pacific/Truk")
    naive = datetime.datetime.strptime(mytime, "%Y %m %d %H:%M:%S")
    local_dt = local.localize(naive)
    #utc_dt = local_dt.astimezone(pytz.utc)

    return local_dt.strftime("%Y %m %d %H:%M:%S")
>>>>>>> 7aadf03475cd663874a2e34d6cc1607404838c24

def getinfo():
  conn = sqlite3.connect('/home/pi/git/Web/mydatabase.db')
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

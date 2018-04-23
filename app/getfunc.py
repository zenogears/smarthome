#!/usr/bin/python3
import sqlite3
import sys
import pytz, datetime

local = pytz.timezone("Europe/Moscow")



def timetoutc(mytime):

    naive = datetime.datetime.strptime(mytime, "%Y %m %d %H:%M:%S")
    local_dt = local.localize(naive)
    utc_dt = local_dt.astimezone(pytz.utc)

    return local_dt.strftime("%Y %m %d %H:%M:%S")

def getinfo():
  conn = sqlite3.connect('/home/zen/git/smarthome/mydatabase.db')
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

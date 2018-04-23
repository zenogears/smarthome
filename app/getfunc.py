#!/usr/bin/python3
import sqlite3

def getinfo():
  conn = sqlite3.connect("/home/pi/git/Web/mydatabase.db")
  cursor = conn.cursor()

  sql = "SELECT * FROM tempdata"

  cursor.execute(sql)
  return(cursor.fetchall())

if __name__ == '__main__':
  getinfo()

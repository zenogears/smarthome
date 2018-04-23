#!/usr/bin/python3
import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

sql = "SELECT * FROM tempdata"

cursor.execute(sql)
print(cursor.fetchall())
conn.commit()

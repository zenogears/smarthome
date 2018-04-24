#!/usr/bin/python3
#! -*- coding: utf8 -*-

from app import app, db
from sqlalchemy import create_engine, select, DateTime, SmallInteger, Integer, Table, Column, MetaData
from config import SQLALCHEMY_DATABASE_URI

def mainfunc():
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

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

    for row in sorted(result, key=lambda x: x['id']):
        print(row)

if __name__ == '__main__':
    mainfunc()
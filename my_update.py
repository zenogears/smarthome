#!/usr/bin/python3
#! -*- coding: utf8 -*-

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, SmallInteger
from sqlalchemy.sql import select

import datetime
import sys
import Adafruit_DHT
import configparser
import time
import os

truevalues=(
(1, datetime.datetime(2018, 4, 24, 17, 33, 34, 251809), 25, 21),
(2, datetime.datetime(2018, 4, 24, 17, 33, 52, 390558), 25, 21),
(3, datetime.datetime(2018, 4, 24, 17, 37, 3, 777377), 25, 21),
(4, datetime.datetime(2018, 4, 24, 17, 38, 20, 536169), 25, 22),
(5, datetime.datetime(2018, 4, 24, 18, 10, 48, 470586), 25, 22),
(6, datetime.datetime(2018, 4, 24, 18, 10, 52, 659166), 25, 26),
(7, datetime.datetime(2018, 4, 24, 18, 48, 18, 777813), 25, 26),
(8, datetime.datetime(2018, 4, 24, 19, 40, 5, 51589), 25, 29),
(9, datetime.datetime(2018, 4, 24, 20, 0, 2, 741649), 25, 29),
(10, datetime.datetime(2018, 4, 24, 21, 0, 2, 583366), 25, 28),
(11, datetime.datetime(2018, 4, 24, 22, 0, 3, 416127), 24, 27),
(12, datetime.datetime(2018, 4, 24, 23, 0, 3, 251616), 24, 26),
(13, datetime.datetime(2018, 4, 25, 0, 0, 3, 93671), 24, 25),
(14, datetime.datetime(2018, 4, 25, 1, 0, 5, 470913), 24, 24),
(15, datetime.datetime(2018, 4, 25, 2, 0, 3, 320284), 24, 24),
(16, datetime.datetime(2018, 4, 25, 3, 0, 3, 159586), 24, 23),
(17, datetime.datetime(2018, 4, 25, 4, 0, 2, 657265), 24, 23),
(18, datetime.datetime(2018, 4, 25, 5, 0, 2, 504889), 25, 25),
(19, datetime.datetime(2018, 4, 25, 6, 0, 3, 340163), 24, 19),
(20, datetime.datetime(2018, 4, 25, 7, 0, 3, 174083), 24, 17),
(21, datetime.datetime(2018, 4, 25, 8, 0, 3, 27274), 24, 16),
(22, datetime.datetime(2018, 4, 25, 9, 0, 2, 860755), 24, 15),
(23, datetime.datetime(2018, 4, 25, 10, 0, 2, 714239), 24, 15),
(24, datetime.datetime(2018, 4, 25, 11, 0, 2, 538493), 24, 15),
(25, datetime.datetime(2018, 4, 25, 12, 0, 3, 391256), 24, 15),
(26, datetime.datetime(2018, 4, 25, 13, 0, 3, 238829), 25, 15),
(27, datetime.datetime(2018, 4, 25, 14, 0, 3, 103812), 24, 15),
(28, datetime.datetime(2018, 4, 25, 15, 0, 2, 940909), 24, 15),
(29, datetime.datetime(2018, 4, 25, 16, 0, 2, 766438), 24, 15),
(30, datetime.datetime(2018, 4, 25, 17, 0, 2, 606105), 25, 22),
(31, datetime.datetime(2018, 4, 25, 18, 0, 2, 437439), 24, 20),
(32, datetime.datetime(2018, 4, 25, 19, 0, 3, 300328), 25, 28),
(33, datetime.datetime(2018, 4, 25, 20, 0, 3, 134223), 25, 23),
(34, datetime.datetime(2018, 4, 25, 21, 0, 2, 977067), 24, 25),
(35, datetime.datetime(2018, 4, 25, 22, 0, 2, 844281), 24, 27),
(36, datetime.datetime(2018, 4, 25, 23, 0, 2, 695664), 24, 28),
(37, datetime.datetime(2018, 4, 26, 0, 0, 2, 529676), 24, 27),
(38, datetime.datetime(2018, 4, 26, 1, 0, 3, 389178), 24, 29),
(39, datetime.datetime(2018, 4, 26, 2, 0, 3, 217547), 24, 27),
(40, datetime.datetime(2018, 4, 26, 3, 0, 3, 65040), 24, 27),
(41, datetime.datetime(2018, 4, 26, 4, 0, 2, 601022), 24, 27),
(42, datetime.datetime(2018, 4, 26, 5, 0, 3, 450636), 25, 28),
(43, datetime.datetime(2018, 4, 26, 6, 0, 3, 311243), 25, 27),
(44, datetime.datetime(2018, 4, 26, 7, 0, 3, 155455), 25, 25),
(45, datetime.datetime(2018, 4, 26, 8, 0, 3, 10418), 25, 26),
(46, datetime.datetime(2018, 4, 26, 9, 0, 2, 835391), 25, 26),
(47, datetime.datetime(2018, 4, 26, 10, 0, 2, 683100), 25, 25),
(48, datetime.datetime(2018, 4, 26, 11, 0, 2, 522733), 25, 26),
(49, datetime.datetime(2018, 4, 26, 12, 0, 3, 357696), 25, 28),
(50, datetime.datetime(2018, 4, 26, 13, 0, 3, 198042), 25, 28),
(51, datetime.datetime(2018, 4, 26, 14, 0, 3, 42655), 25, 27),
(52, datetime.datetime(2018, 4, 26, 15, 0, 2, 921539), 25, 27),
(53, datetime.datetime(2018, 4, 26, 16, 0, 2, 797140), 25, 28),
(54, datetime.datetime(2018, 4, 26, 17, 0, 2, 631698), 25, 28),
(55, datetime.datetime(2018, 4, 26, 18, 0, 2, 516909), 25, 28),
(56, datetime.datetime(2018, 4, 26, 19, 0, 3, 407245), 25, 28),
(57, datetime.datetime(2018, 4, 26, 19, 0, 56, 503891), 25, 29)
)

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///' + os.path.join(basedir, 'smarthome.db'), echo=True)

config = configparser.RawConfigParser()
config.read("/home/pi/global_config.conf")

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
Temp = Table('Temp', metadata,
        Column('id', Integer, primary_key=True),
        Column('time', DateTime),
        Column('temperature', SmallInteger),
        Column('humidity', SmallInteger),
    )

for i in truevalues:
    ins = Temp.insert().values(i)
    print(ins)
    print(ins.compile().params)

conn = engine.connect()
result = conn.execute(ins)

s = select([Temp])
result = conn.execute(s)

for row in result:
	print(row)

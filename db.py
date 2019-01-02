# -*- coding: utf-8 -*-
import csv
import os
import sqlite3
from io import StringIO

import requests
import mosql.query


ROAD_NAME_URL = ('http://data.moi.gov.tw/MoiOD/System/DownloadFile.aspx?'
                 'DATA=59BB886A-BB02-4821-B071-EDF292F15CCA')
ROAD_NAME_DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')


def db_connect(database_path=ROAD_NAME_DATABASE_PATH):
    conn = sqlite3.connect(database_path)
    return conn


def init_db():
    conn = db_connect()
    cur = conn.cursor()
    sql = """CREATE TABLE road_names (
        id integer PRIMARY KEY AUTOINCREMENT,
        county TEXT NOT NULL,
        city TEXT NOT NULL,
        name TEXT NOT NULL)"""
    cur.execute(sql)
    conn.close()


def insert_road_name(cur, county, city, name):
    sql = mosql.query.insert('road_names',
                             {'county': county,
                              'city': city,
                              'name': name})
    cur.execute(sql)


def insert_all_road_names():
    r = requests.get(ROAD_NAME_URL)
    reader = csv.reader(StringIO(r.text))

    conn = db_connect()
    cur = conn.cursor()
    for r in reader:
        insert_road_name(cur, *r)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    insert_all_road_names()

# -*- coding: utf-8 -*-
import sys

import matplotlib.font_manager as mfm
import matplotlib.pyplot as plt
import mosql.query
from db import db_connect


FONT_PATH = '/usr/share/fonts/adobe-source-han-sans/SourceHanSansTW-Medium.otf'
prop = mfm.FontProperties(fname=FONT_PATH)


def get_all_road_names():
    conn = db_connect()
    cur = conn.cursor()
    sql = mosql.query.select('road_names', {'name like': '%'})
    cur.execute(sql)
    return cur.fetchall()


def search_road(wildcard):
    conn = db_connect()
    cur = conn.cursor()
    sql = mosql.query.select('road_names',
                             {'name like': f'%{wildcard}%'})
    cur.execute(sql)
    print(cur.fetchall())


def search_road_only_how_much(wildcard):
    conn = db_connect()
    cur = conn.cursor()
    sql = mosql.query.select('road_names',
                             {'name like': f'%{wildcard}%'})
    cur.execute(sql)
    return len(cur.fetchall())


if __name__ == '__main__':
    if len(sys.argv[1:]) == 1:
        search_road(sys.argv[1])
    else:
        import n2c
        words = [n2c.num2chinese(i) for i in range(1, 100)]
        d = {w: search_road_only_how_much(w) for w in words}
        plt.bar(d.keys(), d.values())
        plt.xticks(range(len(d.keys())), d.keys(), rotation=45, fontproperties=prop)
        plt.xlabel('搜尋字', fontproperties=prop)
        plt.ylim(0, 2500)
        plt.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22 13:03
# @Author  : GUO Ziyao
import sqlite3

from flask import current_app
from flask import g


def connect_db():
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    return (rv[0] if rv else None) if one else rv

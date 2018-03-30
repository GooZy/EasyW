#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/23 13:22
# @Author  : GUO Ziyao
from blueprint import app

from flask import g


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if error:
        app.logger.error("Teardown error: %s" % error)
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

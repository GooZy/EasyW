#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 08:53
# @Author  : GUO Ziyao
import os

from easyw.common.db import init_db

from flask import Flask
from flask import g

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config['DATABASE'] = os.path.join(app.instance_path, 'easyw.db')
app.config.from_object('config.default')

# If can't find the variable, don't throw exception
app.config.from_envvar('APP_CONFIG_FILE', silent=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

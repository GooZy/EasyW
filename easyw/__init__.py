#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 08:53
# @Author  : GUO Ziyao
import os

from easyw.common.db import init_db

from flask import Flask


app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config['DATABASE'] = os.path.join(app.instance_path, 'easyw.db')
app.config['DATA_DIR'] = os.path.join(app.root_path, 'static', 'data')
app.config.from_object('config.default')

if not os.path.exists(app.config['DATA_DIR']):
    os.makedirs(app.config['DATA_DIR'])

# If can't find the variable, don't throw exception
app.config.from_envvar('APP_CONFIG_FILE', silent=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

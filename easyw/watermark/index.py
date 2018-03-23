#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22 08:54
# @Author  : GUO Ziyao
"""
Homepage
"""
from easyw import app


@app.route('/')
def hello_world():
    return 'Hello, World!'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22 12:58
# @Author  : GUO Ziyao
from . import app
from watermark.index import bp as index_bp
from watermark.views.user import bp as user_bp


app.register_blueprint(index_bp)
app.register_blueprint(user_bp)

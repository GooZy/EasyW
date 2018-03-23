#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/21 13:56
# @Author  : GUO Ziyao
import os

from easyw.bootstrap import app


port = int(os.environ.get('EASYW_PORT', 9715))
app.run(host='0.0.0.0', port=port, debug=True)

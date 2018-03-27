#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22 08:48
# @Author  : GUO Ziyao
"""
Watermark processing
"""
from flask import Blueprint

from flask import render_template

bp = Blueprint('process', __name__)


@bp.route('/lsb_index', methods=['GET', 'POST'])
def lsb_index():
    return render_template('lsb.html')


@bp.route('/dwt_index', methods=['GET', 'POST'])
def dwt_index():
    return render_template('dwt.html')

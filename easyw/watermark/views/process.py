#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22 08:48
# @Author  : GUO Ziyao
"""
Watermark processing
"""
from easyw.watermark.biz.image import ImageBiz

from flask import Blueprint
from flask import render_template
from flask import request

bp = Blueprint('process', __name__)


@bp.route('/lsb_index', methods=['GET', 'POST'])
def lsb_index():
    return render_template('lsb.html')


@bp.route('/api/perform_lsb', methods=['GET', 'POST'])
def perform_lsb():
    cover_image = request.files.get('cover_image')
    watermark = request.files.get('watermark')
    if not cover_image or not watermark:
        return render_template('lsb.html', error='Upload files error!')
    # save files to local path
    cover_image_path = ImageBiz.save_image(cover_image)
    watermark_path = ImageBiz.save_image(watermark)

    result_files = ImageBiz.lets_lsb(cover_image_path, watermark_path)

    return render_template('lsb_result.html', result_files=result_files)


@bp.route('/dwt_index', methods=['GET', 'POST'])
def dwt_index():
    return render_template('dwt.html')

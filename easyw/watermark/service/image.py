#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/27 23:05
# @Author  : GUO Ziyao
from easyw.common.db import query_db


class ImageService(object):

    @classmethod
    def get_all_image(cls, username):
        return query_db('SELECT * FROM images')

    @classmethod
    def add_image(cls, image_path):
        query_db("INSERT INTO images(path) VALUES (?)", [image_path])

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/27 23:05
# @Author  : GUO Ziyao
from easyw.common.db import query_db


class ImageService(object):

    @classmethod
    def get_all_image(cls):
        return query_db('SELECT * FROM images')

    @classmethod
    def get_image_by_path(cls, image_path):
        return query_db('SELECT * FROM images WHERE path = ?', [image_path])

    @classmethod
    def add_image(cls, image_path):
        if not cls.get_image_by_path(image_path):
            query_db("INSERT INTO images(path) VALUES (?)", [image_path])

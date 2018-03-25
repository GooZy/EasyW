#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/25 20:18
# @Author  : GUO Ziyao
from easyw.common.db import query_db
from easyw.common.utils import hash_password


class UserService(object):

    @classmethod
    def get_user_by_name(cls, username):
        return query_db('SELECT * FROM users WHERE username=?', [username])

    @classmethod
    def get_user_by_name_and_password(cls, username, password):
        return query_db('SELECT * FROM users WHERE username=? AND password=?', [username, hash_password(password)])

    @classmethod
    def add_user(cls, username, password):
        query_db("INSERT INTO users(username, password) VALUES (?, ?)", [username, hash_password(password)])

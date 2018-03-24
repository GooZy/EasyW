#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 17:13
# @Author  : GUO Ziyao
import hashlib


def hash_password(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()

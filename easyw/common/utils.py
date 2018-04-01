#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 17:13
# @Author  : GUO Ziyao
import hashlib

import cv2


def hash_password(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()


def show_img(img, title='TEST'):
    cv2.imshow(title, img)
    cv2.waitKey(0)

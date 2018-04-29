#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/24 17:13
# @Author  : GUO Ziyao
import copy
import hashlib

import cv2
import numpy as np


def hash_password(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()


def show_img(img, title='TEST'):
    cv2.imshow(title, img)
    cv2.waitKey(0)


def get_web_path(path):
    return path.replace(path.rsplit('/', 3)[0], '')


def arnold(img, key):
    N, a, b, c, d = key
    h, w = img.shape[: 2]
    new_img = copy.deepcopy(img)
    # 置换N次
    for i in range(N):
        for x in range(h):
            for y in range(w):
                nx = ((a * x + b * y) % w + w) % w
                ny = ((c * x + d * y) % w + w) % w
                nx = int(nx)
                ny = int(ny)
                new_img[nx, ny] = img[x, y]
        img = copy.deepcopy(new_img)
    return new_img


def iarnold(img, key):
    N, a, b, c, d = key
    # 求矩阵逆
    matrix = np.mat([[a, b], [c, d]]).I
    # 精度问题
    [[a, b], [c, d]] = matrix.tolist()
    return arnold(img, [N, a, b, c, d])

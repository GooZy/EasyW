#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 12:48
# @Author  : GUO Ziyao
import cv2

from easyw.common.utils import show_img


cover_image = cv2.imread('/Users/guoziyao/Desktop/cqu.jpg')
watermark = cv2.imread('/Users/guoziyao/Desktop/cqu.png')

# graying & binaryzation
watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
ret, watermark = cv2.threshold(watermark, 0, 255, cv2.THRESH_OTSU)

b_cover_image = cover_image[:, :, 0]

h, w = watermark.shape[: 2]
# init lsb to 0
b_cover_image = b_cover_image & 254
for i in range(h):
    for j in range(w):
        if watermark[i, j] == 255:
            b_cover_image[i, j] = b_cover_image[i, j] | 1
cover_image[:, :, 0] = b_cover_image
cv2.imwrite('x.bmp', cover_image)
cover_image = cv2.imread('x.bmp')
# decode
h, w = cover_image.shape[: 2]
b_cover_image = cover_image[:, :, 0]
for i in range(h):
    for j in range(w):
        if b_cover_image[i, j] & 1:
            b_cover_image[i, j] = 255
        else:
            b_cover_image[i, j] = 0
show_img(b_cover_image, 'DECODE')

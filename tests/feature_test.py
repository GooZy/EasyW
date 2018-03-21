#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 12:48
# @Author  : GUO Ziyao
import cv2

img = cv2.imread('/Users/guoziyao/Desktop/my/EasyW/data/cqu.png')

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('a', gray_img)


ret, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

cv2.imshow('b', binary_img)
cv2.waitKey(0)
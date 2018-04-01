#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 14:10
# @Author  : GUO Ziyao
import os

from easyw import app
from easyw.watermark.service.image import ImageService

import cv2


DIR = os.path.join(app.root_path, 'data')
if not os.path.exists(DIR):
    os.makedirs(DIR)


class ImageBiz(object):

    @classmethod
    def save_image(cls, image, filename=None):
        if not filename:
            filename = image.filename
            image_data = image.read()
            file_path = os.path.join(DIR, filename)
            with open(file_path, 'wb') as f:
                f.write(image_data)
        else:
            file_path = os.path.join(DIR, filename)
            cv2.imwrite(file_path, image)
        ImageService.add_image(file_path)
        return file_path


    @classmethod
    def lsb(cls, cover_image_path, watermark_path):
        cover_image = cv2.imread(cover_image_path)
        watermark = cv2.imread(watermark_path)

        # graying & binaryzation
        watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
        ret, watermark = cv2.threshold(watermark, 0, 255, cv2.THRESH_OTSU)

        # get the blue channel of cover_image
        b_cover_image = cover_image[:, :, 0]
        h, w = watermark.shape[: 2]
        # initial the lsb to 0
        b_cover_image = b_cover_image & 254
        for i in range(h):
            for j in range(w):
                if watermark[i, j] == 255:
                    b_cover_image[i, j] = b_cover_image[i, j] | 1
        cover_image[:, :, 0] = b_cover_image
        return cls.save_image(cover_image, 'easyw_result.jpg')


    @classmethod
    def decode_lsb(cls, image_path):
        image = cv2.imread(image_path)
        h, w = image.shape[: 2]
        b_image = image[:, :, 0]
        for i in range(h):
            for j in range(w):
                if b_image[i, j] & 1:
                    b_image[i, j] = 255
                else:
                    b_image[i, j] = 0
        return cls.save_image(b_image, 'easyw_decode.jpg')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 14:10
# @Author  : GUO Ziyao
import os

from easyw import app
from easyw.common.utils import get_web_path
from easyw.watermark.service.image import ImageService

import cv2
import numpy as np


DIR = app.config['DATA_DIR']


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
    def warp_result(cls, title, path):
        return {
            'title': title,
            'file': get_web_path(path),
            'decode_file': get_web_path(cls.decode_lsb(path))
        }


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
        return cls.save_image(cover_image, 'easyw_result.bmp')


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
        filename = image_path.split('/')[-1].split('.')[0] + '_decode.bmp'
        return cls.save_image(b_image, filename)


    @classmethod
    def lets_lsb(cls, cover_image_path, watermark_path):
        result_files = list()
        path = ImageBiz.lsb(cover_image_path, watermark_path)
        result_files.append(cls.warp_result('Normal', path))
        result_files.extend(cls.attack_image(path))
        return result_files


    @classmethod
    def attack_image(cls, image_path):
        img = cv2.imread(image_path)
        base_file_name = image_path.split('/')[-1].split('.')[0]
        attacks = list()
        # Gaussian Blur
        blur = cv2.GaussianBlur(img, (21, 21), 0)
        path = cls.save_image(blur, base_file_name + '_blur.bmp')
        attacks.append(cls.warp_result('Gaussian Blur', path))
        # Scale
        scale = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        path = cls.save_image(scale, base_file_name + '_scale.bmp')
        attacks.append(cls.warp_result('Scale', path))
        # JPEG
        path = cls.save_image(img, base_file_name + '_jpeg.jpg')
        attacks.append(cls.warp_result('JPEG', path))
        # Rotate
        rows, cols = img.shape[: 2]
        M = cv2.getRotationMatrix2D((int(rows / 2), int(cols / 2)), 90 * 180 / np.pi, 1)
        rotate = cv2.warpAffine(img, M, (rows, cols), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        path = cls.save_image(rotate, base_file_name + '_rotate.bmp')
        attacks.append(cls.warp_result('Rotate', path))
        # Sharpen
        kernel = np.array([0, -1, 0, -1, 5, -1, 0, -1, 0]).reshape((3, 3))
        sharpen = cv2.filter2D(img, img.shape[-1], kernel)
        path = cls.save_image(sharpen, base_file_name + '_sharpen.bmp')
        attacks.append(cls.warp_result('Sharpen', path))
        return attacks

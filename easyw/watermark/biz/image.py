#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/31 14:10
# @Author  : GUO Ziyao
import os

from easyw import app
from easyw.common.utils import get_web_path
from easyw.common.utils import arnold
from easyw.common.utils import iarnold
from easyw.watermark.service.image import ImageService

import cv2
import pywt
import numpy as np


DIR = app.config['DATA_DIR']
SCRAMBLING_KEY = app.config['SCRAMBLING_KEY']
COEFFICIENTS = app.config['COEFFICIENTS']


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
    def warp_result(cls, title, path, which='lsb', cover_image_path=None):
        if which == 'lsb':
            return {
                'title': title,
                'file': get_web_path(path),
                'decode_file': get_web_path(cls.decode_lsb(path))
            }
        else:
            return {
                'title': title,
                'file': get_web_path(path),
                'decode_file': get_web_path(cls.decode_dwt(path, cover_image_path))
            }

    @classmethod
    def lsb(cls, cover_image_path, watermark_path):
        cover_image = cv2.imread(cover_image_path)
        cover_image = cv2.resize(cover_image, (400, 400))
        watermark = cv2.imread(watermark_path)
        watermark = cv2.resize(watermark, (100, 100))

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
    def dwt(cls, cover_image_path, watermark_path):
        image = cv2.imread(cover_image_path, 0)
        watermark = cv2.imread(watermark_path, 0)
        image = cv2.resize(image, (400, 400))
        watermark = cv2.resize(watermark, (100, 100))
        watermark = arnold(watermark, SCRAMBLING_KEY)

        # 对图片三级小波分解
        image = np.float32(image)
        image /= 255
        [cA3, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(image, 'haar', level=3)

        # 对水印一级小波分解
        watermark = np.float32(watermark)
        watermark /= 255
        cA, (cH, cV, cD) = pywt.dwt2(watermark, 'haar')

        # 水印嵌入
        a1, a2, a3, a4 = COEFFICIENTS
        cA3 += a1 * cA
        cH3 += a2 * cH
        cV3 += a3 * cV
        cD3 += a4 * cD

        # 重构原图
        cA2 = pywt.idwt2((cA3, (cH3, cV3, cD3)), 'haar')
        cA1 = pywt.idwt2((cA2, (cH2, cV2, cD2)), 'haar')
        watermarkedImage = pywt.idwt2((cA1, (cH1, cV1, cD1)), 'haar')
        watermarkedImage *= 255
        watermarkedImage = np.uint8(watermarkedImage)
        return cls.save_image(watermarkedImage, 'easyw_dwt_result.bmp')

    @classmethod
    def decode_dwt(cls, image_path, cover_image_path):
        org_img = cv2.imread(cover_image_path, 0)
        org_img = cv2.resize(org_img, (400, 400))
        watermarkedImage = cv2.imread(image_path, 0)[:400, :400]
        a1, a2, a3, a4 = COEFFICIENTS

        # 提取水印
        watermarkedImage = np.float32(watermarkedImage)
        watermarkedImage /= 255
        [cA3, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(watermarkedImage, 'haar', level=3)
        image = np.float32(org_img)
        image /= 255
        [x, (y, z, w), (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(image, 'haar', level=3)

        cA = (cA3 - x) / a1
        cH = (cH3 - y) / a2
        cV = (cV3 - z) / a3
        cD = (cD3 - w) / a4

        extracted = pywt.idwt2((cA, (cH, cV, cD)), 'haar')
        extracted *= 255
        extracted = np.uint8(extracted)
        extracted = iarnold(extracted, SCRAMBLING_KEY)
        filename = image_path.split('/')[-1].split('.')[0] + '_decode.bmp'
        return cls.save_image(extracted, filename)

    @classmethod
    def lets_dwt(cls, cover_image_path, watermark_path):
        result_files = list()
        path = ImageBiz.dwt(cover_image_path, watermark_path)
        result_files.append(cls.warp_result('Normal', path, which='dwt', cover_image_path=cover_image_path))
        result_files.extend(cls.attack_image(path, which='dwt', cover_image_path=cover_image_path))
        return result_files

    @classmethod
    def attack_image(cls, image_path, which='lsb', cover_image_path=None):
        img = cv2.imread(image_path)
        base_file_name = image_path.split('/')[-1].split('.')[0]
        attacks = list()
        # Gaussian Blur
        blur = cv2.GaussianBlur(img, (15, 15), 0)
        path = cls.save_image(blur, base_file_name + '_blur.bmp')
        attacks.append(cls.warp_result('Gaussian Blur', path, which=which, cover_image_path=cover_image_path))
        # Scale
        scale = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        scale = cv2.resize(scale, None, fx=2.0/3.0, fy=2.0/3.0, interpolation=cv2.INTER_CUBIC)
        path = cls.save_image(scale, base_file_name + '_scale.bmp')
        attacks.append(cls.warp_result('Scale', path, which=which, cover_image_path=cover_image_path))
        # JPEG
        path = cls.save_image(img, base_file_name + '_jpeg.jpg')
        attacks.append(cls.warp_result('JPEG', path, which=which, cover_image_path=cover_image_path))
        # Rotate
        rows, cols = img.shape[: 2]
        M = cv2.getRotationMatrix2D((int(rows / 2), int(cols / 2)), 30, 1)
        rotate = cv2.warpAffine(img, M, (rows, cols), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        M = cv2.getRotationMatrix2D((int(rows / 2), int(cols / 2)), -30, 1)
        rotate = cv2.warpAffine(rotate, M, (rows, cols), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        path = cls.save_image(rotate, base_file_name + '_rotate.bmp')
        attacks.append(cls.warp_result('Rotate', path, which=which, cover_image_path=cover_image_path))
        # Sharpen
        kernel = np.array([0, -1, 0, -1, 5, -1, 0, -1, 0]).reshape((3, 3))
        sharpen = cv2.filter2D(img, img.shape[-1], kernel)
        path = cls.save_image(sharpen, base_file_name + '_sharpen.bmp')
        attacks.append(cls.warp_result('Sharpen', path, which=which, cover_image_path=cover_image_path))
        # Noise
        for i in range(2000):  # 添加点噪声
            temp_x = np.random.randint(0, img.shape[0])
            temp_y = np.random.randint(0, img.shape[1])
            img[temp_x][temp_y] = 255
        path = cls.save_image(img, base_file_name + '_noise.bmp')
        attacks.append(cls.warp_result('Noise', path, which=which, cover_image_path=cover_image_path))
        return attacks

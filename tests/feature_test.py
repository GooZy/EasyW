#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 12:48
# @Author  : GUO Ziyao
import cv2
import pywt
import numpy as np
import matplotlib.pyplot as plt

from easyw.common.utils import show_img
from easyw.common.utils import arnold
from easyw.common.utils import iarnold
from config.default import SCRAMBLING_KEY


def test_lsb():
    cover_image = cv2.imread('/Users/guoziyao/Desktop/lena.jpg')
    org_image = cover_image
    watermark = cv2.imread('/Users/guoziyao/Desktop/cqu.jpg')
    org_watermark = watermark

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
    # 显示LSB嵌入结果
    # fig = plt.figure('Result')
    # ax = fig.add_subplot(121)
    # b, g, r = cv2.split(org_image)
    # org_image = cv2.merge([r, g, b])
    # ax.imshow(org_image)
    # ax.set_title('Before')
    # ax.axis('off')  # 关闭坐标轴显示
    # ax = fig.add_subplot(122)
    # b, g, r = cv2.split(cover_image)
    # cover_image = cv2.merge([r, g, b])
    # ax.imshow(cover_image)
    # ax.set_title('After')
    # ax.axis('off')  # 关闭坐标轴显示
    # plt.show()

    # decode
    h, w = cover_image.shape[: 2]
    b_cover_image = cover_image[:, :, 0]
    for i in range(h):
        for j in range(w):
            if b_cover_image[i, j] & 1:
                b_cover_image[i, j] = 255
            else:
                b_cover_image[i, j] = 0
    # show_img(b_cover_image, 'DECODE')
    # 显示LSB解码结果
    fig = plt.figure('Result')
    ax = fig.add_subplot(121)
    b, g, r = cv2.split(org_watermark)
    org_watermark = cv2.merge([r, g, b])
    ax.imshow(org_watermark)
    ax.set_title('Origin')
    ax.axis('off')  # 关闭坐标轴显示
    ax = fig.add_subplot(122)
    ax.imshow(b_cover_image, cmap='gray')
    ax.set_title('Extraction')
    ax.axis('off')  # 关闭坐标轴显示
    plt.show()


def test_dwt():
    image = cv2.imread('/Users/guoziyao/Desktop/lena.jpg', 0)
    watermark = cv2.imread('/Users/guoziyao/Desktop/cqu.jpg', 0)
    image = cv2.resize(image, (400, 400))
    cv2.imshow('Cover Image', image)
    watermark = cv2.resize(watermark, (100, 100))
    watermark = arnold(watermark, SCRAMBLING_KEY)
    cv2.imshow('Watermark Image', watermark)
    org_img = image

    # 对图片三级小波分解
    image = np.float32(image)
    image /= 255
    [cA3, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = pywt.wavedec2(image, 'haar', level=3)

    # 对水印一级小波分解
    watermark = np.float32(watermark)
    watermark /= 255
    cA, (cH, cV, cD) = pywt.dwt2(watermark, 'haar')

    # 水印嵌入
    a1, a2, a3, a4 = 0.2, 0.1, 0.1, 0.1
    cA3 += a1 * cA
    cH3 += a2 * cH
    cV3 += a3 * cV
    cD3 += a4 * cD

    # 重构原图
    cA2 = pywt.idwt2((cA3, (cH3, cV3, cD3)), 'haar')
    cA1 = pywt.idwt2((cA2, (cH2, cV2, cD2)), 'haar')
    watermarkedImage = pywt.idwt2((cA1, (cH1, cV1, cD1)), 'haar')
    show_img(watermarkedImage)

    # 提取水印
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
    show_img(extracted, 'Extracted')


def get_bit_image(image, bit):
    value = 255 ^ (1 << bit)
    image = np.uint8(image) & value
    return image


def test_lena_bit():
    """
    显示位面测试结果
    """
    image = cv2.imread('/Users/guoziyao/Desktop/lena.jpg', 0)
    tests = list()
    tests.append((image, 'Origin'))
    for i in range(8):
        tests.append((get_bit_image(image, i), 'The %s bit' % i))
    fig = plt.figure('Result')
    for index, each in enumerate(tests):
        ax = fig.add_subplot(int('33' + str(index + 1)))
        ax.imshow(each[0], cmap='gray')
        ax.set_title(each[1])
        ax.axis('off')  # 关闭坐标轴显示
    plt.show()


if __name__ == '__main__':
    test_lsb()
    # test_dwt()
    # test_lena_bit()

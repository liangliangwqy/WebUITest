#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:TangLiang

from PIL import Image
from PIL import ImageChops


def compare_images(path_one, path_two, diff_save_location):
    # 比较图片，如果有不同则生成展示不同的图片
    image_one = Image.open(path_one).resize((540, 1155)).convert('RGB')
    image_two = Image.open(path_two).resize((540, 1155)).convert('RGB')
    diff1 = ImageChops.difference(image_one, image_two)
    new_img = Image.new('RGB', diff1.size, (255, 255, 255))
    diff = ImageChops.difference(new_img, diff1)

    if diff1.getbbox() is None:
        # 图片间没有任何不同则直接退出
        print('测试通过，页面完全相同。')
    else:
        print('开始保存图片')
        diff.save(diff_save_location,"JPEG")
        print('测试不通过，页面有差异，差异文件已保存到：'+diff_save_location)


if __name__ == '__main__':
    path_one='../images/rn.png'
    path_two='../images/h5.png'
    compare_images(path_one, path_two, '../images/')

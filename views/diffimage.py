#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 

from PIL import Image
from PIL import ImageChops
import os

def compare_images(path_one,path_two,diff_save_location):
    #比较图片，如果有不同则生成展示不同的图片
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    diff = ImageChops.difference(image_one, image_two)

    if diff.getbbox() is None:
        # 图片间没有任何不同则直接退出
        print('测试通过，页面完全相同')
    else:
        diff.save(diff_save_location)
        print('测试不通过，页面有差异，差异文件已保存到：'+diff_save_location)



if __name__ == '__main__':
    compare_images(r'C:\Users\Tony\Python\WebTest\projects\bbs.meizu.cn\baseimages\bbs.meizu.cn_base.png',
                   r'C:\Users\Tony\Python\WebTest\projects\bbs.meizu.cn\newimages\bbs.meizu.cn_base.png',
                   r'C:\Users\Tony\Python\WebTest\projects\bbs.meizu.cn\diffimages\bbs.meizu.cn_base.png')

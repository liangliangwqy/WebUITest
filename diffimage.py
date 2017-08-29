#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 

from PIL import Image
from PIL import ImageChops 
import capture
import gui.gui
#获取页面截图
website=gui.gui.app.difff
#    input('请输入需要获取页面截图的网址：')
capture.capture('http://'+website)

def compare_images(path_one, path_two, diff_save_location):
    """
    比较图片，如果有不同则生成展示不同的图片

    @参数一: path_one: 第一张图片的路径(测试目标)
    @参数二: path_two: 第二张图片的路径(基准图片)
    @参数三: diff_save_location: 不同图的保存路径
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)

    diff = ImageChops.difference(image_one, image_two)

    if diff.getbbox() is None:
        # 图片间没有任何不同则直接退出
        print('测试通过，页面完全相同') 
        diff.save(diff_save_location)
        diff.show()
        return
    else:
        diff.save(diff_save_location)
        diff.show()

if __name__ == '__main__':
    compare_images('C:\\Users\\Tony\\Python\\WebTest\\base\\base-www.png',
                   'C:\\Users\\Tony\\Python\\WebTest\\shot-now.png',
                   'C:\\Users\\Tony\\Python\\WebTest\\result.png')


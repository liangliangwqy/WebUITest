#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#参考程序：http://www.cnblogs.com/sparkling-ly/p/5466644.html
from selenium import webdriver
import os
import time
from PIL import Image
import getsave_fn

#本方法用于chrome和edge浏览器获取网页的长截图
def chrome_capture(url,savepath='baseimages',whichbrowser='Chrome'):
    """chrome截屏
    url- 要截屏的url
    pix_w- 窗口宽
    pix_h- 窗口高
    filename-生成截图的文件名
    """
    global real_scroll_h
    global image_pix_h
    pix_h=800#定义页面每次滚动的高度
    image_pix_h = pix_h#分图片的高度等于每次滚动的高度
    if whichbrowser=='Chrome':
        pix_w=1947-26
        driver = webdriver.Chrome()
        driver.set_window_size(pix_w, pix_h + 85 + 47)  # 原来是89，猜测为浏览器头的高度，实测是85,47是被自动化软件控制的通知条的高度
    elif whichbrowser=='Edge':
        pix_w = 1947 - 32
        driver = webdriver.Edge()
        driver.set_window_size(pix_w, pix_h + 84)  # Edge浏览器的头高度为76,但实际截图时发现84可得到完美的图片
        print('pix_w:', pix_w)
    elif whichbrowser=='Firefox':
        pix_w = 1947 - 32
        driver = webdriver.Firefox()
        driver.set_window_size(pix_w, pix_h+109)#Firefox的浏览器头高为109，实际截图时发现**可得到完美的图片
        print('pix_w:', pix_w)
    else:#IE11
        pix_w = 1947-32
        driver = webdriver.Ie()
        driver.set_window_size(pix_w, pix_h+55+7)  # IE浏览器的头高度为55,但实际截图时发现84可得到完美的图片(793),使用QQ截图时，自动捕获的浏览器窗口和此处设置的x、y值完全相同，但是实际测量窗口高度是少了7个像素，不知为何有7个像素的高度不可见。
        print('pix_w:',pix_w)

    driver.get('http://'+url)
    time.sleep(2)
    img_list = []
    i = 0
    last_t=0
    while i < 20:
        #滚动到指定位置并等待1s
        print('滚动前whichbrowser的值：',whichbrowser)
        if whichbrowser=='Chrome' or whichbrowser=='Firefox' or whichbrowser=='IE':
            js_chrome="document.documentElement.scrollTop="+str(i * pix_h)#在chrome上工作良好
            driver.execute_script(js_chrome)
            time.sleep(2)
            # 通过js获取当前页面的总长度和滚动条目前所在的位置
            js_chrome_scroll = "return document.body.scrollHeight.toString()+','+document.documentElement.scrollTop"  # chrome
            js1_result = driver.execute_script(js_chrome_scroll)
        elif whichbrowser=='Edge':
            js_edge="document.body.scrollTop="+str(i * pix_h)
            driver.execute_script(js_edge)
            time.sleep(2)
            # 通过js获取当前页面的总长度和滚动条目前所在的位置
            js_edge_scroll = "return document.body.scrollHeight.toString()+','+document.body.scrollTop.toString()"#Edge
            js1_result = driver.execute_script(js_edge_scroll)

        print('js1_result:'+js1_result)
        real_scroll_h, real_top = js1_result.split(',')[0], js1_result.split(',')[1]
        # real_scroll_h, real_top 是当前滚动条长度和当前滚动条的top，作为是否继续执行的依据，由于存在滚动条向下拉动后会加载新内容的情况，所以需要以下的判断
        #real_scroll_h可以看做是页面的总长度，real_top是目前滚动条(看做一个点)所在的位置。
        # 如果这次设置的top成功，则继续滚屏
        if real_top == str(i * pix_h):
            i += 1
            print('存储图片名：''.\\cache-' + str(i) + '.png')
            driver.save_screenshot('.\\cache-'+ str(i) + '.png')#获取当前页面的截图
            img_list.append('.\\cache-'+ str(i) + '.png')#把当前页面的截图文件名存入数组
            last_t = real_top
            print('当前滚动条位置'+real_top)
        else:
            # 如果本次设置失败，看这次的top和上一次记录的top值是否相等，相等则说明没有新加载内容，且已到页面底，跳出循环
            if real_top != last_t:
                last_t = real_top
            else:
                driver.save_screenshot('.\\cache-' + str(i + 1) + '.png')
                img_list.append('.\\cache-' + str(i + 1) + '.png')
                break
    driver.close()
    # 生成图片的文件名
    save_fn = getsave_fn.save_fn(url, savepath, whichbrowser)
    print('save_fn in chromecapture:' + save_fn)
    image_merge(img_list,save_fn,whichbrowser)


def image_merge(images,save_fn,whichbrowser):
    """垂直合并多张图片
    images - 要合并的图片路径列表
    ouput_dir - 输出路径
    output_name - 输出文件名
    """

    max_width = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > max_width:
                max_width = width
                print('max_width:',max_width)
    total_height=int(real_scroll_h)
    print('total_height:',total_height)


    # 产生一张空白图
    new_img = Image.new('RGB', (max_width, total_height), 255)

    # 合并
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            new_img.paste(img, (x, y))
            if y <= total_height-2*image_pix_h:
                y += height
            else:
                y = total_height-image_pix_h  # 最后一次滚动高度不足一屏时，图片有部分重合，以底部为准

    if whichbrowser=='Chrome':
        bounds=(0,0,new_img.size[0]-18,new_img.size[1])
        last_img=new_img.crop(bounds)
        last_img.save(save_fn)
    else:
        bounds = (0, 0, new_img.size[0] - 12, new_img.size[1])
        last_img = new_img.crop(bounds)
        last_img.save(save_fn)

    print('图片合成已完成')
    #需要在此处加入裁切图片的步骤，裁掉右侧宽为7个像素的滚动条
    for img_path in images:
        os.remove(img_path)
        print('缓存分页图片已删除',img_path)
    return save_fn


if __name__=='__main__':
    chrome_capture('www.meizu.com/pro7', savepath='newimages',whichbrowser='Edge')
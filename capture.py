#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import os,re,sys
import chromecapture
import getsave_fn
#python版selenium安装命令：sudo easy_install selenium
from selenium import webdriver
import urllib3
#PIL 模块安装命令：pip install pillow
from PIL import Image

#本方法用于firefox和IE11浏览器获取网页的长截图
def capture(url,savepath='baseimages',whichbrowser='IE'):
    #生成图片的文件名
    save_fn=getsave_fn.save_fn(url,savepath,whichbrowser)
    #调用webdriver获取页面截图
    if whichbrowser=='IE':
        browser = webdriver.Ie()  # Get local session of browser
        print('IE')
    else:
        browser = webdriver.Firefox()
    #把浏览器窗口设置的很高，可以在firefox和IE11（不使用这种方法也可以）上获取整个网页的截图，Chrome和Edge不行。
    browser.get('http://'+url)  # Load page
    js= "return document.body.scrollHeight.toString()"
    highpx=browser.execute_script(js)
    print('highpx',highpx)
    if whichbrowser == 'IE':
        browser.set_window_size(1920,int(highpx)+116)
    else:
        browser.set_window_size(1920-21, int(highpx) + 116)
    # 添加js脚本，使页面滚动到最后，以便加载完所有元素。
    browser.execute_script("""
    (function () {
      var y = 0;
      var step = 100;
      window.scroll(0, 0);

      function f() {
        if (y < document.body.scrollHeight) {
          y += step;
          window.scroll(0, y);
          setTimeout(f, 50);
        } else {
          window.scroll(0, 0);
          document.title += "scroll-done";
        }
      }

      setTimeout(f, 1000);
    })();
  """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(2)
    print('准备保存')
    browser.save_screenshot(save_fn)
    image=Image.open(save_fn)
    image_rgb=image.convert("RGB")#因为webdriver默认保存的图片是RGBA格式的，但是Image只能处理RGB格式的图片。
    image_rgb.save(save_fn)#转换之后需要保存一下
    print('保存为RGB格式成功！')
    browser.close()
    image.close()


if __name__ == "__main__":
    capture("www.meizu.com/index.html",savepath='newimages',whichbrowser='Firefox')
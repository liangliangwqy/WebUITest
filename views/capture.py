#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import os,re
from selenium import webdriver
import urllib3
from PIL import Image

def capture(url,savepath='baseimages'):
    #获取url的域名
    protocol,host,a=urllib3.get_host(url)
    print('url:' + url)
    #去掉url的前缀
    urlpath1,num1=re.subn(r'://','_',url)
    #把url里面的点替换成下划线
    urlpath,num2=re.subn(r'\/','_',urlpath1)
    print('urlpath:'+urlpath)

    #保存原图的路径
    save_fnpath = os.path.abspath('..') + '\\projects\\' +host+'\\'+savepath
    if not os.path.exists(save_fnpath):
        os.makedirs(save_fnpath)
    save_fn=save_fnpath+'\\'+urlpath+'_base.png'
    print('save_fn:'+save_fn)

    #调用webdriver获取页面截图
    browser = webdriver.Ie()  # Get local session of browser
    browser.set_window_size(1920, 1080)
    browser.get('http://'+url)  # Load page

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
        time.sleep(5)
    print('准备保存')
    browser.save_screenshot(save_fn)
    image=Image.open(save_fn)
    image_rgb=image.convert("RGB")#因为webdriver默认保存的图片是RGBA格式的，但是Image只能处理RGB格式的图片。
    image_rgb.save(save_fn)#转换之后需要保存一下
    print('保存为RGB格式成功！')
    browser.close()
    image.close()


if __name__ == "__main__":
    capture("bbs.meizu.cn")
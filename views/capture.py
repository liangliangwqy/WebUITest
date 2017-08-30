#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import os,re
from selenium import webdriver
import urllib3


def capture(url, save_fn='.\\shot-now.png'):

    #获取url的域名
    protocol,host,a=urllib3.get_host(url)

    #去掉url的前缀
    urlpath1,num1=re.subn(r'://','_',url)
    #把url里面的点替换成下划线
    urlpath,num2=re.subn(r'\/','_',urlpath1)
    print(urlpath)
    #保存原图的路径
    save_fnpath = os.path.abspath('..') + '\\projects\\' +host+'\\baseimages'
    if not os.path.exists(save_fnpath):
        os.makedirs(save_fnpath)
    save_fn=save_fnpath+'\\'+urlpath+'_base.png'
    print(save_fn)

    #调用webdriver获取页面截图
    browser = webdriver.Ie()  # Get local session of browser
    browser.set_window_size(1920, 1080)
    browser.get(url)  # Load page
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

    browser.save_screenshot(save_fn)
    browser.close()


if __name__ == "__main__":
    capture("https://www.meizu.com/products/pro6plus/summary.html")
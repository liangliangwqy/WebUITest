#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:TangLiang

import time
from webuitest import getsave_fn
from selenium import webdriver  # python版selenium安装命令：sudo easy_install selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image  # PIL 模块安装命令：pip install pillow


# 本方法用于IE系列浏览器获取网页的长截图
def capture(url, screen_pix_w, savepath='baseimages', whichbrowser='IE', whereisbrowser='local'):
    # 生成图片的文件名
    save_fn = getsave_fn.save_fn(url, savepath, whichbrowser)
    # 调用webdriver获取页面截图
    if whereisbrowser == 'local':
        browser = webdriver.Ie()
        browser.get('http://' + url)
        version = browser.capabilities['version']
        print('本地IE浏览器的版本是:', version)
    elif whichbrowser == 'IE 8':
        # browser = webdriver.Remote(command_executor='http://172.16.180.21:4010/wd/hub',desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        browser = webdriver.Remote(command_executor='http://172.16.180.108:4444/wd/hub',
                                   desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        print('正在调取http://172.16.180.108:4444/wd/hub上的远程IE8')
    elif whichbrowser == 'IE 9':
        # browser = webdriver.Remote(command_executor='http://172.16.180.22:4010/wd/hub',desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        browser = webdriver.Remote(command_executor='http://172.16.180.109:4444/wd/hub',
                                   desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        print('正在调取http://172.16.180.109:4444/wd/hub上的远程IE 9')
    elif whichbrowser == 'IE 10':
        browser = webdriver.Remote(command_executor='http://172.16.180.110:4444/wd/hub',
                                   desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        print('正在调取http://172.16.180.110:4444/wd/hub上的远程IE 10')
    elif whichbrowser == 'IE 11':
        browser = webdriver.Remote(command_executor='http://172.16.180.112:4444/wd/hub',
                                   desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        print('正在调取http://172.16.180.112:4444/wd/hub上的远程IE 11')
    else:
        print('您选择的浏览器不被支持，默认调取本地IE浏览器进行测试')
        browser = webdriver.Ie()
    # 把浏览器窗口设置的很高，可以在firefox和IE11（不使用这种方法也可以）上获取整个网页的截图，Chrome和Edge不行。
    browser.get('http://' + url)  # Load page
    highpx = 800
    if whichbrowser == 'IE 8':
        if whereisbrowser == 'local':
            browser.set_window_size(screen_pix_w + 5, highpx + 116)
        else:
            browser.set_window_size(screen_pix_w + 9, highpx + 116)  # IE浏览器默认可以获取整个页面的截图
        print('正在设置 IE 8的窗口大小')
    elif whichbrowser == 'IE 9':
        browser.set_window_size(screen_pix_w + 5, highpx + 116)  # IE浏览器默认可以获取整个页面的截图
        print('正在设置 IE 9的窗口大小')
    elif whichbrowser == 'IE 10':
        browser.set_window_size(screen_pix_w + 5, highpx + 116)  # IE浏览器默认可以获取整个页面的截图
        print('正在设置 IE 10的窗口大小')
    elif whichbrowser == 'IE 11':
        browser.set_window_size(screen_pix_w + 5, highpx + 116)  # IE浏览器默认可以获取整个页面的截图
        print('正在设置 IE 11的窗口大小')
    else:
        browser.set_window_size(screen_pix_w - 16, highpx + 116)  # Firefox需要把窗口设置成和整个页面一样大，才能获取整个页面的截图
        time.sleep(5)
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
    print('正在存储完整页面截图')
    browser.save_screenshot(save_fn)
    image = Image.open(save_fn)
    image_rgb = image.convert("RGB")  # 因为webdriver默认保存的图片是RGBA格式的，但是Image只能处理RGB格式的图片。
    image_rgb.save(save_fn)  # 转换之后需要保存一下
    print('保存为RGB格式成功！')
    browser.quit()  # 在关闭driver时用Driver.Quit();不要用Driver.Close();
    image.close()


if __name__ == "__main__":
    # capture("www.meizu.com/pro7/index.html", screen_pix_w=1920, savepath='newimages', whichbrowser='IE 8',whereisbrowser='remote')
    # capture("www.meizu.com/pro7/index.html", screen_pix_w=1920, savepath='newimages', whichbrowser='IE 9',whereisbrowser='remote')
    # capture("www.meizu.com/pro7/index.html", screen_pix_w=1920, savepath='newimages', whichbrowser='IE 10',whereisbrowser='remote')
    capture("www.meizu.com/pro7/index.html", screen_pix_w=1920, savepath='newimages', whichbrowser='IE 11',
            whereisbrowser='remote')

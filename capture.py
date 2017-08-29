#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
from selenium import webdriver

def capture(url, save_fn=".\\shot-now.png"):
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
    capture("http://www.meizu.com/pro7")
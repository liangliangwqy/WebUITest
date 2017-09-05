v0.9
基本功能已经实现。
-------------------------
运行环境：
本程序的运行依赖Python3.6，wget 1.19.1，webdriver

目前www.meizu.com有以下几个页面因动画时间过长导致截图不清晰
https://www.meizu.com/products/meilannote5/summary.html
https://www.meizu.com/accessory/a20.html
https://www.meizu.com/products/pro6plus/summary.html

发现问题：
1.从www.flyme.cn采集到www.flyme.cn/tutorial/index.html。但是无法打开。
从百度搜索上面的网址可以看到flyme论坛多次提到这个地址，但是目前只能打开www.flyme.cn/tutorial/
2.在批量获取页面时，www.flyme.cn/firmwarelist-133.html页面出错，但是手动测试未发现问题，目前已替换成正常的图片。
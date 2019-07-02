#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:TangLiang
import urllib3
import re
import os


# TODO(Tony):在V1.6版本中修改路径的组合方式，兼容windows和linux系统
def save_fn(url, savepath='baseimages', whichbrowser='IE'):
    protocol, host, a = urllib3.get_host(url)
    print('正在获取截图的url:' + url)
    # 去掉url的前缀
    urlpath1, num1 = re.subn(r'://', '_', url)
    # 把url里面的点替换成下划线
    urlpath, num2 = re.subn(r'\/', '_', urlpath1)
    # 保存图片的路径
    if savepath == 'baseimages':
        save_fnpath = os.path.abspath('.') + '\\projects\\' + host + '\\' + savepath
    else:
        save_fnpath = os.path.abspath('.') + '\\projects\\' + host + '\\' + savepath + '\\' + whichbrowser
    if not os.path.exists(save_fnpath):
        os.makedirs(save_fnpath)
        # print("保存图片的路径：",save_fnpath)
    save_fn = save_fnpath + '\\' + urlpath + '.png'
    print('生成的图片文件存储在:' + save_fn)
    return save_fn


if __name__ == "__main__":
    save_fn("www.meizu.com/pro7", whichbrowser='Edge')

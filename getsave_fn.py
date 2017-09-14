#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import urllib3
import re,os
def save_fn(url,savepath='baseimages',whichbrowser='IE'):
    protocol,host,a=urllib3.get_host(url)
    print('url:' + url)
    #去掉url的前缀
    urlpath1,num1=re.subn(r'://','_',url)
    #把url里面的点替换成下划线
    urlpath,num2=re.subn(r'\/','_',urlpath1)
    print('urlpath:'+urlpath)

    #保存原图的路径
    if savepath=='baseimages':
        save_fnpath = os.path.abspath('.') + '\\projects\\' +host+'\\'+savepath
    else:
        save_fnpath = os.path.abspath('.') + '\\projects\\' + host + '\\' + savepath+'\\'+whichbrowser
    if not os.path.exists(save_fnpath):
        os.makedirs(save_fnpath)
        print("生成路径：",save_fnpath)
    save_fn=save_fnpath+'\\'+urlpath+'.png'
    print('save_fn:'+save_fn)
    return save_fn

if __name__ == "__main__":
    save_fn("www.meizu.com/pro7",whichbrowser='Edge')
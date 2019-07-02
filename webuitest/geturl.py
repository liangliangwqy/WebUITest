#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:TangLiang
# 本程序从网上获取关键的获取网站链接部分代码，地址：http://blog.csdn.net/hitwangpeng/article/details/47952479
# TODO(Tony):在V1.4版本中修改获取连接的实现方式，使用纯Python实现，避免不同用户需要安装wget的问题
import os
import re

# import shutil

REJECT_FILETYPE = 'rar,7z,css,js,jpg,jpeg,gif,bmp,png,swf,exe'  # 定义爬虫过程中不下载的文件类型


def getinfo(webaddress):
    global REJECT_FILETYPE

    url = 'http://' + webaddress + '/'  # 补充协议获得完整的url
    print('正在抓取>>>>> ' + url)  # 提示表示正在抓取网站

    # 判断项目目录是否存在，如果不存在就创建项目目录
    projectpath = os.path.abspath('.') + '\\projects\\' + webaddress
    if not os.path.exists(projectpath):
        os.makedirs(projectpath)
    print(webaddress + '的项目目录是：' + projectpath + '\\')
    '''
    #定义下载的网页文件存放目录
    websitefilepath=projectpath+'\\websitefile'
    print(webaddress+'页面文件目录是:'+websitefilepath)

    if  os.path.exists(websitefilepath):#如果此文件夹已经存在就将其删除，因为它存在时爬虫将不成功
        print('here')
        shutil.rmtree(websitefilepath)#shutil.rmtree函数用于删除文件夹及其中的文件
        os.makedirs(websitefilepath)#删除后重新生成该文件夹
    else:
        os.makedirs(websitefilepath)  #生成该文件夹
        print('文件夹已生成')
    '''
    outputfilepath = os.path.abspath('.') + '\\projects\\' + webaddress + '\\output.txt'  # 在项目文件夹下创建一个过渡性质的文件output.txt

    print('正在生成连接信息过渡文件：' + outputfilepath)
    fobj = open(outputfilepath, 'w+')
    command = 'wget -r -m -nv --reject=' + REJECT_FILETYPE + ' -o ' + outputfilepath + ' ' + url  # 利用wget命令爬取网站
    print('正在执行命令:', command)
    tmp0 = os.popen(command).readlines()  # 函数os.popen执行命令并且将运行结果存储在变量tmp0中

    # noinspection PyTypeChecker
    print(tmp0, file=fobj)
    allinfo = fobj.read()
    target_url = re.compile(r'\".*?\"', re.DOTALL).findall(allinfo)  # 通过正则表达式筛选出得到的网址
    target_num = len(target_url)
    fobj1 = open(projectpath + '\\' + webaddress + '.txt', 'w')  # 在本目录下创建一个txt文件，里面存储最终得到的内容
    for i in range(target_num):
        # noinspection PyTypeChecker
        print(target_url[i][1:-1], file=fobj1)
    fobj.close()
    fobj1.close()
    if os.path.exists(outputfilepath):  # 将过渡文件output.txt删除
        os.remove(outputfilepath)  # os.remove用于删除文件
        print('已经获取到本站点的所有连接，如有需要请到以下位置查看或修改：', projectpath + '\\' + webaddress + '.txt')


if __name__ == "__main__":
    webaddress = input("请输入网址(不需要前缀 \"http://\"):")
    getinfo(webaddress)
    print("Well Done.")  # 代码执行完毕之后打印此提示信息

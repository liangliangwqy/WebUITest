#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from tkinter import *

import capture
import diffimage
import geturl,chromecapture


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #测试网址输入框的标题
        self.websiteLabel=Label(self,text="测试网址：").grid(row=0,column=0)

        #测试网址域名输入框
        self.websiteEntry = Entry(self)
        self.websiteEntry.grid(row=0, column=1)

        #获取站点所有url按键
        self.geturlButton=Button(self,text="1.获取所有连接",command=self.getwebsiteurl)
        self.geturlButton.grid(row=0,column=2)
        #获取原始图片的功能按键
        self.website1 = Button(self, text="2.获取基准图片", command=lambda :self.getimage(path='baseimages'))
        self.website1.grid(row=3, column=0)



        global choosebrowser
        choosebrowser = StringVar()

        #选择浏览器

        self.ChromeRadioButtom = Radiobutton(self, text='Chrome',variable=choosebrowser, value='Chrome')
        self.ChromeRadioButtom.grid(row=2, column=0)
        self.IERadioButtom=Radiobutton(self,text='Edge',variable=choosebrowser,value='Edge')
        self.IERadioButtom.grid(row=2,column=1)
        self.FirefoxRadioButtom = Radiobutton(self, text='Firefox',variable=choosebrowser, value='Firefox')
        self.FirefoxRadioButtom.grid(row=2, column=2)
        self.IERadioButtom=Radiobutton(self,text='IE',variable=choosebrowser,value='IE')
        self.IERadioButtom.grid(row=2,column=3)
        self.TipsLabel = Label(self, text="选择一个浏览器用于2、3、4操作：")
        self.TipsLabel.grid(row=1, column=1)
        #使用选择的浏览器获取新图
        self.website1 = Button(self, text="3.获取新图", command=lambda :self.getimage(path='newimages'))
        self.website1.grid(row=3, column=1)


        #比较图片的功能按键
        self.diffButton=Button(self,text="4.比较图片",command=self.diff)
        self.diffButton.grid(row=3,column=2)

        #退出程序的按钮
        self.quitButton = Button(self, text='退出程序', command=self.quit)
        self.quitButton.grid(row=4,column=1)

    # 获得被测网站的所有页面连接
    def getwebsiteurl(self):
        website = self.websiteEntry.get()
        print('正在获取' + website + '的所有连接...')
        geturl.getinfo(website)

    #获取所有页面原始截图
    def getoriginimage(self):
        website = self.websiteEntry.get()
        whichbrowser = choosebrowser.get()
        print('正在获取' + website + '的所有页面截图...')
        url=open(os.path.abspath('.')+'\\projects\\'+website+'\\'+website+'.txt')
        for line in url:
            #对所有页面连接生成截图
            print('正在获取' +line,end=''+ '的页面截图...')
            capture.capture(line[:-1], 'baseimages', whichbrowser)#因为每行结尾都是换行符，用[:-1]的方法读取最后一位之前的内容
            print('原图获取完成！')


    #-获取页面的当前截图
    def getimage(self,path='newimages'):
        whichbrowser=choosebrowser.get()
        print('whichbrowser:',whichbrowser)
        website = self.websiteEntry.get()
        url = open(os.path.abspath('.') + '\\projects\\' + website + '\\' + website + '.txt')
        for line in url:
            # 对所有页面连接生成截图
            print('正在获取' + line, end='' + '的页面截图...')
            if whichbrowser=='IE':
                capture.capture(line[:-1], path, whichbrowser)  # 因为每行结尾都是换行符，用[:-1]的方法读取最后一位之前的内容
                print('IE')
            elif whichbrowser=='Firefox':
                capture.capture(line[:-1], path, whichbrowser)  # 因为每行结尾都是换行符，用[:-1]的方法读取最后一位之前的内容
                print('Firefox')
            else:
                chromecapture.chrome_capture(line[:-1], path, whichbrowser)
                print('here')
            print('新图获取完成！')

    #与原始图片进行对比，结果保存到diffimages文件夹
    def diff(self):
        whichbrowser = choosebrowser.get()
        website = self.websiteEntry.get()
        path_one1 = os.path.abspath('.') + '\\projects\\' + website + '\\baseimages'#基准图片目录
        path_two1 = os.path.abspath('.') + '\\projects\\' + website + '\\newimages\\'+whichbrowser#新图片目录
        diff_save_location1 = os.path.abspath('.') + '\\projects\\' + website + '\\diffimages\\'+whichbrowser#差异图片目录
        if not os.path.exists(diff_save_location1):
            os.makedirs(diff_save_location1)
        pathDir = os.listdir(path_one1)#获取baseimages文件夹下所有文件的名称
        for allDir in pathDir:
            print(allDir)
            path_one=path_one1+"\\"+allDir
            path_two = path_two1+"\\" + allDir
            diff_save_location=diff_save_location1+"\\" + allDir

            diffimage.compare_images(path_one, path_two, diff_save_location, )


app = Application()
# 设置窗口标题:
app.master.title('WebTest')
# 主消息循环:
app.mainloop()
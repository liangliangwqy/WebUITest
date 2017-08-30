#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from tkinter import *

from views import capture, diffimage,geturl


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        #显示三个输入框的标题
        self.websiteLabel=Label(self,text="测试网址：").grid(row=0)
        self.path_oneLabel=Label(self,text='标准图片路径：').grid(row=1)
        self.path_twoLabel = Label(self, text='新获取图片路径：').grid(row=2)
        self.path_threeLabel = Label(self, text='差异结果图片保存路径：').grid(row=3)

        #显示四个输入框
        self.websiteEntry = Entry(self)
        self.websiteEntry.grid(row=0, column=1)


        self.path_oneEntry=Entry(self)
        self.path_oneEntry.grid(row=1,column=1)

        self.path_twoEntry = Entry(self)
        self.path_twoEntry.grid(row=2,column=1)

        self.diff_save_locationEntry = Entry(self)
        self.diff_save_locationEntry.grid(row=3, column=1)

        #获取原始图片的功能按钮
        self.website1 = Button(self, text="获取原图", command=self.getoriginimage)
        self.website1.grid(row=4, column=0)
        #比较图片的功能按钮
        self.diffButton=Button(self,text="比较图片",command=self.diff)
        self.diffButton.grid(row=4,column=1)

        #退出程序的按钮
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=4,column=2)
    def getoriginimage(self):
        website = self.websiteEntry.get()
        print('正在获取'+website+'的所有连接...')

        #获得被测网站的所有页面连接
        geturl.getinfo(website)
        print('geturl.fobj1：'+geturl.fobj1)
        url=open(geturl.fobj1)
        for line in url:
            #对所有页面连接生成截图
            print('正在获取' +line+ '的页面截图...')
            capture.capture(url)
            print('原图获取完成！')
    def diff(self):
        # 获取三个输入框的值
        path_one = self.path_oneEntry.get()
        path_two = self.path_twoEntry.get()
        diff_save_location = self.diff_save_locationEntry.get()
        #执行图片对比，并输出结果
        diffimage.compare_images(path_one, path_two, diff_save_location)

app = Application()
# 设置窗口标题:
app.master.title('WebTest')
# 主消息循环:
app.mainloop()
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:TangLiang
import os
from tkinter import *
from webuitest import chromecapture, diffimage, capture, geturl


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createwidgets()

    def createwidgets(self):
        # 测试网址输入框的标题
        self.websiteLabel = Label(self, text="被测站点域名：")
        self.websiteLabel.grid(row=0, column=0, columnspan=1)

        # 测试网址域名输入框
        self.websiteEntry = Entry(self)
        self.websiteEntry.grid(row=0, column=1, columnspan=1)

        # 获取站点所有url按键
        self.geturlButton = Button(self, text="1.获取所有连接", command=self.getwebsiteurl)
        self.geturlButton.grid(row=0, column=2)

        # TODO(Tony):在V1.5版本中实现单选按钮的默认选择
        global choosebrowser
        global choosewhereisbrowser
        choosebrowser = StringVar()
        choosewhereisbrowser = IntVar()

        # 选择浏览器
        self.WhereisbrowserButtom = Checkbutton(self, text='使用本地浏览器', variable=choosewhereisbrowser)
        self.WhereisbrowserButtom.grid(row=1, column=2, columnspan=1, sticky=W)

        self.ChromeRadioButtom = Radiobutton(self, text='Chrome', variable=choosebrowser, value='Chrome')
        self.ChromeRadioButtom.grid(row=2, column=0, sticky=W)
        self.IERadioButtom = Radiobutton(self, text='Edge', variable=choosebrowser, value='Edge')
        self.IERadioButtom.grid(row=2, column=1, sticky=W)
        self.FirefoxRadioButtom = Radiobutton(self, text='Firefox', variable=choosebrowser, value='Firefox')
        self.FirefoxRadioButtom.grid(row=2, column=2, sticky=W)
        self.IERadioButtom = Radiobutton(self, text='IE 8', variable=choosebrowser, value='IE 8')
        self.IERadioButtom.grid(row=3, column=0, sticky=W)
        self.IERadioButtom = Radiobutton(self, text='IE 9', variable=choosebrowser, value='IE 9')
        self.IERadioButtom.grid(row=3, column=1, sticky=W)
        self.IERadioButtom = Radiobutton(self, text='IE 10', variable=choosebrowser, value='IE 10')
        self.IERadioButtom.grid(row=3, column=2, sticky=W)
        self.IERadioButtom = Radiobutton(self, text='IE 11', variable=choosebrowser, value='IE 11')
        self.IERadioButtom.grid(row=3, column=3, sticky=W)
        self.TipsLabel = Label(self, text="选择一个浏览器用于2、3、4操作：")
        self.TipsLabel.grid(row=1, column=0, columnspan=2, sticky=W)

        # TODO(Tony):在V1.5版本中实现单选按钮的默认选择,实现浏览器多选
        global screen_pix_w
        screen_pix_w = StringVar()
        # 选择图片宽度
        self.PCScreenRadioButtom = Radiobutton(self, text='1920（PC）', variable=screen_pix_w,
                                               value='1920')  # 最常见PC显示器宽度为1920，因edge浏览器获取截图最宽为1892，设value为1920时所有浏览器可获得宽度为1892的截图
        self.PCScreenRadioButtom.grid(row=5, column=0, sticky=W)
        self.TwoKRadioButtom = Radiobutton(self, text='1440（Moblie）', variable=screen_pix_w,
                                           value='1468')  # 适合2k手机使用，获取到的图片宽度为1440
        self.TwoKRadioButtom.grid(row=5, column=1, sticky=W)
        self.FHDMobileRadioButtom = Radiobutton(self, text='1080（Moblie）', variable=screen_pix_w,
                                                value='1108')  # 适合1080P手机使用，获取到的图片宽度为1080
        self.FHDMobileRadioButtom.grid(row=5, column=2, sticky=W)
        self.HDRadioButtom = Radiobutton(self, text='720（Moblie）', variable=screen_pix_w,
                                         value='748')  # 适合720P手机使用，获取到的图片宽度为720
        self.HDRadioButtom.grid(row=5, column=3, sticky=W)
        self.TipsLabel = Label(self, text="选择一个显示屏宽度用于2、3、4操作：")
        self.TipsLabel.grid(row=4, column=0, columnspan=3, sticky=W)

        # 获取原始图片的功能按键
        self.website1 = Button(self, text="2.获取基准图片", command=lambda: self.getimage(path='baseimages'))
        self.website1.grid(row=7, column=0)
        # 使用选择的浏览器获取新图
        self.website1 = Button(self, text="3.获取新图", command=lambda: self.getimage(path='newimages'))
        self.website1.grid(row=7, column=1)
        # 比较图片的功能按键
        self.diffButton = Button(self, text="4.比较图片", command=self.diff)
        self.diffButton.grid(row=7, column=2)

        self.TipsLabel = Label(self, text="Tips1：因不同浏览器对同一元素的渲染通常存在像素级的差异，不同浏览器的截图对比仅供参考。")
        self.TipsLabel.grid(row=8, column=0, columnspan=3, sticky=W)
        self.TipsLabel = Label(self, text="Tips2：在不同的测试环境分别用相同的浏览器获取截图，对比结果可精确验证不同环境下的差异。")
        self.TipsLabel.grid(row=9, column=0, columnspan=3, sticky=W)
        self.TipsLabel = Label(self, text="Tips3：如需要测试指定连接，请修改项目文件夹下的“域名.txt”文件，注意保持最后一行空白。")
        self.TipsLabel.grid(row=10, column=0, columnspan=3, sticky=W)
        # 退出程序的按钮
        self.quitButton = Button(self, text='退出程序', command=self.quit)
        self.quitButton.grid(row=11, column=1)

    # 获得被测网站的所有页面连接
    def getwebsiteurl(self):
        website = self.websiteEntry.get()
        print('正在获取' + website + '站点的所有连接...')
        geturl.getinfo(website)

    #  -获取页面的当前截图
    def getimage(self, path='newimages'):
        whichbrowser = choosebrowser.get()
        if choosewhereisbrowser.get() == 1:
            whereisbrowser = 'local'
        else:
            whereisbrowser = 'remote'
        print('正在调取的浏览器是:', whichbrowser)
        screen_pix_w1 = int(screen_pix_w.get())
        print('设置显示器宽度为:', screen_pix_w1)
        website = self.websiteEntry.get()
        url = open(os.path.abspath('.') + '\\projects\\' + website + '\\' + website + '.txt')
        for line in url:
            # 对所有页面连接生成截图
            print('正在获取' + line, end='' + '的页面截图...')
            if whichbrowser == 'IE 8' or whichbrowser == 'IE 9' or whichbrowser == 'IE 10' or whichbrowser == 'IE 11':
                capture.capture(line[:-1], screen_pix_w1, path, whichbrowser,
                                whereisbrowser)  # 因为每行结尾都是换行符，用[:-1]的方法读取最后一位之前的内容
            else:
                chromecapture.chrome_capture(line[:-1], screen_pix_w1, path, whichbrowser, whereisbrowser)
            print('页面截图获取完成！')
            print('\n')

    # 与原始图片进行对比，结果保存到diffimages文件夹
    def diff(self):
        whichbrowser = choosebrowser.get()
        website = self.websiteEntry.get()
        path_one1 = os.path.abspath('.') + '\\projects\\' + website + '\\baseimages'  # 基准图片目录
        path_two1 = os.path.abspath('.') + '\\projects\\' + website + '\\newimages\\' + whichbrowser  # 新图片目录
        diff_save_location1 = os.path.abspath(
            '.') + '\\projects\\' + website + '\\diffimages\\' + whichbrowser  # 差异图片目录
        if not os.path.exists(diff_save_location1):
            os.makedirs(diff_save_location1)
        pathDir = os.listdir(path_one1)  # 获取baseimages文件夹下所有文件的名称
        for allDir in pathDir:
            print('正在比较的页面是：', allDir)
            path_one = path_one1 + "\\" + allDir
            path_two = path_two1 + "\\" + allDir
            diff_save_location = diff_save_location1 + "\\" + allDir

            diffimage.compare_images(path_one, path_two, diff_save_location, )


print('请在弹出的界面中输入"被测站点域名",如：www.meizu.com')
app = Application()
# 设置窗口标题:
app.master.title('WebTest')
# 主消息循环:
app.mainloop()

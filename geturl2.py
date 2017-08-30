#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.path_one=Entry(self)
        self.path_one.pack()
        self.path_two = Entry(self)
        self.path_two.pack()
        self.diff_save_location = Entry(self)
        self.diff_save_location.pack()
        self.helloLabel = Label(self, text='WebTest')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        #self.diffButton=Button(self,text="比较图片",command=difff)
        #self.diffButton.pack()
    def difff(self):
        path_one=self.path_one.get()
        path_two=self.path_two.get()
        diff_save_location=self.diff_save_location.get()
        #diffimage.compare_images(self.path_one, self.path_two, self.diff_save_location)


app = Application()
# 设置窗口标题:
app.master.title('WebTest')
# 主消息循环:
app.mainloop()
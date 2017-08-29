#!/usr/bin/env python
#-*- conding:utf-8 -*-
from tkinter import *
master =Tk()
master.title='biaoge'
Label(master,text="username").grid(row=0)
Label(master,text="password").grid(row=1)

e1=Entry(master).grid(row=0,column=1)
e2=Entry(master).grid(row=1,column=1)

button=Button(master,text="login").grid(row=0,column=2,columnspan=2,rowspan=2,padx=5,pady=5,sticky=W+E+N+S)
mainloop()
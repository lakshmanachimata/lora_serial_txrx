#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import Tkinter, tkMessageBox
import serial
from Tkinter import *
from tkMessageBox import *
import binascii

global sendData
global recvData


class Application(Frame):

    def __init__(self, master=None):
        global guiHandler
        Frame.__init__(self, master)
        master.minsize(width=800, height=800)
        master.maxsize(width=800, height=800)
        self.grid(padx=0, pady=0)
        T = Text(master, height=2, width=25)
        T.pack()
        T.insert(END, "Enter COM Here")
        T.config(state='disabled')
        global editBox
        editBox = Entry(master)
        editBox.grid(padx=10, pady=10)
        editBox.pack()
        self.createWidgets()
        self.pack(fill=BOTH, expand=1)

    def createWidgets(self):
    
        self.LEXCEL = Button(self)
        self.LEXCEL["text"] = "CONNECT DEVICE"
        self.LEXCEL.pack({"side": "left"})
        self.LEXCEL.grid(row=0, column=0)

        self.DOWNLINK = Button(self)
        self.DOWNLINK["text"] = "SEND DOWN LINK"
        self.DOWNLINK.pack({"side": "left"})
        self.DOWNLINK.grid(row=2, column=0)
        

        self.QUIT = Button(self)
        self.QUIT["text"] = "EXIT APP"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})
        self.QUIT.grid(row=4, column=0)


root = Tk()
root.wm_title("GND LoRa Test and Report Tool")
app = Application(master=root)
app.mainloop()
root.destroy()

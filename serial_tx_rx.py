#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import Tkinter, tkMessageBox
import serial
from Tkinter import *
from tkMessageBox import *
import binascii
import datetime
import threading


global sendData
global recvData
global portValue
global portEditBox


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
        self.DATAT = Text(root, height=10, width=70)
        self.DATAT.pack()
        global portEditBox
        portEditBox = Entry(master)
        portEditBox.grid(padx=10, pady=10)
        portEditBox.pack()
        self.createWidgets()
        self.pack(fill=BOTH, expand=1)

    def connectDevice(self):
        global portValue
        portValue = portEditBox.get()
        self.ser = serial.Serial(port=portValue, baudrate=9600, timeout=60)
        print self.ser.name
        self.readThread = threading.Thread(target=self.readDataFromDevice)
        self.readThread.start()

    def readDataFromDevice(self):
        startDT = datetime.datetime.now()
        print (str(startDT))
        while True:
            data = []
            data.append(self.ser.readline())
            logTime = datetime.datetime.now()
            print data 
            print (str(logTime))

    def quitApp(self):
        # self.readThread
        print ("QUITTING APP")
        self.quit()
        
    def createWidgets(self):
    
        self.LEXCEL = Button(self)
        self.LEXCEL["text"] = "CONNECT DEVICE"
        self.LEXCEL.pack({"side": "left"})
        self.LEXCEL["command"] = self.connectDevice
        self.LEXCEL.grid(row=0, column=0)

        self.DOWNLINK = Button(self)
        self.DOWNLINK["text"] = "SEND DOWN LINK"
        self.DOWNLINK.pack({"side": "left"})
        self.DOWNLINK.grid(row=2, column=0)
        

        self.QUIT = Button(self)
        self.QUIT["text"] = "EXIT APP"
        self.QUIT["command"] =  self.quitApp
        self.QUIT.pack({"side": "left"})
        self.QUIT.grid(row=4, column=0)


root = Tk()
root.wm_title("GND LoRa Test and Report Tool")
app = Application(master=root)
app.mainloop()
root.destroy()

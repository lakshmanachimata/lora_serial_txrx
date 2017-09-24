#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import Tkinter, tkMessageBox
import serial
from Tkinter import *
from tkMessageBox import *
import binascii
import datetime
import threading
import time

global sendData
global recvData
global portValue
global portEditBox
global sendDataBox
global deviceId

class Application(Frame):

    def __init__(self, master=None):
        global guiHandler
        Frame.__init__(self, master)
        master.minsize(width=800, height=800)
        master.maxsize(width=800, height=800)
        self.grid(padx=0, pady=0)
        # self.DATAT = Text(root, height=10, width=70)
        # self.DATAT.place(relx=, rely=2.5)

        comText = Text(master, height=2, width=25)
        comText.place(relx=0.1, rely=0.01)
        comText.insert(END, "Enter COM Here")
        comText.config(state='disabled')

        sendText = Text(master, height=2, width=25)
        sendText.place(relx=0.1, rely=0.05)
        sendText.insert(END, "Enter DATA Here")
        sendText.config(state='disabled')

        deviceIDText = Text(master, height=2, width=25)
        deviceIDText.place(relx=0.1, rely=0.09)
        deviceIDText.insert(END, "Device ID")
        deviceIDText.config(state='disabled')

        global portEditBox
        portEditBox = Entry(master)
        portEditBox.place(relx=0.3, rely=0.01)

        global sendDataBox
        sendDataBox = Entry(master)
        sendDataBox.place(relx=0.3, rely=0.05)

        self.CONNECT = Button(self)
        self.CONNECT["text"] = "Connect"
        self.CONNECT.pack({"side": "left"})
        self.CONNECT["command"] = self.connectDevice
        self.CONNECT.place(relx=0.6, rely=0.01)

        self.SENDDATA = Button(self)
        self.SENDDATA["text"] = "Send"
        self.SENDDATA.pack({"side": "left"})
        self.SENDDATA["command"] = self.writeDataToDevice
        self.SENDDATA.place(relx=0.6, rely=0.05)

        self.QUIT = Button(self)
        self.QUIT["text"] = "EXIT"
        self.QUIT["command"] = self.quitApp
        self.QUIT.pack({"side": "left"})
        self.QUIT.place(relx=0.9, rely=0.01)

        self.sendLog = Text(master, borderwidth=2, height=40, width=100)
        self.sendLog.place(relx=0.01, rely=0.15)
        self.sendLog.insert(END, "DATA LOG \n\n")
        # self.sendLog.config(state='disabled')

        # self.recvLog = Text(master, height=40, width=50)
        # self.recvLog.place(relx=0.51, rely=0.15)
        # self.recvLog.insert(END, "Recv Data \n")
        # self.sendLog.config(state='disabled')


        self.pack(fill=BOTH, expand=1)

    def getID(self):
        global deviceId
        self.ser.write('@connect!')
        self.isREading = True
        self.readThread = threading.Thread(target=self.readDataFromDevice)
        self.readThread.start()


    def connectDevice(self):
        global portValue
        portValue = portEditBox.get()
        self.ser = serial.Serial(port=portValue, baudrate=9600)
        self.sendLog.insert("end", self.ser.name + "   Connected" + "\n")
        self.getID()

    def writeDataToDevice(self):
        global sendDataBox
        sdata = sendDataBox.get()
        writeData = '$' + sdata + '#'
        self.ser.write(writeData)



    def readDataFromDevice(self):
        while self.isREading:
            try:
                data = []
                line = self.ser.readline()
                if(len(line) > 0 and line != "\n"):
                    if(line.startswith('$dev:')):
                        devid = line.partition(':')[-1].rpartition('#')[0]
                        print ("DEVID IS  " + devid)
                        self.deviceIDTextVal = Text(root, height=2, width=25)
                        self.deviceIDTextVal.place(relx=0.3, rely=0.09)
                        self.deviceIDTextVal.insert(END, devid)
                        self.deviceIDTextVal.config(state='disabled')
                    else:
                        data.append(line)
                        logTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        data.append("   ")
                        data.append(str(logTime))
                        self.sendLog.insert("end", data)
                        self.sendLog.insert("end", "\n")
                else:
                    print("NO DATA")
            except serial.SerialException:
                print("SERIAL EXCEPTION HANDLED")

    def quitApp(self):
        self.isREading = False
        time.sleep(1)
        
        if hasattr(self, 'ser'):
            print ("CLOSING DEVICE CONNECTION")
            self.ser.close()

        print ("QUITTING APP")
        self.quit()
            



root = Tk()
root.wm_title("GND LoRa Test and Report Tool")
app = Application(master=root)
app.mainloop()
root.destroy()

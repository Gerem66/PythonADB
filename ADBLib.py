#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
from PIL import Image

class SmartPhone(object):
    def __init__(self, ADB_PATH, index = 0):
        self.PIC_PATH = "/sdcard/screen.jpg"
        self.TMP_IMG = "screen.jpg"

        self.ADB_PATH = ADB_PATH + ("\\" if ADB_PATH[-1] != "\\" else "")
        self.DEVICES = []
        self.LoadDevices()
        self.SetDevice(index)
    
    def LoadDevices(self):
        devices = os.popen(self.ADB_PATH + "adb devices").read().split("\n")
        for device in devices[1:]:
            if device == "": continue
            d = device.split()
            if d[1] == "device":
                self.DEVICES.append(d[0])
        if len(self.DEVICES) <= 0:
            self.Error("No device detected !")
    
    def GetDevices(self):
        return self.DEVICES

    def SetDevice(self, index):
        if index < 0 or index >= len(self.DEVICES):
            self.Error("Wrong device index")
        self.CURR_DEV = index

    def ADB(self, arg):
        os.system("{}adb -s {} {}".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], arg))



    # Public functions
    
    def Press(self, x, y):
        self.CheckType([x, y], int)
        self.ADB("shell input tap {} {}".format(x, y))

    def LongPress(self, x, y, duration):
        self.Swipe(x, y, x, y, duration)
    
    def Swipe(self, x1, y1, x2, y2, duration):
        self.CheckType([x1, x2, y1, y2, duration], int)
        self.ADB("shell input touchscreen swipe {} {} {} {} {}".format(x1, y1, x2, y2, duration))

    def WriteText(self, text):
        self.ADB("shell input text '{}'".format(text))

    def TakeScreenshot(self):
        self.ADB("shell screencap -p " + self.PIC_PATH)
        self.ADB("pull {} {}".format(self.PIC_PATH, self.TMP_IMG))
        self.ADB("shell rm " + self.PIC_PATH)
        time.sleep(0.1)
        img = Image.open(self.TMP_IMG).copy()
        os.remove(self.TMP_IMG)
        return img
    


    # Errors

    def CheckType(self, vars, typ):
        for var in vars:
            if type(var) != typ:
                self.Error("Argument isn't an integer !")
            
    def Error(self, text):
        print("Error : " + text)
        exit(-1)
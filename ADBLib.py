#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
from PIL import Image

class SmartPhone(object):
    def __init__(self, ADB_PATH):
        self.errors = [
            "Argument isn't an integer !"
        ]
        self.ADB_PATH = ADB_PATH + ("\\" if ADB_PATH[-1] != "\\" else "")
        self.PIC_PATH = "/sdcard/screen.jpg"
        self.TMP_IMG = "screen.jpg"
    
    def Press(self, x, y):
        self.CheckType([x, y], int)
        os.system(self.ADB_PATH + "adb shell input tap {} {}".format(x, y))

    def LongPress(self, x, y, duration):
        self.Swipe(x, y, x, y, duration)
    
    def Swipe(self, x1, y1, x2, y2, duration):
        self.CheckType([x1, x2, y1, y2, duration], int)
        os.system("{}adb shell input touchscreen swipe {} {} {} {} {}".format(self.ADB_PATH, x1, y1, x2, y2, duration))

    def TakeScreenshot(self):
        os.system(self.ADB_PATH + "adb shell screencap -p " + self.PIC_PATH)
        os.system(self.ADB_PATH + "adb pull {} {}".format(self.PIC_PATH, self.TMP_IMG))
        os.system(self.ADB_PATH + "adb shell rm " + self.PIC_PATH)
        time.sleep(0.1)
        img = Image.open(self.TMP_IMG).copy()
        os.remove(self.TMP_IMG)
        return img
    
    def CheckType(self, vars, typ):
        for var in vars:
            if type(var) != typ:
                self.Error(0)
    
    def Error(self, index_code):
        i = index_code if index_code > 0 and index_code < len(self.errors) else 0
        print(self.errors[i])
        exit(-1)
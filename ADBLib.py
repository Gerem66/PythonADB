#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
from PIL import Image

class SmartPhone(object):
    def __init__(self, ADB_PATH):
        self.ADB_PATH = ADB_PATH + ("\\" if ADB_PATH[-1] != "\\" else "")
        self.PIC_PATH = "/sdcard/screen.jpg"
    
    def Press(self, x, y):
        if type(x) != int or type(y) != int:
            return
        os.system(self.ADB_PATH + "adb shell input tap {} {}".format(x, y))

    def LongPress(self, x, y, duration):
        self.Swipe(x, y, x, y, duration)
    
    def Swipe(self, x1, y1, x2, y2, duration):
        os.system("{}adb shell input touchscreen swipe {} {} {} {} {}".format(self.ADB_PATH, x1, y1, x2, y2, duration))

    def TakeScreenshot(self):
        os.system(self.ADB_PATH + "adb shell screencap -p " + self.PIC_PATH)
        os.system(self.ADB_PATH + "adb pull {} screen.jpg".format(self.PIC_PATH))
        os.system(self.ADB_PATH + "adb shell rm " + self.PIC_PATH)
        time.sleep(0.1)
        return Image.open("screen.jpg")
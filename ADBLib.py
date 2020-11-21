#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
from cv2 import imread

# Save : adb exec-out getevent -t /dev/input/event4 > recorded_touch_events.txt
# Load : adb push sendevent-arm64 /data/local/tmp/
#        adb push recorded_touch_events.txt /data/local/tmp/
#        adb shell /data/local/tmp/sendevent-arm64 /dev/input/event4 /data/local/tmp/recorded_touch_events.txt

class SmartPhone(object):
    def __init__(self, ADB_PATH = '', index = 0):
        self.PIC_PATH = "/sdcard/screen.jpg"
        self.TMP_IMG = "screen.jpg"
        self.offset_x = 0
        self.offset_y = 0

        if len(ADB_PATH) > 0 and ADB_PATH[-1] != "\\":
            ADB_PATH += "\\"
        self.ADB_PATH = ADB_PATH
        self.DEVICES = []
        self.EVENTSCREEN = ""
        self.LoadDevices()
        self.SetDevice(index)
        self.GetEventScreen()
    
    def SetOffset(self, x, y):
        self.offset_x = x
        self.offset_y = y
    
    def LoadDevices(self):
        devices = os.popen(self.ADB_PATH + "adb devices").read().split("\n")
        for device in devices[1:]:
            if device == "": continue
            d = device.split()
            if d[1] == "device":
                self.DEVICES.append(d[0])
            elif d[1] == "unauthorized":
                print("[!] Unauthorized device : " + d[0])
        if len(self.DEVICES) <= 0:
            self.Error("No device detected !")
    
    def GetDevices(self):
        return self.DEVICES

    def SetDevice(self, index):
        if index < 0 or index >= len(self.DEVICES):
            self.Error("Wrong device index")
        self.CURR_DEV = index
    
    def GetEventScreen(self):
        found = False
        events = os.popen("{}adb -s {} shell getevent -lp 2>/dev/null | egrep -o \"(/dev/input/event\S+)\"".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV]))
        for event in events:
            info = os.popen("{}adb -s {} shell getevent -lp {}".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], event[:-1]))
            for i in info:
                if "ABS_MT" in i:
                    self.EVENTSCREEN = event[:-1]
                    found = True
                    break
            if found:
                break

    def ADB(self, arg, sync = True, quiet = False):
        q = " > "+os.devnull if quiet else ""
        if not sync:
            os.popen("{}adb -s {} {}{}".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], arg, q))
        else:
            os.system("{}adb -s {} {}{}".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], arg, q))



    # Public functions
    
    def Press(self, x, y):
        self.CheckType([x, y], int)
        self.ADB("shell input tap {} {}".format(x + self.offset_x, y + self.offset_y))

    def LongPress(self, x, y, duration = 1000):
        self.Swipe(x, y, x, y, duration)
    
    def Swipe(self, x1, y1, x2, y2, duration = 1000):
        self.CheckType([x1, x2, y1, y2, duration], int)
        self.ADB("shell input touchscreen swipe {} {} {} {} {}".format(x1 + self.offset_x, y1 + self.offset_y, x2 + self.offset_x, y2 + self.offset_y, duration))

    def WriteText(self, text):
        self.ADB("shell input text '{}'".format(text))

    def TakeScreenshot(self, debug = False):
        self.ADB("shell screencap -p " + self.PIC_PATH, quiet=not debug)
        self.ADB("pull {} {}".format(self.PIC_PATH, self.TMP_IMG), quiet=not debug)
        self.ADB("shell rm " + self.PIC_PATH, quiet=not debug)
        time.sleep(0.1)
        img = imread(self.TMP_IMG).copy()
        os.remove(self.TMP_IMG)
        return img
    
    def TakeScreenshotWithPress(self, x, y, debug = False):
        self.ADB("shell input touchscreen swipe {} {} {} {} {}".format(x + self.offset_x, y + self.offset_y, x + self.offset_x, y + self.offset_y, 500), False, not debug)
        time.sleep(0.6)
        return self.TakeScreenshot(debug)

    def SaveMove(self):
        print("[!] Ctrl-C to end recording")
        os.system("{}adb -s {} exec-out getevent -t {} > recorded_touch_events.txt".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], self.EVENTSCREEN))
        exit(0)
    
    def SendMove(self):
        self.ADB("push sendevent-arm64 /data/local/tmp/")
        self.ADB("push recorded_touch_events.txt /data/local/tmp/")
        self.ADB("shell /data/local/tmp/sendevent-arm64 {} /data/local/tmp/recorded_touch_events.txt".format(self.EVENTSCREEN))


    # Errors

    def CheckType(self, vars, typ):
        for var in vars:
            if type(var) != typ:
                self.Error("Argument isn't an integer !")
            
    def Error(self, text):
        print("[-] " + text)
        exit(0)
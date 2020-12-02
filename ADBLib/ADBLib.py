#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
from cv2 import imread

class SmartPhone(object):
    def __init__(self, ADB_PATH = '', index = 0):
        self.PATH = os.path.dirname(__file__)
        self.PIC_PATH = "/sdcard/screen.jpg"
        self.TMP_IMG = "screen.jpg"
        self.offset_x = 0
        self.offset_y = 0
        self.eventuploaded = False

        if len(ADB_PATH) > 0 and ADB_PATH[-1] != "\\":
            ADB_PATH += "\\"
        self.ADB_PATH = ADB_PATH
        self.DEVICES = []
        self.EVENTSCREEN = ""
        self.LoadDevices()
        self.SetDevice(index)
        self.GetEventScreen()
    
    def Destroy(self):
        self.ADB("shell rm /data/local/tmp/sendevent-arm64", True)
        if self.eventuploaded:
            self.ADB("shell rm /data/local/tmp/events", True)
    
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

        # Upload : "sendevent-arm64"
        self.ADB("push {}/sendevent-arm64 /data/local/tmp/".format(self.PATH), True)
    
    def SetOffset(self, x, y):
        self.offset_x = x
        self.offset_y = y
    
    def GetEventScreen(self):
        found = False

        # Get all events
        events = []
        e = "/dev/input/event"
        output = os.popen("{}adb -s {} shell getevent -lp".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV]))
        for line in output.readlines():
            if e in line and not "could not get driver version" in line:
                length = len(e) + 1
                start = len(line) - length - 1
                events.append(line[start:start+length])

        # Wich is screen
        for event in events:
            info = os.popen("{}adb -s {} shell getevent -lp {}".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], event))
            for i in info:
                if "ABS_MT" in i:
                    self.EVENTSCREEN = event
                    found = True
                    break
            if found:
                break

    #########################
    # Private ADB functions #
    #########################

    def ADB(self, arg, quiet = False):
        q = " > "+os.devnull if quiet else ""
        os.system("{}adb -s {} {}{}".format(self.ADB_PATH, self.DEVICES[self.CURR_DEV], arg, q))

    def ADBPress(self, x, y):
        s = "0003 003a 00000001\n"
        s += "0003 0035 {}\n".format(self.IntToHex(x))
        s += "0003 0036 {}\n".format(self.IntToHex(y))
        s += "0003 0039 00000000\n"
        s += "0000 0002 00000000\n"
        s += "0001 014a 00000001\n"
        s += "0000 0000 00000000\n"
        return s
    def ADBRelease(self):
        s = "0000 0002 00000000\n"
        s += "0001 014a 00000000\n"
        s += "0000 0000 00000000\n"
        return s
    def ADBSet(self, x, y):
        s = "0003 003a 00000001\n"
        s += "0003 0035 {}\n".format(self.IntToHex(x))
        s += "0003 0036 {}\n".format(self.IntToHex(y))
        s += "0003 0039 00000000\n"
        s += "0000 0002 00000000\n"
        s += "0000 0000 00000000\n"
        return s
    def ADBTimer(self, d):
        return str(d) + "\n"
    def SendMove(self, ADBcommands):
        with open("{}/events".format(self.PATH), "a") as f:
            f.write(ADBcommands)
        self.ADB("push {}/events /data/local/tmp/".format(self.PATH), True)
        self.ADB("exec-out /data/local/tmp/sendevent-arm64 {} /data/local/tmp/events".format(self.EVENTSCREEN), True)
        os.remove("{}/events".format(self.PATH))
        self.eventuploaded = True

    ####################
    # Public functions #
    ####################

    def WriteText(self, text):
        self.ADB("shell input text '{}'".format(text))

    def TakeScreenshot(self, point = None, debug = False):
        press = False
        if point != None:
            self.CheckType(point, [int])
            press = True
            x, y = point
            self.SendMove(self.ADBPress(x, y))
        
        self.ADB("shell screencap -p " + self.PIC_PATH, not debug)
        self.ADB("pull {} {}".format(self.PIC_PATH, self.TMP_IMG), not debug)
        
        if point != press:
            self.SendMove(self.ADBRelease())
        
        self.ADB("shell rm " + self.PIC_PATH, not debug)
        img = imread(self.TMP_IMG).copy()
        os.remove(self.TMP_IMG)
        return img
    
    # TouchScreen functions
    
    def Press(self, x, y, duration = 1):
        self.Swipe([[x, y, duration]])

    def Swipe(self, coords):
        self.CheckType(coords, [int, float])
        s = self.ADBPress(coords[0][0], coords[0][1])
        s += self.ADBTimer(coords[0][2])

        for i in range(1, len(coords)):
            step = max(abs(coords[i][0] - coords[i-1][0]), abs(coords[i][1] - coords[i-1][1]))
            dt = float(coords[i][2]) / float(step)
            dx = (coords[i][0] - coords[i-1][0]) / step
            dy = (coords[i][1] - coords[i-1][1]) / step
            for p in range(step):
                nx = int(coords[i-1][0] + (dx * p))
                ny = int(coords[i-1][1] + (dy * p))
                s += self.ADBSet(nx, ny)
                s += self.ADBTimer(dt)

        s += self.ADBRelease()
        self.SendMove(s)

    #########    
    # Other #
    #########

    def IntToHex(self, val):
        return hex(val)[2:].zfill(8)

    ##########
    # Errors #
    ##########

    def CheckType(self, Var, Type):
        if not type(Var) in Type:
            if type(Var) == list:
                for v in Var:
                    self.CheckType(v, Type)
            else:
                self.Error("Argument type error !")
            
    def Error(self, text):
        print("[-] " + text)
        exit(0)
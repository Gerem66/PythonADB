#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
from ADBLib import SmartPhone as SP
from time import time
myPhone = SP()
#myPhone.SaveMove()
#myPhone.SendMove()
input(">> ")
t1 = time()
myPhone.ADBSwipe(600, 822, 311, 922, 0.5)
print(time() - t1)
#myPhone.Press(100, 800)
#myPhone.Swipe(50, 1500, 500, 1500) # Default duration : 1000ms
#myPhone.WriteText("heyyy !")
#cv2.imwrite("test.jpg", myPhone.TakeScreenshot())

myPhone.Destroy()
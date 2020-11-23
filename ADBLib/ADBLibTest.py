#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
from ADBLib import SmartPhone as SP

myPhone = SP()

#myPhone.Press(600, 822, 2)
#myPhone.Swipe([[ 600, 822, 0 ], [ 311, 922, 0.5 ], [ 500, 500, 1 ], [ 1000, 1000, 0.1 ]])
#myPhone.WriteText("heyyy !")
#cv2.imwrite("test.jpg", myPhone.TakeScreenshot()) # Save screenshot

myPhone.Destroy()
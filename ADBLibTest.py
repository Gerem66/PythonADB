#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
from ADBLib import SmartPhone as SP

myPhone = SP(r"C:\Users\Geremindows\Downloads\platform-tools")
#myPhone.Press(100, 800)
myPhone.Swipe([[50, 1500], [500, 1500]]) # Default duration : 1000ms
#myPhone.WriteText("heyyy !")
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
from ADBLib import SmartPhone as SP

myPhone = SP()

#myPhone.Press(600, 822, 2)
#myPhone.Swipe([[ 600, 822, 0 ], [ 311, 922, 0.5 ], [ 500, 500, 1 ], [ 1000, 1000, 0.1 ]])
#myPhone.WriteText("heyyy !")
#cv2.imwrite("test.jpg", myPhone.TakeScreenshot()) # Save screenshot

# Take and show screenshot
#img = myPhone.TakeScreenshot()                                          # Take screenshot
#img = cv2.resize(img, (int(len(img[0]) / 4), int(len(img) / 4)))        # Resize : resolution / 4
#cv2.imshow("test", img)                                                 # Show popup with screenshot
#cv2.waitKey(0)                                                          # Wait to press key
#cv2.destroyAllWindows()                                                 # Destroy window

myPhone.Destroy()
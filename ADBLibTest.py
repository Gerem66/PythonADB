#!/usr/bin/python3
# -*- coding: utf-8 -*-

import math
import cv2
from ADBLib import SmartPhone as SP

myPhone = SP()

#myPhone.Press(600, 822, 2)
#myPhone.Swipe([[ 600, 822, 0 ], [ 311, 922, 0.5 ], [ 500, 500, 1 ], [ 1000, 1000, 0.1 ]])
#myPhone.WriteText("heyyy !")
#cv2.imwrite("test.jpg", myPhone.TakeScreenshot()) # Save screenshot



# Pokéball roll
cercle = [ 500, 1500, 250, 0.01 ] # (500, 500) Point du centre du cercle, 50 : diamètre du cercle, 0.1 : vitesse entre chaque point
points = []
for _ in range(3): # On fait 3 tours
    for a in range(360)[::10]: # On prend 36 points sur un cercle trigo (0°, 10°, 20°, ..., 350°)
        rad = a * math.pi / 180
        p = [ 0, 0, 0 ] # Nouveau point
        p[0] = int(cercle[0] + (math.cos(rad) * cercle[2]))
        p[1] = int(cercle[1] + (math.sin(rad) * cercle[2]))
        p[2] = cercle[3]
        points.append(p)
myPhone.Swipe(points)
# Code un peu à l'arrache, tu calcules TOUS les points un à un,
# Stv opti tu peux calculer les points que tu veux sue UN seul cercle, puis les dupliquer pour faire plusieurs tours par exemple...
# Ne prend pas trop de points ou un temps trop court entre chaque point, si ça va trop vite le jeu ne va pas suivre



myPhone.Destroy()
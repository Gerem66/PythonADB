#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2 as cv
from ADBLib import SmartPhone as SP

myPhone = SP()
img = myPhone.TakeScreenshot()
image = img[1079:1879,:,:]

sys.setrecursionlimit(20000)

def CheckAround(index, start, x, y):
    if len(shapes) == index:
        shapes.append([])
        mt_shp.append([])

    shapes[index].append([x, y])
    edged[y][x] = 125

    for a in around:
        newx = max(0, min(len(edged[0]) - 1, x + a[0]))
        newy = max(0, min(len(edged) - 1, y + a[1]))
        if (newx != x or newy != y) and edged[newy][newx] == 255:
            CheckAround(index, False, newx, newy)
        
def ShapesInSurface(x1, y1, x2, y2):
    output = 0
    for i in shapes:
        for s in i:
            x, y = s
            if x > x1 and x < x2 and y > y1 and y < y2:
                output += 1
                break
    return output

def DrawSquare(x1, y1, x2, y2):
    for x in range(x1, x2):
        for y in range(y1, y2):
            if x > 0 and y > 0 and x < len(edged[0]) and y < len(edged):
                edged[y][x] = 255

# Main
edged = cv.Canny(image, 30, 200)
around = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
shapes = []
mt_shp = []

# Get shapes
for x in range(len(edged[0])):
    for y in range(len(edged)):
        if edged[y][x] == 255:
            CheckAround(len(shapes), True, x, y)

# Find Pokémons
square_size = 100
square_step = 50
for x in range(len(edged[0]))[10:-10:square_step]:
    for y in range(len(edged))[10:-10:square_step]:
        nb_shapes = ShapesInSurface(x, y, x + square_size, y + square_size)
        if nb_shapes > 10:
            DrawSquare(x, y, x + square_size, y + square_size)

# Result
cv.imshow('Pokemons', edged)
cv.imshow('Game', image)
cv.waitKey(0)
cv.destroyAllWindows()
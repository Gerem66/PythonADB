#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ADBLib import SmartPhone as SP

# Tu initialise ta variable avec comme seul argument le chemin vers ton ADB
myPhone = SP(r"C:\Users\Geremindows\Downloads\platform-tools")



# Pour effectuer une pression :
#myPhone.Press(500, 500)



# Pour faire une capture d'écran et l'ouvrir
#myPhone.TakeScreenshot().show()



# Sinon, pour l'utiliser tu peux faire qqchose comme
#with myPhone.TakeScreenshot() as img:
#    print(img)
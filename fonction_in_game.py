import cv2 as cv
import numpy as np
from ADBLib import SmartPhone as SP
from PIL import Image
from numpy import asarray

def reco_pkm(image_in): # fonction qui prend en entrée une image de la map et en ressort avec une image modifiée ou les pokemons sont en noirs.

    def mask_on(img,lower,upper): # fonction pour isoler une certaine brochette de couleur 
        lower_range = np.array(lower)  # Set the Lower range value of color in BGR
        upper_range = np.array(upper)   # Set the Upper range value of color in BGR
        #print(type(img), img.shape)
        #print(type(lower_range), img.shape)
        mask = cv.inRange(cv.cvtColor(img, cv.COLOR_BGR2HSV),lower_range,upper_range) # Create a mask with range
        result = cv.bitwise_and(img,img,mask = mask)  # Performing bitwise and operation with mask in img variable
        #cv.imwrite(name,result)
        return result
        
    # =============================================================================
    # On télécharge la premiere image et on applique plusieurs filtre dessus
    # =============================================================================
    #img = cv.imread(image_in) # on récupère le screenshot 
    img = np.array(image_in)
    #img = image_in
    print(type(img))

    green = mask_on(img,(80,200,80),(220,255,200))     # On chope le vert 
    grey = mask_on(img,(120,130,50),(190,200,130))    # On chope le gris 
    yellow = mask_on(img,(130,200,145),(200,255,255))  # On chope le jaune 



    # =============================================================================
    # On fusionne
    # =============================================================================
      
    img = cv.addWeighted(green, 1, grey, 1, 0) # fusion de deux images 
    img = cv.addWeighted(img, 1, yellow, 1, 0) 
    cv.imwrite("all.jpg",img)
    
    
myPhone = SP(r"C:\Users\Geremindows\Downloads\platform-tools")
reco_pkm(myPhone.TakeScreenshot())

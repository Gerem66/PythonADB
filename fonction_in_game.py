def reco_pkm(image_in): # fonction qui prend en entrée une image de la map et en ressort avec une image modifiée ou les pokemons sont en noirs.

    def mask_on(img,name,blue_1,green_1,red_1,blue_2,green_2,red_2): # fonction pour isoler une certaine brochette de couleur 
        lower_range = np.array([blue_1,green_1,red_1])  # Set the Lower range value of color in BGR
        upper_range = np.array([blue_2,green_2,red_2])   # Set the Upper range value of color in BGR
        #print(type(img), img.shape)
        #print(type(lower_range), img.shape)
        mask = cv.inRange(img,lower_range,upper_range) # Create a mask with range
        result = cv.bitwise_and(img,img,mask = mask)  # Performing bitwise and operation with mask in img variable
        cv.imwrite(name,result)
        
    # =============================================================================
    # On télécharge la premiere image et on applique plusieurs filtre dessus
    # =============================================================================
    img = cv.imread(image_in) # on récupère le screenshot 
    #img = image_in
    print(type(img))

    mask_on(img,"test_green.jpg",100,200,80,210,255,200)     # On chope le vert 
    mask_on(img,"test_grey.jpg",130,140,60,180,200,130)    # On chope le gris 
    mask_on(img,"test_yellow.jpg",145,200,145,200,255,255)  # On chope le jaune 


    # =============================================================================
    # On fusionne
    # =============================================================================
    green = cv.imread('test_green.jpg', 1) # lecture des images 
    grey = cv.imread('test_grey.jpg', 1) 
    yellow = cv.imread('test_yellow.jpg', 1) 
      
    img = cv.addWeighted(green, 1, grey, 1, 0) # fusion de deux images 
    img = cv.addWeighted(img, 1, yellow, 1, 0) 
    cv.imwrite("all.jpg",img)
    
    # Show the image 
    cv.imshow('image', img) 
    
    
reco_pkm(asarray(myPhone.TakeScreenshot()))

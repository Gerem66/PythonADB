# =============================================================================
# Liste des fonctions opérationnelle pour Pokémon Go Bot
# =============================================================================
import cv2 as cv
import numpy as np
from PogoADBLib import SmartPhone as SP
import time
myPhone = SP(r".\platform-tools") # Chemin absolu ou relatif depuis ce script

"""revoir filtre"""
"""pokestop"""
"""perso milieu enlevé"""
"""rond blanc capture nuit"""
"""enlever les pixels qui représentent le joueur"""
"""rajouter un moyen de savoir quand c'est mode nuit"""
"""filtrer cercle couleur pour déterminer quel ball prendre"""
"""encens fait beuger les filtres"""
"""montgolfiere team rocket"""
"""combat team rocket"""
"""pokemon pas au centre terrain"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def is_approx(list_a, list_b,delta): # fonction qui regarde si deux listes sont approximativement identiques
# a utiliser pour comparer des valeurs de pixels 
    result = False 
    if len(list_a) != len(list_b):
        return False
    for i in range(len(list_a)):
            if list_b[i] >= list_a[i] - delta and list_b[i] <= list_a[i] + delta : 
                result = True 
            else : 
                result = False 
    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def is_approx_nbr(a,b,delta): # fonction qui regarde si deux nombres sont environ égaux 
    result = False 
    if b >= a - delta and b <= a + delta : 
        result = True 
    else : 
        result = False 
    return(result)   

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def is_identical(list_a, list_b): # fonction qui regarde si deux listes sont identiques 
    if len(list_a) != len(list_b):
        return False
    for i in list_a:
        if i not in list_b:
            return False
    return True
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def check_cbt(img) : # fonction qui sert a checker si on est en combat ou non 
    result = False 
    if is_approx(img[260][100], [250, 250, 250],10) and is_approx(img[2000][120], [122, 73, 215],20) and is_approx(img[1980][950], [30, 50, 203],20) : 
       result = True 
    else : 
        result = False 
    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def check_circle() : # fonction qui permet de regarder ou est le cercle du pokemon
    (x,y) = (0,0)
    while x==0 and y == 0 : # tant qu'on a pas la valeur du centre du cercle 
        img = myPhone.TakeScreenshotWithPress(550,2000) 
        cv.imwrite("test_rond_blanc.png",img)
        img=img[300:1800,:]
        """
        img = mask_on(img,(140,160,160),(255,255,255))  # On chope l'anneau blanc
        bleu = mask_on(img,(190,0,0),(195,0,0)) # filtre bleu contre l'appui
        img = cv.addWeighted(img, 1, bleu, 1, 0) # fusion de deux images 
        """
        output = img.copy()
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find circles
        circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1.3, 100)
        # If some circle is found
        if circles is not None:
           # Get the (x, y, r) as integers
           circles = np.round(circles[0, :]).astype("int")
           #print(circles)
           # loop over the circles
           for (x, y, r) in circles:
              cv.circle(output, (x, y), r, (0, 255, 0), 2)
        cv.imwrite("test.png",output)
    return(int(x),int(y+300)) # on retourne le centre du cercle 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def lance_pkb(x,y):
    
    #myPhone.Swipe(500,2100,500,1200,200)
    myPhone.Swipe(500,2100,500,int(y- (y*(9/100))),200)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def after_catch(img) : # fonction juste après avoir capturé un pokémon 
    """
    
    gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    
    
    template=cv.imread('ok.png',0)
    #result of template matching of object over an image
    result=cv.matchTemplate(gray,template,cv.TM_CCOEFF)
    sin_val, max_val, min_loc, max_loc=cv.minMaxLoc(result)
    
    
    
    top_left=max_loc
    #increasing the size of bounding rectangle by 50 pixels
    bottom_right=(top_left[0]+50,top_left[1]+50)
    cv.rectangle(image, top_left, bottom_right, (0,255,0),5)
    
    cv.imwrite("resultat_ok.png",image)
    """
    #img=cv.imread(r'temp\tempo.png')
    result = False 
    # on regarde les 4 points autour de l'écran de résumé xp
    if is_approx(img[800][100], [254, 255, 245],10) and is_approx(img[800][1000], [244, 255, 246],10) : # 2 points du haut (toujours au même endroit)
        if is_approx(img[1500][100], [244, 255, 245],10) and is_approx(img[1500][1000], [235, 255, 238],10) :  # 2 points du bas (changent de place des fois)
        # on regarde deux points sur le bouton vert "ok"
            if is_approx(img[1500][543], [157, 213, 114],10) : # 2 poits, changent de places des fois 
            #is_approx(img[1450][543], [157, 213, 114],10) 
                result=True
    
    return(result)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def fiche_pkm(img) : # fonction qui regarde si on est sur la fiche pokemon 
    result = False
    if is_approx(img[900][40], [250, 250, 250],10) and is_approx(img[900][1040], [250, 250, 250],10) : # 2 points du haut (toujours au même endroit)
        if is_approx(img[2100][540], [150, 135, 28],10) and is_approx(img[2040][540], [150, 135, 28],10) : # 2 points du haut (toujours au même endroit)
            result = True 
            
    return(result)




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def lecture_IV(): # fonction qui permet de lire les IV du pokémon
    etoile = 0
    myPhone.Press(930,2100) # on appui sur le bouton avec 3 barres 
    time.sleep(0.2) # on attend un peu histoire que les options apparaissent 
    myPhone.Press(826,1666) # on clique sur évaluer 
    time.sleep(0.2) # on attend un peu 
    myPhone.Press(826,1666) # on clique pour faire passer blanche 
    time.sleep(1) # on attend un peu histoire que les options apparaissent 
    img = myPhone.TakeScreenshot() # prend un screenshot pour scanner 
    #cv.imwrite('Image_tessssssssssssssst.jpg',img)
    #print(img[1430][230],img[1390][160],img[1415][90])
    # on scanne 
    if is_approx(img[1430][230], [111, 201, 255],10) : # troisième étoile 230 1365
        etoile = 3 
    else : # si pas trois étoile on regarde si 2 
        if is_approx(img[1455][160], [111, 202, 253],10) : # deuxième étoile 160 1390 
            etoile = 2 
        else : # si pas 2 étoiles 
            if is_approx(img[1480][90], [112, 203, 254],10) : # première étoile 90 1415 
                etoile = 1 
            else : # si y'a pas 1 étoile bah y'en a 0 
                etoile = 0 
    myPhone.Press(500,500) # on clique pour finir
    return(etoile)
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def relache(cran_etoile=-1, etoile=-2,pkm_event = False): # fonction qui permet de relacher le pokemon en fonction d'un cran d'étoiles placé au préalable
    
    if etoile < cran_etoile : # si le nombre d'étoile du pokemon est inférieur au cran, alors on le relache
        time.sleep(0.2) # on attend un peu histoire que les options apparaissent     
        myPhone.Press(930,2100) # on appui sur le bouton avec 3 barres 
        time.sleep(0.2) # on attend un peu histoire que les options apparaissent 
        myPhone.Press(850,1850) # on clique sur transferer
        time.sleep(0.2) # on attend un peu 
        myPhone.Press(550,1300) # on clique sur ok
        if pkm_event : # si on a décidé de transférer les pkm event
            time.sleep(0.4) # on attend un peu 
            img = myPhone.TakeScreenshot() # prend un screenshot pour regarder si y'a encore qqch 
            # on regarde si y'a le truc pour pokemon evenement 
            if is_approx(img[900][90], [255, 255, 255],10) and is_approx(img[900][1000], [255, 255, 255],10) and  is_approx(img[1440][90], [255, 255, 255],10) and  is_approx(img[1440][1000], [255, 255, 255],10) : 
                print("pokemon event transféré")
                myPhone.Press(550,1200) # on clique sur ok pour le transferer 
            else : 
                print(img[900][90],img[900][1000],img[1440][90],img[1440][1000])
        

        

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def mask_on(img,lower,upper): # fonction pour isoler une certaine brochette de couleur 
    lower_range = np.array(lower)  # Set the Lower range value of color in BGR
    upper_range = np.array(upper)   # Set the Upper range value of color in BGR
    mask = cv.inRange(img,lower_range,upper_range) # Create a mask with range
    result = cv.bitwise_and(img,img,mask = mask)  # Performing bitwise and operation with mask in img variable
    return result

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""enlever les pixels qui représentent le joueur"""
def find_smth(img) : # fonction qui va trouver qqch si y'a un certain nombre de pixel noir a côté les uns des autres 
    
    def somme(liste) : # fonction qui sert a faire la somme de tous les éléments d'une liste 2 dimensions
        total = 0
        for row in range (len(liste)):
            for col in range(len(liste[0])):
                total = total + liste[row][col]
        return(total)


    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY) # on transforme les couleurs en nuances de gris 
    
    for i in range(len(gray)): # on parcoure toute l'image 
        for j in range(len(gray[i])):
            if gray[i][j] == 0 : # si le pixel est noir alors on va regarder des pixels aux alentours 
                # trois possibilités d'alentours, un carré, ou deux rectangle (un plus long et un plus large)
                # le carré fait 15*15 pixels et les rectangle font 20*11 ou 11*20
                if (somme(gray[i:i+15,j:j+15].tolist())/len(gray[i:i+15,j:j+15])) <= 10 : # on regarde si la moyenne des pixels vaut moins de 10 (noir quoi)
                    #print("carré ici",print(j,1079+i))
                    return(j,1079+i)
                elif (somme(gray[i:i+20,j:j+11].tolist())/len(gray[i:i+20,j:j+11])) <= 10 :
                    #print("rectangle ici", print(j,1079+i))
                    return(j,1079+i)
                elif (somme(gray[i:i+11,j:j+20].tolist())/len(gray[i:i+11,j:j+20])) <= 10 :
                    #print("rectangle ici", print(j,1079+i))
                    return(j,1079+i)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""rajouter un moyen de savoir quand c'est mode nuit"""
def map_mask_on(img):
    img = img[1079:1878,:,:] # on récupère qu'une certaine partie de l'écran parce que l'écran en entier est inutile
    
    
    green = mask_on(img,(80,200,80),(220,255,200))     # On chope le vert BGR
    grey = mask_on(img,(120,130,50),(190,200,130))    # On chope le gris  BGR
    yellow = mask_on(img,(130,200,145),(200,255,255))  # On chope le jaune BGR
    """
    green = mask_on(img,(80,100,20),(220,180,130))     # On chope le vert BGR NUIT
    grey = mask_on(img, (110,70,30),(200,130,160))  # On chope le gris BGR NUIT
    yellow = mask_on(img,(110,130,140),(220 ,210,240))  # On chope le jaune BGR NUIT 
    
    """
      
    img = cv.addWeighted(green, 1, grey, 1, 0) # fusion de deux images 
    img = cv.addWeighted(img, 1, yellow, 1, 0) # image avec les filtres 
    return(img)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def ecran_jeu(image) : # fonction disant si on est sur l'écran de jeu ou non 
    result = False 
    image = image[1778:,329:774,:] # on découpe un zone en bas de l'écran 
    image=cv.cvtColor(image,cv.COLOR_BGR2GRAY) # on transforme les couleurs en nuances de gris 
    for i in range(70,len(image))[::4] : # on parcoure toutes les couleurs de pixels 
        for j in range(len(image[i]))[::5]:
            if is_approx_nbr(image[i][j],255,5) : # on cherche un pixel blanc 
                if is_approx_nbr(image[i-70][j],118,5) : # on cherche un pixel rouge 
                    if is_approx_nbr(image[i-35][j],185,5) : # on cherche un pixel gris 
                        result = True 
    return(result)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

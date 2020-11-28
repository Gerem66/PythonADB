# =============================================================================
# Liste des fonctions opérationnelle pour Pokémon Go Bot
# =============================================================================
import cv2 as cv
import numpy as np
from ADBLib import SmartPhone as SP
import time
myPhone = SP(r"..\platform-tools") # Chemin absolu ou relatif depuis ce script

press = True # variable qui dit si on simule les clics ou non d
fonction = False # variable qui dit qu'on affiche l'activation des print au début de chaque fonction 


"""machine learning pour reconnaitre pokemon pokestop arène montgolfière et pokestop rocket"""
"""appliquer ordre importante arène > pokestop > pokemon"""
"""revoir le fonctionnement du main"""
"""arene capter bouton combat/depot ou rien et agir en conséquences"""

"""filtrer cercle couleur pour déterminer quel ball prendre"""
"""encens fait beuger les filtres"""
"""montgolfiere team rocket"""
"""combat team rocket"""
"""pokemon pas au centre terrain"""
"""lecture IV nouvelle fonction"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# =============================================================================
"""fonctions pour le non ingame direct mais qui servent au ingame"""
# =============================================================================
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
            return(False)
    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def is_approx_nbr(a,b,delta): # fonction qui regarde si deux nombres sont environ égaux 
    result = False 
    if b >= a - delta and b <= a + delta : 
        result = True 
    else : 
        result = False 
    return(result)   

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def is_identical(list_a, list_b): # fonction qui regarde si deux listes sont identiques 
    if len(list_a) != len(list_b):
        return False
    for i in list_a:
        if i not in list_b:
            return False
    return True
    
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def mask_on(img,lower,upper): # fonction pour isoler une certaine brochette de couleur 
    lower_range = np.array(lower)  # Set the Lower range value of color in BGR
    upper_range = np.array(upper)   # Set the Upper range value of color in BGR
    mask = cv.inRange(img,lower_range,upper_range) # Create a mask with range
    result = cv.bitwise_and(img,img,mask = mask)  # Performing bitwise and operation with mask in img variable
    return result

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def imagesearch(image, searched, mask_blanc = False, precision=0.8): # fonction pour chercher un élément dans une image 
    # image étant l'image que l'on cherche 
    # serched étant l'image sur laquelle on cherche 

    
    template = cv.imread(image) # on lis la photo du truc qu'on cherche 

    test_gray = searched
    
    if mask_blanc : 

        test_gray = mask_on(searched,(235,235,235),(255,255,255))
        template = mask_on(template,(250,250,250),(255,255,255))
        #cv.imwrite("test.png",test_gray)

    

    test_gray = cv.cvtColor(test_gray, cv.COLOR_BGR2GRAY) # on met le screen du téléphone en nuances gris
    template = cv.cvtColor(template, cv.COLOR_BGR2GRAY) # on met le screen du téléphone en nuances gris 
    """
    cv.imshow('gris',test_gray)
    
    cv.imshow("image",template)
    cv.waitKey(0)
    """
    """
    #template.shape[::-1] # oui 
    #template = template[:, :, 0]
    print((template))
    print((template2))
    """
    h,l = int(template.shape[0]/2), int(template.shape[1]/2) # on récupère la moitié de hauteur et largeur de l'image 


    res = cv.matchTemplate(test_gray, template, cv.TM_CCOEFF_NORMED) # on regarde si ca matche 
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res) # on fait des trucs 


    
    if max_val < precision: # si ca matche pas 
        return [-1, -1] # on renvoie -1 -1 
    hauteur, largeur = max_loc[0] + h, max_loc[1]+l  # on choppe la donnée en lui rajoutant la moitié des dim de l'image pour cliquer au milieu 
    
    

    return (hauteur,largeur) # si ca match on renvoie la valeur haut gauche 


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def imagesearcharea(image,searched,x1,y1,x2,y2,mask_blanc= False,precision=0.8): # fonction pour chercher un élément dans une zone précise d'une image 
    # image étant l'image que l'on cherche 
    # serched étant l'image sur laquelle on cherche 
    # x1,y1 point haut gauche 
    # x2,y2 point bas droit 
    new = searched[y1:y2,x1:x2,:] # on coupe l'image là ou on veut 
    #cv.imshow("image",new) # utile pour débeuger 
    #cv.waitKey(0) 
    #print("mask blanc f2 : ",mask_blanc)
    """
    if image == r"item\arene_bleu.png" : # si c'est bleu on va appliquer un masque bleu 
        print("oui")
        image_test = cv.imread(image)
        image_test = mask_on(image_test,(245,60,60),(255,70,70)) #BGR
        cv.imwrite(image,image_test)
    """
    

    x,y = imagesearch(image,new,mask_blanc) # on récup les données 
    
    if x == -1 or y == -1 : # maintenant il faut rajouter ce qu'on a enlevé sauf si c'est -1 return
        return(-1,-1)
    else : 
        return(x+x1,y+y1)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def find_images_screenshot(img,*image_pose): # fonction servant à trouver une ou plusieurs images et retournant si elles sont bien là (True or False)
    result = False # de base a faux au cas où 
    table_result = [] # tableau dans lequel on va sauvegarder les points haut gauche de l'image trouvée 
    for i in range(len(image_pose)) : # on va parcourir la liste des arguments 
        if len(image_pose[i]) != 5 and len(image_pose[i]) != 6 : print("ERREUR : pas bon argument find_images_screenshot")
        name = "item\\"+image_pose[i][0]             
        x1 = image_pose[i][1]
        y1 = image_pose[i][2]
        x2 = image_pose[i][3]
        y2 = image_pose[i][4]
        try : 
            mask_blanc = image_pose[i][5]
        except : 
            mask_blanc = False 
        x,y = imagesearcharea(name, img, x1,y1,x2,y2,mask_blanc) # on va chercher l'image dans la position donnée 
        table_result.append(x) # on ajoute les résultats dans le tableau 
        table_result.append(y)
        #print(image_pose[i][0],x,y)
    
    for j in table_result : # maintenant on parcoure la liste avec tous les résultats 
        if j != -1 : result = True # on va regarder si toutes les infos sont différentes de -1 
        else : return False # si juste une vaut -1 alors on dégage 
        
    return(result)
    
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""fonction servant directement in game"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# =============================================================================
"""fonction check endroit"""
# =============================================================================
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def check_cbt(img) : # fonction qui sert a checker si on est en combat ou non 
    """
    result = False 
    if is_approx(img[260][100], [250, 250, 250],10) and is_approx(img[2000][120], [122, 73, 215],20) and is_approx(img[1980][950], [30, 50, 203],20) : 
       result = True 
    else : 
        result = False 
    """
    """
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran 
    x,y = imagesearcharea("bonhomme.png", img, 0, 0, int(1/3 * l),int( 1/5*h))# on va chercher l'icone du bonhomme qui s'échappe 
     
    if x == -1 and y == -1 : # là on a pas trouvé 
        result = False 
    else : # là on a trouvé 
        result = True 
    return(result)
    """
    if fonction : print("fonction check combat")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    result = find_images_screenshot(img, ["bonhomme.png", 0, 0, int(1/3 * l),int( 1/5*h),True],["berry.png",0, int(4/5*h), int(1/3 * l),int(h)])
    return(result)

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
    """
    """
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    a,b = imagesearcharea("total.png", img, int(0), int(h- 1/2*h), int(1/2 * l),int(h))# on va chercher le mot TOTAL
    x,y = imagesearcharea("ok_new_pkm.png", img, int(1/3 * l), int(h- 1/2*h), int(2/3 * l),int(h))# on va chercher le OK s
    #print("after_catch : ",x,y,a,b)
    if x == -1 or y == -1 or a == -1 or b == -1 : # là on a pas trouvé 
        result = False 
    else : # là on a trouvé 
        result = True 
        if press : myPhone.Press(x,y)
    return(result)
    """
    if fonction : print("fonction after catch")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    result = find_images_screenshot(img, ["total.png", int(0), int(h- 1/2*h), int(1/2 * l),int(h)],["ok_new_pkm.png",int(1/3 * l), int(h- 1/2*h), int(2/3 * l),int(h)])
    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def pos_ok_cbt(img) : # fonction qui dit où est le OK de après les combats 

    if fonction : print("fonction pos ok combat ")
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    x,y = imagesearcharea(r"item\ok_new_pkm.png",img, int(1/3 * l), int(h- 1/2*h), int(2/3 * l),int(h))

    return(x,y)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def fiche_pkm(img) : # fonction qui regarde si on est sur la fiche pokemon 
    """
    result = False
    if is_approx(img[900][40], [250, 250, 250],10) and is_approx(img[900][1040], [250, 250, 250],10) : # 2 points du haut (toujours au même endroit)
        if is_approx(img[2100][540], [150, 135, 28],10) and is_approx(img[2040][540], [150, 135, 28],10) : # 2 points du haut (toujours au même endroit)
            result = True 
            
    return(result)
    """
    """
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran 
    x,y = imagesearcharea("option_pkm.png", img, int(2/3 * l), int(4/5*h), int(l),int(h))# on va chercher les 3 barres 
    a,b = imagesearcharea("appareil_photo.png", img, int(2/3 * l), 0, int(l),int(1/5*h))# on va chercher les 3 barres
    c,d = imagesearcharea("favori.png", img, int(2/3 * l), int(0), int(l),int(1/5*h))# on va chercher les 3 barres
    #print("fiche : ",x,y,a,b,c,d)
    if x == -1 or y == -1 or a == -1 or b == -1 or c == -1 or d == -1 : # là on a pas trouvé 
        result = False 
    else : # là on a trouvé 
        result = True 
    return(result)
    """
    if fonction : print("fonction fiche pokemon")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    #result = find_images_screenshot(img, ["option_pkm.png", int(2/3 * l), int(4/5*h), int(l),int(h)],["appareil_photo.png",  int(2/3 * l), 0, int(l),int(1/4*h),True],["favori.png", int(2/3 * l), int(0), int(l),int(1/5*h),True])
    result = find_images_screenshot(img, ["option_pkm.png", int(2/3 * l), int(4/5*h), int(l),int(h)])
    return(result)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def on_pkstop(img) : # fonction qui valide si on est sur un pokestop ou non
    """
    result = False 
    
    #print(img[2100][100],img[2100][1000],img[2180][540])
    # on check trois points qui sont censés etre bleu 
    if is_approx(img[2100][100], [237, 126, 32],10) and is_approx(img[2100][1000], [237, 126, 32],10) and is_approx(img[2180][540], [237, 126, 32],10) : 
        result = True
    elif is_approx(img[2100][100], [217, 88, 106],10) and is_approx(img[2100][1000], [217, 88, 106],10) and is_approx(img[2180][540], [217, 88, 106],10) : 
        result = True
    """
    """
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    x,y = imagesearcharea(r"item\bouton_quitter.png", img, int(1/3 * l),int(4/5*h) , int(2/3*l),int(h)) # on choppe les coordonnées du du milieu du bouton 
    print(x,y)
    if is_approx(img[y][x], [250, 135, 215],5) or is_approx(img[y][x], [219, 102, 33],5) :
        result = True 
    else : 
        return False 
    """
    if fonction : print("fonction on pokestop")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    result = find_images_screenshot(img, ["bouton_pokestop.png", int(2/3 * l), int(0), int(l),int(1/5*h)],["bouton_quitter.png",  int(1/3 * l),int(4/5*h) , int(2/3*l),int(h)])
    
    
    return(result)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def on_arene(img) : # fonction qui valide si on est sur une arène ou non en sachant qu'on est déjà sur un pokestop
    """
    result = False 
    
    #print(img[2100][100],img[2100][1000],img[2180][540])
    # on check trois points qui sont censés etre bleu 
    if is_approx(img[2100][100], [237, 126, 32],10) and is_approx(img[2100][1000], [237, 126, 32],10) and is_approx(img[2180][540], [237, 126, 32],10) : 
        result = True
    elif is_approx(img[2100][100], [217, 88, 106],10) and is_approx(img[2100][1000], [217, 88, 106],10) and is_approx(img[2180][540], [217, 88, 106],10) : 
        result = True
    """
    # on sait qu'on est sur un pokestop donc probablement une arène, plus qu'a checker le rond en haut a gauche 
    
    
    
    """ try avec les cercles haut gauche mais rien marche wesh 
    x1,y1 = imagesearcharea( r"item\ar_bleu.png", img, int(0), int(0), int(1/3*l),int(1/4*h),False)# on va chercher les 3 barres 
    x2,y2 = imagesearcharea(r"item\arene_rouge.png", img, int(0), int(0), int(1/3*l),int(1/4*h))# on va chercher les 3 barres 
    x3,y3 = imagesearcharea(r"item\arene_jaune.png", img, int(0), int(0), int(1/3*l),int(1/4*h))# on va chercher les 3 barres 
    x1,y1 = imagesearch( r"item\ar_bleu.png", img)
    x2,y2 = imagesearch( r"item\arene_bleu.png", img)
    print("arène : ",x1,y1,x2,y2,x3,y3)   
    


    if x1 != -1 and y1 != -1 or x2 != -1 and y2 != -1 or x3 != -1 and y3 != -1 : # on regarde si on a chopé un des trois cercles 
        result = True # si on a un des trois alors on est sur une arène 
    else : 
        result = False 
        
    """
    if fonction : print("fonction on arene")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
    x,y = imagesearcharea(r"item\pokestop_arene.png",img, int(2/3 * l), int(4/5*h), int(l),int(h))
    
    if x == -1 or y == -1 : # si on n'a pas trouvé le premier type de pokestop, on regarde le second type
        x,y = imagesearcharea(r"item\pokestop_ar_raid.png",img, int(2/3 * l), int(4/5*h), int(l),int(h),True)


    
    a,b = imagesearcharea(r"item\bouton_quitter.png",img, int(1/3 * l), int(4/5*h), int(2/3*l),int(h))
    if x == -1 or y == -1 or a == -1 or b == -1  : 
        return False 
    else : 
        #print("oui arène")
        result = True 
        myPhone.Press(x,y)
        time.sleep(1)
        myPhone.Swipe(1000,1150,100,1150,100)
        time.sleep(0.3)
        myPhone.Press(a,b)
        
    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""fonction ne servant pas"""
def level_up(img) : # fonction qui dis si on level up ou pas 
    """
    result = False 
    
    if is_approx(img[734][100], [255, 255, 255],10) : # on regarde si un premier pixel est la 
    # s'il est la, on check tous les autres 
        if is_approx(img[734][200], [255, 255, 255],10) and is_approx(img[734][300], [255, 255, 255],10) and is_approx(img[734][100], [255, 255, 255],10) and is_approx(img[734][200], [255, 255, 255],10) and     is_approx(img[734][300], [255, 255, 255],10) : 
            result = True 
    
    return(result)
    """
    if fonction : print("fonction level up")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran 
    x,y = imagesearcharea(r"item\ok_lvl_up.png", img, int(0), int(4/5*h), int(l),int( h))# on va chercher l'icone du bonhomme qui s'échappe 
     
    #print("lvl up : ",x,y)
    
    if x == -1 or y == -1 : # là on a pas trouvé 
        result = False 
    else : # là on a trouvé 
        result = True 
    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def ecran_jeu(img) : # fonction disant si on est sur l'écran de jeu ou non 
    """
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
    """
    
    """
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran 
   
    x,y = imagesearcharea(r"item\menu_pokmn.png", img, int(1/3*l), int(4/5*h), int(2/3*l),int( h))# on va chercher l'icone du bonhomme qui s'échappe 
    a,b = imagesearcharea(r"item\cardinal.png", img, int(2/3*l), int(0), int(l),int( 1/4*h))# on va chercher l'icone du bonhomme qui s'échappe 

    if x == -1 or y == -1 : # là on a pas trouvé 
        result = False 
    else : # là on a trouvé 
        result = True 
    """
    
    if fonction : print("fonction ecran jeu")
    result = False # de base a faux au cas où 
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran 
    

    result = find_images_screenshot(img, ["menu_pkm_blanc.png", int(1/3*l), int(4/5*h), int(2/3*l),int( h),True],["cardinal_blanc2.png",  int(2/3*l), int(0), int(l),int( 1/4*h), True])


    return(result)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# =============================================================================
"""fonction servant en combat """
# =============================================================================
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def check_circle() : # fonction qui permet de regarder ou est le cercle du pokemon
    if fonction : print("fonction check circle")
    (x,y) = (0,0)
    while x==0 and y == 0 : # tant qu'on a pas la valeur du centre du cercle 
        img = myPhone.TakeScreenshotWithPress(550,2000) 
        #cv.imwrite("test_rond_blanc.png",img)
        img=img[300:1800,:]
        cv.imwrite("test_combat.png",img)
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
        cv.imwrite("test_combat_circle.png",output)
    return(int(x),int(y+300)) # on retourne le centre du cercle 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def lance_pkb(x,y):
    if fonction : print("fonction lance pkb combat")
    #myPhone.Swipe(500,2100,500,1200,200)
    myPhone.Swipe(500,2100,500,int(y- (y*(9/100))),200)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# =============================================================================
"""fonction pour voir le pokemon attrapé et faire des bails (relacher/évaluer) """
# =============================================================================
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def lecture_IV(img): # fonction qui permet de lire les IV du pokémon
    """
    etoile = 0
    time.sleep(0.4) # on attend un peu histoire que les options apparaissent 
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
    """
    if fonction : print("fonction Lecture IV")
    etoile = 0
    h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran 
    time.sleep(0.4) # on attend un peu histoire que les options apparaissent 
    x,y = imagesearcharea("item\option_pkm.png", img, int(2/3 * l), int(4/5*h), int(l),int(h))# on va chercher les 3 barres 
    myPhone.Press(x,y) # on clique dessus 
    time.sleep(0.4) # on attend un peu histoire que les options apparaissent 
    img = myPhone.TakeScreenshot() # prend un screenshot pour scanner 
    x,y = imagesearcharea("item\evaluer.png", img, int(2/3 * l), int(1/2*h), int(l),int(h))# on va chercher le bouton évaluer 
    myPhone.Press(x,y) # on clique dessus 
    time.sleep(0.2) # on attend vite fait 
    myPhone.Press(x,y) # on clique pour passer à l'éval 
    time.sleep(1) # on attend un peu histoire que les options apparaissent 
    img = myPhone.TakeScreenshot() # prend un screenshot pour scanner 
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
def relache(cran_etoile=-1, etoile=-2,pkm_event = False): # fonction qui permet de relacher le pokemon en fonction d'un cran d'étoiles placé au préalable
    if fonction : print("fonction relache ou non")
    if etoile < cran_etoile : # si le nombre d'étoile du pokemon est inférieur au cran, alors on le relache
        time.sleep(0.2) # on attend un peu histoire que les options apparaissent     
        if press : myPhone.Press(930,2100) # on appui sur le bouton avec 3 barres 
        time.sleep(0.2) # on attend un peu histoire que les options apparaissent 
        if press : myPhone.Press(850,1850) # on clique sur transferer
        time.sleep(0.2) # on attend un peu 
        if press : myPhone.Press(550,1300) # on clique sur ok
        if pkm_event : # si on a décidé de transférer les pkm event
            time.sleep(0.4) # on attend un peu 
            img = myPhone.TakeScreenshot() # prend un screenshot pour regarder si y'a encore qqch 
            # on regarde si y'a le truc pour pokemon evenement 
            if is_approx(img[900][90], [255, 255, 255],10) and is_approx(img[900][1000], [255, 255, 255],10) and  is_approx(img[1440][90], [255, 255, 255],10) and  is_approx(img[1440][1000], [255, 255, 255],10) : 
                print("pokemon event transféré")
                if press : myPhone.Press(550,1200) # on clique sur ok pour le transferer 
            else : 
                print(img[900][90],img[900][1000],img[1440][90],img[1440][1000])
        
    else : # s'il a assez d'étoile, alors on le garde 
        if press : myPhone.Press(540,2050) # on clique sur ok
        

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ========================================================================================
""" THE fonction / DA fonction, qui sert à chercher les pokémons/arènes/pokestop/etc.. """
# ========================================================================================
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def find_smth(img) : # fonction qui va trouver qqch si y'a un certain nombre de pixel noir a côté les uns des autres 
    if fonction : print("fonction find something")
    def somme(liste) : # fonction qui sert a faire la somme de tous les éléments d'une liste 2 dimensions
        total = 0
        for row in range (len(liste)):
            for col in range(len(liste[0])):
                total = total + liste[row][col]
        return(total)
    print("entre find something ")
    x,y=0,0
    gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY) # on transforme les couleurs en nuances de gris 
    cv.imwrite("image_grise.png",gray)
    for i in range(len(gray)): # on parcoure toute l'image 
        for j in range(len(gray[i])):
            if gray[i][j] == 0 : # si le pixel est noir alors on va regarder des pixels aux alentours 
                # trois possibilités d'alentours, un carré, ou deux rectangle (un plus long et un plus large)
                # le carré fait 15*15 pixels et les rectangle font 20*11 ou 11*20
                if (somme(gray[i:i+15,j:j+15].tolist())/len(gray[i:i+15,j:j+15])) <= 10 : # on regarde si la moyenne des pixels vaut moins de 10 (noir quoi)
                    #print("carré ici",print(j,1079+i))
                    x,y=(j,1079+i)
                elif (somme(gray[i:i+20,j:j+11].tolist())/len(gray[i:i+20,j:j+11])) <= 10 :
                    #print("rectangle ici", print(j,1079+i))
                    x,y=(j,1079+i) 
                elif (somme(gray[i:i+11,j:j+20].tolist())/len(gray[i:i+11,j:j+20])) <= 10 :
                    #print("rectangle ici", print(j,1079+i))
                    x,y=(j,1079+i)
                if press : myPhone.Press(x,y) # et on clique dessus 
                if press : myPhone.Press(15+x,15+y) # et on clique dessus
    print("sort find something ")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# ========================================================================================
""" Autre truc """
# ========================================================================================
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""rajouter un moyen de savoir quand c'est mode nuit"""
def map_mask_on(img):
    img = img[1079:1878,:,:] # on récupère qu'une certaine partie de l'écran parce que l'écran en entier est inutile
    cv.imwrite("photo_avant_filtre.png",img)
    """
    green = mask_on(img,(80,200,80),(220,255,200))     # On chope le vert BGR
    grey = mask_on(img,(120,130,50),(190,200,130))    # On chope le gris  BGR
    yellow = mask_on(img,(130,200,145),(200,255,255))  # On chope le jaune BGR
    """
    """
    green = mask_on(img,(80,100,20),(220,180,130))     # On chope le vert BGR NUIT
    grey = mask_on(img, (110,70,30),(200,130,160))  # On chope le gris BGR NUIT
    yellow = mask_on(img,(110,130,140),(220 ,210,240))  # On chope le jaune BGR NUIT
    """
    
    green_light =  mask_on(img,(80,100  ,50),(165,150,120)) # On chope le vert clair BGR NUIT
    green_dark = mask_on(img,(90,65,0),(130,100,10)) # On chope le vert foncé  BGR NUIT
    building = mask_on(img,(140,140,55),(200,170,100)) # On chope les batiments BGR NUIT
    building_boundaries = mask_on(img,(140,140,100),(180,170,125)) # On chope les batiments BGR NUIT
    road = mask_on(img,(150,180,110),(160,190,120)) # On chope les routes BGR NUIT
    road_boundaries = mask_on(img,(110,75,35),(145,95,50)) # On chope les bordures des routes BGR NUIT
    pokestop_violet = mask_on(img,(216,87,90),(218,89,120)) # On chope les pokestop BGR NUIT
    pokestop_rose = mask_on(img,(250,170,250),(255,185,255)) # On chope les pokestop BGR NUIT

    
    
    """ 
    img = cv.addWeighted(green, 1, grey, 1, 0) # fusion de deux images 
    img = cv.addWeighted(img, 1, yellow, 1, 0) # image avec les filtres 
    """
    
    img = cv.addWeighted(green_light, 1, green_dark, 1, 0) # image avec les filtres 
    img = cv.addWeighted(img, 1, building, 1, 0) # image avec les filtres
    img = cv.addWeighted(building_boundaries, 1, img, 1, 0) # image avec les filtres
    img = cv.addWeighted(road, 1, img, 1, 0) # image avec les filtres
    img = cv.addWeighted(road_boundaries, 1, img, 1, 0) # image avec les filtres
    img = cv.addWeighted(pokestop_rose, 1, img, 1, 0) # image avec les filtres
    img = cv.addWeighted(pokestop_violet, 1, img, 1, 0) # image avec les filtres
    
    # on va juste remplacer tous les pixels autour du joueur par des pixels blancs histoire de pas confondre joueur et pkm
    for i in range(290,410) : 
        for j in range(500,580) :
            img[i][j] = [255,255,255]

    
    cv.imwrite("photo_filtre.png",img)
    return(img)



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def pokestop(): # fonction qui fait tourner le pokestop 
    if fonction : print("fonction pokestop")
    time.sleep(0.4)
    myPhone.Swipe(1000,1150,100,1150,100)
    time.sleep(0.2)
    myPhone.Press(540,2060)
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def quit_lvl_up(): 
    if fonction : print("fonction quit level up ")
    if press : myPhone.Press(540,1950)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def arene():#on pose/combat/fait qqch jsp moi
    if fonction : print("fonction arene") 
    time.sleep(1)
    myPhone.Press(540,2060)

    



""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

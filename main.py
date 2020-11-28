from fonction_in_game import *

from ADBLib import SmartPhone as SP


myPhone = SP(r"..\platform-tools") # Chemin absolu ou relatif depuis ce script
lec_iv = True # variable disant si on lis des IV ou non 
transfert = True # variable disant si on transfert des pokémons ou non 
cran_etoile = 3 # variable donnant le cran a partir duquel les pokémons a trop bas IV sont relachés 
pkm_event = True # variable servant a dire si on veut relacher les pokémons event qu'on vient d'attraper 
Alive = True
rien = 0 # variable qui dit le nombre de fois ou rien ne se passe 
while Alive:
    try : 
        img = myPhone.TakeScreenshot() # on prend un screenshot d'abord
        
        #img=cv.imread("temp\level_up.jpg")
        #cv.imshow("test",img)

        if ecran_jeu(img) : # si on est sur l'écran de jeu
            rien = 0
            print("écran du jeu")
            #(find_smth(map_mask_on(img))) # alors on cherche qqch et on clique dessus 
            
            
        if check_cbt(img) : # on regarde si on est bien en combat 
            rien = 0
            print("on rentre en combat")
            combat = True
            compteur = 0 # compteur qui va servir a dire si le pokémon s'est enfui ou non
            nombre_ball = 0 # compteur qui compte le nombre de balle utilisée sur le pokemon 
            while combat : 
                
                time.sleep(2)
                img = myPhone.TakeScreenshot()
                print("procedure de combat",compteur)
                while check_cbt(img):
                    compteur = 0 # on remet le compteur a 0 car il se passe qqch 
                    print("en combat")
                    a,b = check_circle()
                    lance_pkb(a,b)
                    img = myPhone.TakeScreenshot() # pour regarder si le pokemon a bougé 
                    #cv.imwrite('test.png',img)
                    nombre_ball = nombre_ball + 1 
                    if nombre_ball >= 10 : # si on a eu plus de 10 essais, trop galère on dégage 
                        break
                    
                while after_catch(img) : 
                    compteur = 0 # on remet le compteur a 0 car il se passe qqch 
                    img = myPhone.TakeScreenshot() # pour voir si y'a bien le ok, et oui il est 
                    print("attrapé")
                    x,y = pos_ok_cbt(img) # on cherche l'emplacement du ok
                    myPhone.Press(x,y) # on clique dessus 
                    time.sleep(1)
                    
                while fiche_pkm(img) : 
                    compteur = 0 # on remet le compteur a 0 car il se passe qqch 
                    print("sur la fiche")
                    if lec_iv : # on lis les IV 
                        print("on veut lire l'iv")
                        etoile = lecture_IV(img)
                    if transfert and lec_iv : # on relache les pokémon en fonction de leur iv
                        print("on veut peut etre le transferer le pokemon car il a ",etoile)
                        relache(cran_etoile,etoile,pkm_event)
                    if transfert and not lec_iv : # on relache les pokemons peut importe leur IV 
                        print("on transfère peut importe l'IV")
                        relache()
                        #myPhone.Press(540,2080)
                        # finir fonction et rajouter clic 
                    img = myPhone.TakeScreenshot()
                    combat = False 
                    
                compteur = compteur + 1 
                if compteur >= 8 : 
                    print("pokemon enfuit")
                    combat = False 
                if nombre_ball >= 10 : # si on a eu plus de 10 essais, trop galère on dégage 
                        break
            print("on sort du combat et du traitement")
            
            
            
        if on_pkstop(img):# on regarde si on est sur un pokestop OU arène 
            rien = 0
            print("pokestop ou arène")
            if on_arene(img) : # on check si c'est une arène 
                print("arène") # on va regarder si on peut poser un pkm sachant que le pokestop a déjà été tourné 
                arene()
            else : # sinon, c'est un pokestop 
                print("pokestop")
                pokestop()
         
            
        if rien >= 5 : 
            h, l = len(img),len(img[0]) # on choppe la longueur et la largeur de l'écran
            myPhone.Press(int(l/2),int(h/2))
            rien = 0 
        rien = rien + 1 
        print("rien ne se passe depuis : ",rien)
        time.sleep(0.5)
    except KeyboardInterrupt:
        Alive = False

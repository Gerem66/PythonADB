from fonction_pogo import *

from ADBLib import SmartPhone as SP


myPhone = SP(r".\platform-tools") # Chemin absolu ou relatif depuis ce script
lec_iv = True # variable disant si on lis des IV ou non 
transfert = True # variable disant si on transfert des pokémons ou non 
cran_etoile = 3 # variable donnant le cran a partir duquel les pokémons a trop bas IV sont relachés 
pkm_event = False # variable servant a dire si on veut relacher les pokémons event qu'on vient d'attraper 
Alive = True
while Alive:
    try : 
        img = myPhone.TakeScreenshot() # on prend un screenshot d'abord
    
        if ecran_jeu(img) : # si on est sur l'écran de jeu
            print("écran du jeu")
            x,y = (find_smth(map_mask_on(img))) # alors on cherche un pokémon 
            myPhone.Press(x,y) # et on clique dessus 
            myPhone.Press(15+x,15+y) # et on clique dessus 
            
        if check_cbt(img) : # on regarde si on est bien en combat 
            print("en combat")
            a,b = check_circle()
            lance_pkb(a,b)
            
        if after_catch(img):
            print("attrapé")
            myPhone.Press(543,1500) # et on clique dessus 
            # rajouter le fait de presser les coordonnées pour appuer sur bouton OK
            
        if fiche_pkm(img) : 
            print("sur la fiche")
            if lec_iv : # on lis les IV 
                print("on veut lire l'iv")
                etoile = lecture_IV()
            if transfert and lec_iv : # on relache les pokémon en fonction de leur iv
                print("on veut transferer le pokemon car il a ",etoile)
                relache(cran_etoile,etoile)
            if transfert and not lec_iv : # on relache les pokemons peut importe leur IV 
                print("on transfère peut importe l'IV")
                relache()
            #myPhone.Press(540,2080)
            # finir fonction et rajouter clic 

    except KeyboardInterrupt:
        Alive = False


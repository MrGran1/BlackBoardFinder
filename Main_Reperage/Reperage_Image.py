import numpy as np
import cv2

from Reperage_Tableau import *

def reperageImage(i, dilatation, img):
    """
    Fonction qui classe les éléments de l'image par rapport à Reperage_Tableau. Si l'élément est en dehors du tableau on le met en noir.
    """
    new_img = img.copy()
    tab = reperage_tab(i, "Train")
    tab = tab.astype(np.uint8)

    # On récupère les dimensions de l'image
    h, w = img.shape[:2]

    # On récupère les dimensions du tableau
    hTab, wTab = tab.shape[:2]

    # On parcourt l'image et on regarde si le pixel est dans le tableau. Si non on le met en noir
    # Grace a dilatation qui contient le texte dilaté repéré, 
    # si le pixel est dans le tableau et que c'est du texte, on le met en gris, sinon en blanc
    for y in range(h):
        for x in range(w):
            if tab[int(y*hTab/h)][int(x*wTab/w)] == 0: # Si le pixel est en dehors du tableau
                new_img[y][x] = 0
            elif dilatation[y][x] == 255:              # Si le pixel est dans le tableau et que c'est du texte
                new_img[y][x] = 128
            else:                                      # Si le pixel est dans le tableau et que ce n'est pas du texte
                new_img[y][x] = 255

    return new_img
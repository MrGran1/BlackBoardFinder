import numpy as np
import cv2
import matplotlib.image as pltimg
import matplotlib.pyplot as plt

from Seuil_Couleur import *
from Fonctions_de_base import *
from Reperage_Tableau import *
from Reperage_Elements_Tab import *
from Evaluation import *

    

def main():

    i = 60
    img = pltimg.imread("D:/Dossier_chelou/Users/kelli/Documents/GitHub/Projet-Image-Suicide-Squad-/Images_Train_et_test/Entrainement_(57)/" + str(i) + ".jpg")
    vt_img = pltimg.imread("D:/Dossier_chelou/Users/kelli/Documents/GitHub/Projet-Image-Suicide-Squad-/Json/" + str(i) + "VT/label.png")

    #1 Repérage tableau de l'image
    print("Conversion en gris (en cours...)")
    tab = convGris(img)
    print("Binarisation (en cours...)")
    seuilCentre(tab)
    print("Conexite 4 (en cours...)")
    tab = connexite4(tab)

    #2 Repérage éléments blancs du tableau avec le seuillage
    elemV1 = seuilTexteBlanc(img)

    #3 On combine 1 et 2 pour enlever les éléments blancs qui ne sont pas dans le tableau
    print("RepElemsBlancsAmelio (en cours...)")
    elemV2 = RepElemsBlancsAmelio(tab, elemV1)

    #4 On dilate le résultat final pour convenir avec la VT
    print("Dilatation de l'image final (en cours...)")
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))  # nombre à gauche augmente horizontalement et à droite verticalement les formes blanches
    dilation = cv2.dilate(elemV2, rect_kernel, iterations = 5)         # iterations augmente de façon homogène les formes blanches

    #5 AFFICHAGE
    # Affichage de la dilatation
    plt.figure()
    plt.subplot(2, 3, 1)  
    plt.imshow(dilation, cmap='gray')
    plt.title('Étape 4-Dilatation')

    # Affichage de la VT de cette image
    plt.subplot(2, 3, 2)  
    plt.imshow(vt_img, cmap='gray')
    plt.title('Étape 5-Comparaison VT')

    # Affichage Image de base
    plt.subplot(2, 3, 3) 
    plt.imshow(img)
    plt.title('Image de base')

    # Affichage du repérage de tableau
    plt.subplot(2, 3, 4)  
    plt.imshow(tab, cmap='gray')
    plt.title('Étape 1-Repérage Tableau')

    # Affichage du seuillage des elements blancs
    plt.subplot(2, 3, 5)  
    plt.imshow(elemV1, cmap='gray')
    plt.title('Étape 2-Repérage Elements Blancs')

    # Affichage améliorée des elements blancs
    plt.subplot(2, 3, 6)  
    plt.imshow(elemV2, cmap='gray')
    plt.title('Étape 3-Repérage Amélioré Elements Blancs')

    plt.tight_layout()  # Pour éviter les chevauchements
    plt.show()

main()
 
import numpy as np

from collections import deque
from Fonctions_de_base import *

def seuilCentre(img):
    """ Effectue un seuillage sur une image en fonction de la moyenne des pixels du centre de l'image
    param :
    img : numpy array qui represente une image
    """
    #On récupère la couleur du centre de l'image
    couleur = getCouleurCentre(img)
    #On effectue un seuillage avec une marge de 30 au dessus et en dessous
    seuil1= couleur + 30
    seuil2=couleur - 30

    seuil(img,seuil1,seuil2)



def getCouleurCentre(img):
    """ Récupère la couleur la plus dominante au centre de l'image pour récuperer la couleur du tableau"""
    xcentre = int (img.shape[1]/2)  # avant : (img.shape[0]/2)
    ycentre = int(img.shape[0]/2)   # avant : (img.shape[1]/2)
    condition = False
    max = -1
    couleurMax = ""
    nbCouleur = {} # dictionnaire qui contient les couleurs et le nombre de fois qu'elles apparaissent
    #On parcourt les pixels du centre de l'image
    for i in range (ycentre-250, ycentre + 250):       # avant : for j
        for j in range (xcentre-250, xcentre + 250):   # avant : for i
            condition = False

            #On regarde si la couleur du pixel est déjà dans le dictionnaire
            for couleur in nbCouleur.keys():
                #On incrémente la couleur du pixel si elle est proche d'und couleur du dictionnaire de +-20
                if couleur >= img[i,j]-20 and couleur <= img[i,j] + 20 :   # avant : [j,i]
                    nbCouleur[couleur] += 1
                    condition = True
                    break

            if condition == False  :
                nbCouleur[img[i,j]] = 1    # avant : [j,i]

    #On récupère la couleur la plus présente
    for couleur in nbCouleur.keys():
        
        if nbCouleur[couleur] > max:
            couleurMax = couleur
            max = nbCouleur[couleur]
    
    
    return couleurMax 




def connexite4(img):
    h, w = img.shape[:2]
    start = (w // 2, h // 2)

    visited = set()
    visited.add(start)

    q = deque()
    q.append(start)

    imgFinale = np.zeros((h, w), dtype=np.uint8)

    while q:
        i, j = q.popleft()
        imgFinale[j, i] = 255

        for ni, nj in ((i+1, j), (i-1, j), (i, j+1), (i, j-1)):
            if 0 <= ni < w and 0 <= nj < h and (ni, nj) not in visited and img[nj, ni] != 0:
                visited.add((ni, nj))
                q.append((ni, nj))

    return imgFinale




def boucheurDeTrou(bin):
    """ Colorie le maximum de partie noir du tableau en blanc

    param : 
    bin : image binarisée avec déja le tableau repéré
    """
    image_padded = np.zeros((bin.shape[0] + 16, bin.shape[1] + 16), dtype = np.uint8)
    image_padded[8 : -8, 8: -8] = bin 

    resfinal = np.zeros((bin.shape[0], bin.shape[1]), dtype = np.uint8)

    for i in range (bin.shape[0]):
        for j in range(bin.shape[1]):

            if (bin[i,j] == 255):
                resfinal[i,j] = 255

            else :
                ind1 = False
                ind2 = False

                for k in range(j-8,j+8):
                    if ((image_padded[i,k]) == 255) :
                        ind1=True
                        break
                for l in range(i-8,i+8):
                    if ((image_padded[l,j]) == 255) :
                        ind2=True
                        break

                if (ind1 and ind2):
                    resfinal[i,j] = 255
    return resfinal

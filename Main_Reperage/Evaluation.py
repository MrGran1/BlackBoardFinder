import numpy as np
import matplotlib.image as pltimg

from Fonctions_de_base import *
from Reperage_Tableau import *
from Evaluation import *



def binarisationVT_tableau(img):
    """ Binarise la VT du reperage tableau et texte
    param : 
    img : VT sous forme d'image
    """
    new_img = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j,0] > 0.1 or img[i,j,1] > 0.1:
                new_img[i,j] = 255
            else :
                new_img[i,j] = 0
    return new_img




def binarisationVT_tableau_GPT(img):
    threshold = 0.1
    new_img = np.where((img[:,:,0] > threshold) | (img[:,:,1] > threshold), 255, 0).astype(np.uint8)
    return new_img




def binarisationVT_elementsTableau(img):
    """ Binarise la VT du reperage tableau et texte
    param : 
    img : VT sous forme d'image
    """
    new_img = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j,1] > 0.1:
                new_img[i,j] = 255
            else :
                new_img[i,j] = 0
    return new_img



def binarisationVT_elementsTableau_GPT(img):
    threshold = 0.1
    green_channel = img[:, :, 1]
    new_img = np.where(green_channel > threshold, 255, 0).astype(np.uint8)
    return new_img




def taux_reussiteV1(img, vt):
    """ Compare l'image à la VT et renvoie le taux de réussite
    param : 
    img : Image (binarisé) sur laquelle on a appliqué l'algo et qui faut comparer
    vt : verite terrain sous forme d'image (binarisé) à comparer avec img
    """
    total_pixel = img.shape[0]*img.shape[1]
    pixel_correct = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] == vt[i,j] :
                pixel_correct +=1

    taux_reussite = (pixel_correct / total_pixel) * 100

    return taux_reussite

def taux_reussiteV2(img, vt):
    pixel_correct = 0
    total_pixel = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] ==  255 and vt[i,j] == 255 :
                pixel_correct +=1

            if img[i,j] == 255 or vt[i,j] == 255:
                total_pixel += 1


    taux_reussite = (pixel_correct / total_pixel) * 100

    return taux_reussite

def comparaison_images ():
    nbBon = 0
    nbTotal = 0
    for i in range (29,34):
        print (i)
    
        nbTotal += 1
        img = pltimg.imread(r"./Images_Train_et_test/Entrainement_(57)/"+ str(i) +".jpg")
        print("Conversion en gris")
        gris = convGris(img)
        print("Binarisation")
        seuilCentre(gris)
        print("Conexite 4")
        gris = connexite4(gris)
        vt_img = pltimg.imread("./Json/"+ str(i)+"VT" + "/label.png")
        print("Binarisation VT image")
        vt_bin = binarisationVT_tableau(vt_img)
        print("Taux de reussite")
        taux = taux_reussiteV2(gris, vt_bin)
        print ("Taux de réussite de l'image " + str(i) + ":" + str(taux))
        if (taux>70):
            nbBon +=1
        
    print("Taux de réussite : ", nbBon/nbTotal)
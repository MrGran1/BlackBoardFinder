import numpy as np
import matplotlib.image as pltimg
import cv2

from Fonctions_de_base import *
from Reperage_Tableau import *
from Reperage_Image import *
from Seuil_Couleur import *



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

def binarisationVT_tableauMax(img):
    """ Binarise la VT du reperage tableau, texte et hors tableau
    param : 
    img : VT sous forme d'image
    """
    new_img = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j,0] > 0.1:    #Rouge -> Blanc
                new_img[i,j] = 255

            elif img[i,j,1] > 0.1:  #Vert -> Gris
                new_img[i,j] = 128

            else :                  #Sans couleur -> Noir
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

def taux_reussiteV3(img, vt):
    """
    Compare l'image gris noir blanche, de reperage_image avec la VT et renvoie le taux de réussite
    """
    pixel_correct = 0
    total_pixel = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] ==  255 and vt[i,j] == 255 :
                pixel_correct +=1

            elif img[i,j] ==  128 and vt[i,j] == 128 :
                pixel_correct +=1

            if img[i,j] == 255 or vt[i,j] == 255:
                total_pixel += 1

            elif img[i,j] == 125 or vt[i,j] == 128:
                total_pixel += 1

            if img[i,j] == 255 and vt[i,j] == 128:
                pixel_correct += 0.5


    taux_reussite = (pixel_correct / total_pixel) * 100

    return taux_reussite

def comparaison_images ():
    nbBon = 0
    nbTotal = 0
    tabTest = [3,9,13,18,26,28,49,51,52,61,68,69,70,79,80]
    file = open("resultatFinal.txt",'a')
    for i in tabTest:
        # Repérage + comparaison VT
        print(i)
        nbTotal += 1

        img = pltimg.imread("./Images_Train_et_test/Test_(16)/"+str(i)+".jpg")

        #dilatation du texte blanc
        elemV1 = seuilTexteBlanc(img)
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        dil = cv2.dilate(elemV1, rect_kernel, iterations = 5)

        image = reperageImage(i, dil, img)
        vt_img = pltimg.imread("./Json/"+ str(i)+"VT" + "/label.png")
        print("Binarisation VT image")
        vt_bin = binarisationVT_tableauMax(vt_img)
        print("Taux de reussite")
        taux = taux_reussiteV3(image, vt_bin)
        print ("Taux de réussite de l'image " + str(i) + " : " + str(taux))
        file.write("Taux de réussite de l'image " + str(i) + " : " + str(taux) + "\n")

        if (taux>60):
            nbBon +=1
    file.write("Taux de réussite finale : " + str(nbBon/nbTotal))
    file.close()
    print("Taux de réussite : ", nbBon/nbTotal) 

comparaison_images()
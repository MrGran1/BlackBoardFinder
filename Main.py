import numpy as np
import cv2
import matplotlib.image as pltimg
import matplotlib.pyplot as plt


def comparerPixel(img,pixel1,pixel2):
    """
    Compare deux pixels pour indiquer si ils sont presque de la même couleur
    param:
    img : numpy array qui represente une image
    pixel1/pixel2 : tuple (x,y) representant les coordoonée d'un pixel
    return boolean
    """
    
    x1,y1 = pixel1
    x2,y2=pixel2
    intensite = 0
    for i in range(3):
        intensite += abs(img[y1-1][x1-1][i]-img[y2-1][x2-1][i])

    if (intensite<25):
        return True

    else:
        return False 



def convGris(img):
    """Convertit une image en niveau de gris
    param : 
    img : numpy array qui represente une image
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)
    for x in range(img.shape[0]):

        for y in range(img.shape[1]):
            r = img[x,y][0]
            g = img[x,y][1]
            b = img[x,y][2]

            l = (int(r)+int(g)+int(b))/3

            n[x,y]= l
    return n



def seuil(img,seuil1,seuil2):
    """Effectue un seuillage sur une image 
    param : 
    img : numpy array qui represente une image
    seuil 1/2 : seuil entre lequel les pixels seront blanc 
    
    """

    if (seuil1 > seuil2):
        seuil1,seuil2 = seuil2,seuil1

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x,y] <= seuil2 and img[x,y] >= seuil1 :
                img[x,y]= 255
            
            else :
                img[x,y] = 0



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


    
def griserPixel(img,pixel):
    """
    Grise un pixel
    param:
    img : numpy array qui represente une image
    pixel : tuple (x,y) representant les coordoonée d'un pixel
    return void
    """
    x,y = pixel
    for i in range(3):
        img[x][y][i] = 0.5*img[x][y][i] 



def delimitationImage (img):

    """ Creer un numpy array qui correspond à une image qui explicite les différentes partie d'une image
    param : 
    img : numpy array qui represente une image
    """
    x,y = len(img[0]),len(img)

    print (x,y)
    imgFinale = np.zeros((y,x))


    for j in range (y):
        for i in range (x):
            if(j != y-1):
                if comparerPixel(img,(i,j),(i,j+1)):
                    imgFinale [j+1,i] = 255

            if (i != x-1):
                if comparerPixel(img,(i,j),(i+1,j)):
                    imgFinale [j,i+1] = 255


    return imgFinale



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


def binarisationVT(img):
    new_img = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j,0] > 0.1 or img[i,j,1] > 0.1:
                new_img[i,j] = 255
            else :
                new_img[i,j] = 0
    return new_img



def taux_reussite(img, vt):
    total_pixel = img.shape[0]*img.shape[1]
    pixel_correct = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j] == vt[i,j] :
                pixel_correct +=1

    taux_reussite = (pixel_correct / total_pixel) * 100

    return taux_reussite




def connexite4(img,imgFinale,coordonnee,listeCoordonnee) : 
    """listePixel : une liste contenat les pixels déjà visité
        coordonnée : (i,j) du pixel
    img ; numpy array de l'image
    imgFinale : numpy array d'une image noire

    """
    
    while True:
        i,j = coordonnee

        if j<img.shape[0] and (i,j+1) not in listeCoordonnee and not img[i][j+1] == 0:
            coordonnee = (i,j+1)
            listeCoordonnee.append(coordonnee)
            imgFinale[i][j+1] = 255
        
        elif j>0 and (i,j-1) not in listeCoordonnee and not img[i][j-1] == 0: 
            coordonnee = (i,j-1)
            listeCoordonnee.append(coordonnee)
            imgFinale[i][j-1] = 255

        elif i<img.shape[1] and (i+1,j) not in listeCoordonnee and not img[i+1][j] == 0: 
            coordonnee = (i+1,j)
            listeCoordonnee.append(coordonnee)
            imgFinale[i+1][j] = 255

        
        elif i>0 and (i-1,j) not in listeCoordonnee and not img[i-1][j] == 0: 
            coordonnee = (i-1,j)
            listeCoordonnee.append(coordonnee)
            imgFinale[i-1][j] = 255

        else :
            break

# OpenCV (Open Computer Vision) est une bibliothèque graphique. 
# Elle est spécialisée dans le traitement d’images, que ce soit pour de la photo ou de la vidéo
def contours(img):

    # convertie l'image couleur en une image en nuance de gris
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
    
    # Pour réaliser une segmentation binaire avec OpenCV nous utilisons la fonction threshold()
    # qui prend l'image originale, le seuil, la valeur maximale des pixels et l'attribut THRESH_BINARY en paramètres
    # all pixels value above 120 will be set to 255
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)  

    # Dilate les éléments blancs de l'image en fonction des 3 nombres ci dessous
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)  

    # C'est avec "dilation" qu'il faudra comparer la verité terrain.
    # Le reste de cette fonction c'est juste pour bien encadrer l'image en fonction de "dilation" et avoir un meilleur affichage pour l'utilisateur

    # Trouve les contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Dessine les contours sur l'image de base à partir de l'image dilatée
    imgContour = cv2.drawContours(img, contours, -1, (0,255,255), 3)    


    # cv2.imshow("img",imgContour)              #cv2 a des problèmes (énoncé ci dessous) que plt permet de résoudre
    # cv2.waitKey(0)
    plt.imshow(imgContour, cmap = "gray")         #plt permet d'afficher l'image entiere et de la déplacer pour voir les contours 
    # plt.imshow(imgContour)
    plt.show()
    








def main():
    
    #SEGMENTATION ET BINARISATION DU TABLEAU-
    img = pltimg.imread("./Images_Train_et_test/Test_(16)/13.jpg")
    contours(img)
    # gris = convGris(img)
    # seuilCentre(gris)
    # #-

    # #BINARISATION DE LA VERITE TERRAIN-
    # #./Json/JsonIlan/49VT/label.png
    # #./Json/JsonTigran/23VT/label.png
    # vt_img = pltimg.imread("./Json/JsonIlan/54VT/label.png")
    # vt_bin = binarisationVT(vt_img)
    # #-

    # #AFFICHAGE TAUX DE REUSSITE-
    # print("TAUX DE RÉUSSITE :", taux_reussite(gris, vt_bin))
    # #-
    # imgFinale = np.zeros((gris.shape[0],gris.shape[1]),dtype = np.uint8)
    # #listecoordonnee = []
    # #connexite4(gris,imgFinale,(int(gris.shape[0]/2),int(gris.shape[1]/2)),listecoordonnee)

    # plt.imshow(imgFinale, cmap ='gray')
    # plt.show()

main()

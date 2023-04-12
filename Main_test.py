import cv2
import numpy as np
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

    # # Dilate les éléments blancs de l'image en fonction des 3 nombres ci dessous
    # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    # dilation = cv2.dilate(thresh, rect_kernel, iterations = 3)  

    # # C'est avec "dilation" qu'il faudra comparer la verité terrain.
    # # Le reste de cette fonction c'est juste pour bien encadrer l'image en fonction de "dilation" et avoir un meilleur affichage pour l'utilisateur

    # # Trouve les contours 
    # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # #Dessine les contours sur l'image de base à partir de l'image dilatée
    # imgContour = cv2.drawContours(img, contours, -1, (0,255,255), 2)    


    # cv2.imshow("img",imgContour)              #cv2 a des problèmes (énoncé ci dessous) que plt permet de résoudre
    # cv2.waitKey(0)
    plt.imshow(thresh, cmap = "gray")         #plt permet d'afficher l'image entiere et de la déplacer pour voir les contours 
    # plt.imshow(imgContour)
    plt.show()
    
def connexite4texteBin(bin):
    """ Prend une image binarisée avec un tableau en blanc et son texte en noir, 
    et renvoie une autre image avec seulement le texte en blanc

    param : 
    gris : image binarisée
    """
    image_padded = np.zeros((bin.shape[0] + 8, bin.shape[1] + 8), dtype = np.uint8)
    image_padded[4 : -4, 4: -4] = bin # [:,:,0] on peut faire cette manip, qd ya 3 canaux au lieu de 1, quand on met une image en niveau de gris seulement mettre 2 canaux. Faut que j'essaye de le faire d'ailleurs

    resfinal = np.zeros((bin.shape[0] + 8, bin.shape[1] + 8), dtype = np.uint8)

    for i in range (bin.shape[0]):
        for j in range(bin.shape[1]):
            if (bin[i,j] == 0) :
                for k in range(j-4,j+4):
                    if ((image_padded[i,k]) == 255) :
                        resfinal[i,j] = 255
                for l in range(i-4,i+4):
                    if ((image_padded[l,j]) == 255) :
                        resfinal[i,j] = 255   

    return resfinal

def texteBlanc(img):
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            # if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
            # if ( (85 <= img[i,j,0] <= 184) and (118 <= img[i,j,1] <= 208) and (107 <= img[i,j,2] <= 242) ): # 2.jpg
            if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
                n[i,j] = 255
    
    return n

def texteNoir(img):
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            # if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
            # if ( (85 <= img[i,j,0] <= 184) and (118 <= img[i,j,1] <= 208) and (107 <= img[i,j,2] <= 242) ): # 2.jpg
            if ( (15 <= img[i,j,0] <= 100) and (10 <= img[i,j,1] <= 100) and (6 <= img[i,j,2] <= 100) ): # 1.jpg
                n[i,j] = 255
    
    return n

def texteBleu(img):
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            # if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
            # if ( (85 <= img[i,j,0] <= 184) and (118 <= img[i,j,1] <= 208) and (107 <= img[i,j,2] <= 242) ): # 2.jpg
            if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
                n[i,j] = 255
    
    return n

def texteVert(img):
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (80 <= img[i,j,0] <= 210) and (90 <= img[i,j,1] <= 230) and (100 <= img[i,j,2] <= 215) ): # 1.jpg
                n[i,j] = 255
    
    return n

def texteRouge(img):
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (107 <= img[i,j,0] <= 220) and (100 <= img[i,j,1] <= 208) and (100 <= img[i,j,2] <= 190) ): # 1.jpg
                n[i,j] = 255
    
    return n

def seuil(img,couleur):
    """Effectue un seuillage sur une image 
    param : 
    img : numpy array qui represente une image
    seuil 1/2 : seuil entre lequel les pixels seront blanc 
    
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)
    marge = 60 # 30 pour 1.jpg, 60 pour 2,
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if ( (couleur[0]-marge <= img[i,j][0] <= couleur[0]+marge) and (couleur[1]-marge <= img[i,j][1] <= couleur[1]+marge) and (couleur[2]-marge <= img[i,j][2] <= couleur[2]+marge) ):
                n[i,j] = 255
            else :
                n[i,j] = 0
            
    return n

def seuilCentre(img):
    """ Effectue un seuillage sur une image en fonction de la moyenne des pixels du centre de l'image
    param :
    img : numpy array qui represente une image
    """
    #On récupère la couleur du centre de l'image
    couleur = getCouleurCentre(img)
    return seuil(img,couleur)

def getCouleurCentre(img):
    """ Récupère la couleur la plus dominante au centre de l'image pour récuperer la couleur du tableau"""
    xcentre = int (img.shape[1]/2)  # avant : (img.shape[0]/2)
    ycentre = int(img.shape[0]/2)   # avant : (img.shape[1]/2)
    couleur0 = 0
    couleur1 = 0
    couleur2 = 0
    nbPixel = 250000
    #On parcourt les pixels du centre de l'image
    for i in range (ycentre-250, ycentre + 250):       # avant : for j
        for j in range (xcentre-250, xcentre + 250):   # avant : for i
            couleur0 += img[i,j][0]
            couleur1 += img[i,j][1]
            couleur2 += img[i,j][2]
 
    couleur0 //= nbPixel
    couleur1 //= nbPixel
    couleur2 //= nbPixel
    
    return [couleur0,couleur1,couleur2]


def connexite4texteNonBin(img):
    """ Prend une image avec un tableau, 
    et renvoie une autre image avec seulement le texte en blanc

    param : 
    img : image dont on vous rendre le texte blanc et le reste noir
    """
    image_padded = np.zeros((img.shape[0] + 8, img.shape[1] + 8, 3), dtype = np.uint8)
    image_padded[4 : -4, 4: -4,0]= img[:,:,0] # [:,:,0] on peut faire cette manip, qd ya 3 canaux au lieu de 1, quand on met une image en niveau de gris seulement mettre 2 canaux. Faut que j'essaye de le faire d'ailleurs
    image_padded[4 : -4, 4: -4,1] = img[:,:,1]
    image_padded[4 : -4, 4: -4,2] = img[:,:,2]

    resfinal = np.zeros((img.shape[0] + 8, img.shape[1] + 8), dtype = np.uint8)
    marge = 60
    couleur = getCouleurCentre(img)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            # if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ) : texte blanc
            # if ( (15 <= img[i,j,0] <= 100) and (10 <= img[i,j,1] <= 100) and (6 <= img[i,j,2] <= 100) ) : # texte noir
            if ( (15 <= img[i,j,0] <= 100) and (10 <= img[i,j,1] <= 100) and (6 <= img[i,j,2] <= 100) ) : # texte noir
                for k in range(j-4,j+4):
                    if ( (couleur[0]-marge <= image_padded[i,k][0] <= couleur[0]+marge) and (couleur[1]-marge <= image_padded[i,k][1] <= couleur[1]+marge) and (couleur[2]-marge <= image_padded[i,k][2] <= couleur[2]+marge) ):
                        resfinal[i,j] = 255
                for l in range(i-4,i+4):
                    if ( (couleur[0]-marge <= image_padded[l,j][0] <= couleur[0]+marge) and (couleur[1]-marge <= image_padded[l,j][1] <= couleur[1]+marge) and (couleur[2]-marge <= image_padded[l,j][2] <= couleur[2]+marge) ) :
                        resfinal[i,j] = 255   

    return resfinal

def main():
    
    #SEGMENTATION ET BINARISATION DU TABLEAU-
    #./Images_Train_et_test/Entrainement_(57)/23.jpg
    img = pltimg.imread("D:/Dossier_chelou/Users/kelli/Documents/GitHub/Projet-Image-Suicide-Squad-/Images_Train_et_test/Entrainement_(57)/23.jpg")
    # new_img = texteNoir(img)
    new_img = connexite4texteNonBin(img)
    # contours(img)
    # gris = convGris(img)

    # new_img = seuilCentre(img) # fail 0.jpg,

    # plt.figure()                         
    # plt.imshow(gris, cmap ='gray')

    # res = connexite4texte(gris)
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

    plt.figure()
    plt.imshow(img, cmap ='gray')
    plt.show()

main()






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
            if img[x,y,0] <= seuil2 and img[x,y,0] >= seuil1 :
                img[x,y]= [255,255,255]
            
            else :
                img[x,y] = [0,0,0]

def seuilCentre(img):
    """ Effectue un seuillage sur une image en fonction de la moyenne des pixels du centre de l'image
    param :
    img : numpy array qui represente une image
    """

    seuil1=getCouleurCentre(img)+20
    seuil2=getCouleurCentre(img)-20

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
    xcentre = int (img.shape[0]/2)
    ycentre = int(img.shape[1]/2)
    condition = False
    max = -1
    couleurMax = ""
    nbCouleur = {}
    for j in range (ycentre-250, ycentre + 250):
        for i in range (xcentre-250, xcentre + 250):
            condition = False

            



            for couleur in nbCouleur.keys():
                if couleur >= img[j,i]-20 and couleur <= img[j,i] + 20 :
                    nbCouleur[couleur] += 1
                    condition = True
                    break

            if condition == False  :
                nbCouleur[img[j,i]] = 1


    for couleur in nbCouleur.keys():
        
        if nbCouleur[couleur] > max:
            couleurMax = couleur
            max = nbCouleur[couleur]
    
    
    return couleurMax 
                    

img = pltimg.imread("./train/53.jpg")

#finale = delimitationImage(img)
gris = convGris(img)
print (getCouleurCentre(gris))
#seuil(img,160, 190)
#plt.imshow(img,cmap ='gray')
#plt.show()
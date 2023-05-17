import numpy as np


# def connexite4texteNonBin(img):
#     """ Prend une image avec un tableau, 
#     et renvoie une autre image avec seulement le texte en blanc

#     param : 
#     img : image dont on vous rendre le texte blanc et le reste noir
#     """
#     image_padded = np.zeros((img.shape[0] + 8, img.shape[1] + 8, 3), dtype = np.uint8)
#     image_padded[4 : -4, 4: -4,0]= img[:,:,0] # [:,:,0] on peut faire cette manip, qd ya 3 canaux au lieu de 1, quand on met une image en niveau de gris seulement mettre 2 canaux. Faut que j'essaye de le faire d'ailleurs
#     image_padded[4 : -4, 4: -4,1] = img[:,:,1]
#     image_padded[4 : -4, 4: -4,2] = img[:,:,2]

#     resfinal = np.zeros((img.shape[0] + 8, img.shape[1] + 8), dtype = np.uint8)
#     marge = 60
#     couleur = getCouleurCentreKellian(img)

#     for i in range (img.shape[0]):
#         for j in range(img.shape[1]):
#             # if ( (50 <= img[i,j,0] <= 120) and (50 <= img[i,j,1] <= 130) and (110 <= img[i,j,2] <= 140) ) : #TEXTE BLEU
#             # if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ) : #TEXTE BLANC
#             # if ( (15 <= img[i,j,0] <= 100) and (10 <= img[i,j,1] <= 100) and (6 <= img[i,j,2] <= 100) ) : #TEXTE NOIR
#             if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ) : #TEXTE BLANC
#                 for k in range(j-4,j+4):
#                     if ( (couleur[0]-marge <= image_padded[i,k][0] <= couleur[0]+marge) and (couleur[1]-marge <= image_padded[i,k][1] <= couleur[1]+marge) and (couleur[2]-marge <= image_padded[i,k][2] <= couleur[2]+marge) ):
#                         resfinal[i,j] = 255
#                         break
#                 for l in range(i-4,i+4):
#                     if ( (couleur[0]-marge <= image_padded[l,j][0] <= couleur[0]+marge) and (couleur[1]-marge <= image_padded[l,j][1] <= couleur[1]+marge) and (couleur[2]-marge <= image_padded[l,j][2] <= couleur[2]+marge) ) :
#                         resfinal[i,j] = 255
#                         break

#     return resfinal






def connexite4texteBin(bin):
    """ Prend une image binarisée avec un tableau en blanc et son texte en noir, 
    et renvoie une autre image avec seulement le texte en blanc

    param : 
    bin : image binarisée
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



def connexite4texteBin_GPT(bin):
    h, w = bin.shape
    image_padded = np.pad(bin, ((4, 4), (4, 4)), mode='constant')
    resfinal = np.zeros((h + 8, w + 8), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            if bin[i, j] == 0:
                if np.any(image_padded[i, j-4:j+4] == 255):
                    resfinal[i, j] = 255
                elif np.any(image_padded[i-4:i+4, j] == 255):
                    resfinal[i, j] = 255

    return resfinal




def RepElemsBlancsAmelio(Tab, Elements):
    """ Repere les elements final en fonction du tableau detecté

    param : 
    Tab : Detection du tableau avec la 4 connexité de Tigran (Cette image à 4 pixels en plus de chaque côté)
    Elements : La detection des elements seulement avec le seuillage

    """
   
    image_padded = np.zeros((Tab.shape[0] + 8, Tab.shape[1] + 8), dtype = np.uint8)
    image_padded[4 : -4, 4: -4] = Tab

    resfinal = np.zeros((Tab.shape[0], Tab.shape[1]), dtype = np.uint8)

    for i in range (Elements.shape[0]):
        for j in range(Elements.shape[1]):

            if (Elements[i,j] == 255):
                ind1 = False
                ind2 = False

                for k in range(j-4,j+4):
                    if ((image_padded[i,k]) == 255) :
                        ind1=True
                        break
                for l in range(i-4,i+4):
                    if ((image_padded[l,j]) == 255) :
                        ind2=True
                        break

                if (ind1 and ind2):
                    resfinal[i,j] = 255
    return resfinal
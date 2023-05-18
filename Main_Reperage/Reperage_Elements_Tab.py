import numpy as np




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
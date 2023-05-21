import matplotlib.image as pltimg
import cv2

from Reperage_Tableau import *
from Reperage_Image import *
from Seuil_Couleur import *
from Reperage_Elements_Tab import *




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
    """ Binarise la VT du reperage tableau, éléments du tableau et hors tableau
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




def binarisationVT_elements(img):
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




def fct_Eval_Tableau(img):

    print("Conversion en gris (en cours...)")
    gris = convGris(img)

    print("Binarisation (en cours...)")
    seuilCentre(gris)

    print("Conexite 4 (en cours...)")
    gris = connexite4(gris)

    print("Boucheur de trou (en cours...)")
    fin = boucheurDeTrou(gris)

    return fin




def fct_Eval_Elements_1(img):
    #1 Repérage tableau de l'image
    print("Conversion en gris (en cours...)")
    tab = convGris(img)
    print("Binarisation (en cours...)")
    couleur = seuilCentre_Plus_DonneCouleur(tab)
    print("Conexite 4 (en cours...)")
    tab = connexite4(tab)

    #2 Repérage éléments du tableau avec le seuillage
    if (couleur < 125): #Tableau bleu/vert
        
        elemV1 = seuil_ElementsBlancs(img)
    
    else : #Tableau Blanc
        elemV1 = seuil_ElementsTableauBlanc(img)

    #3 On combine 1 et 2 pour enlever les pixels blancs qui ne sont pas dans le tableau
    print("Suppresion_ElementsHorsTableau (en cours...)")
    elemV2 = Suppresion_ElementsHorsTableau(tab, elemV1)

    #4 On dilate le résultat final pour convenir avec la VT
    print("Dilatation de l'image final (en cours...)")
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))  # nombre à gauche augmente horizontalement et à droite verticalement les formes blanches
    dilation = cv2.dilate(elemV2, rect_kernel, iterations = 5)         # iterations augmente de façon homogène les formes blanches

    return dilation




def fct_Eval_Elements_2(img):
    # Repérage tableau de l'image
    print("Conversion en gris (en cours...)")
    tab = convGris(img)
    print("Binarisation (en cours...)")
    seuilCentre(tab)
    print("Conexite 4 (en cours...)")
    tab = connexite4(tab)

    # On fait une sorte d'inversion
    print("Transformation_ElemNoirsDuTab_EnBlancs (en cours...)")
    elemV1 = Transformation_ElemNoirsDuTab_EnBlancs(tab)

    # On combine 1 et 2 pour enlever les pixels blancs qui ne sont pas dans le tableau
    print("Suppresion_ElementsHorsTableau (en cours...)")
    elemV2 = Suppresion_ElementsHorsTableau(tab, elemV1)

    # On dilate le résultat final pour convenir avec la VT
    print("Dilatation de l'image final (en cours...)")
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))  # nombre à gauche augmente horizontalement et à droite verticalement les formes blanches
    dilation = cv2.dilate(elemV2, rect_kernel, iterations = 5)         # iterations augmente de façon homogène les formes blanches

    return dilation




def fct_Eval_TableauPlusElements(img,i):

    tab = convGris(img)
    couleur = DonneCouleurCentre(tab)

    if (couleur < 125): #Tableau bleu/vert
        elemV1 = seuil_ElementsBlancs(img)
    else :               #Tableau Blanc
        elemV1 = seuil_ElementsTableauBlanc(img)

    image = reperageImage(i, elemV1, img)

    return image




def Eval(nom_fichier,ref_taux,nb_Eval):

    if (nb_Eval == 1):
        print("\n----- FONCTION D'EVALUATION REPERAGE DE TABLEAU -----\n")
    elif(nb_Eval == 2):
        print("\n----- FONCTION D'EVALUATION REPERAGE D'ELEMENTS (1) -----\n")
    elif(nb_Eval == 3):
        print("\n----- FONCTION D'EVALUATION REPERAGE D'ELEMENTS (2) -----\n")
    elif (nb_Eval == 4):
        print("\n----- FONCTION D'EVALUATION REPERAGE DE TABLEAU + ELEMENTS -----\n")
    else :
        print("\n!!!!!!!!!!!!! ERREUR DANS LA SAISIE DU NUMERO D'EVALUATION DANS LE MAIN (CHIFFRE DOIT ETRE 1-4) RELANCEZ LE PROGRAMME !!!!!!!!!!!!!!!!!\n")

    file = open(nom_fichier,'a')
    nbBon = 0
    nbTotal = 0
    fct = 0
    tabTest = [3,9,13,18,26,28,35,49,51,52,61,68,69,70,79,80]

    for i in tabTest:
        print ("image : " + str(i))
    
        nbTotal += 1

        img = pltimg.imread("./Images_Train_et_test/Test_(16)/"+str(i)+".jpg")
        vt_img = pltimg.imread("./Json/"+ str(i)+"VT" + "/label.png")

        if (nb_Eval == 1):
            fct = fct_Eval_Tableau(img)
        elif(nb_Eval == 2):
            fct = fct_Eval_Elements_1(img)
        elif(nb_Eval == 3):
            fct = fct_Eval_Elements_2(img)
        else :
            fct = fct_Eval_TableauPlusElements(img,i)
   

        # BINARISATION VT
        print("Binarisation VT image (en cours...)")
        vt_bin = binarisationVT_elements(vt_img)

        # TAUX DE REUSSITE
        print("Taux de reussite (en cours...)")
        if (nb_Eval == 4):                     # Si on fait l'Eval Tableau+Elements
            taux = taux_reussiteV3(fct, vt_bin)
        else :                                  # Si on fait les 3 autres Evals
            taux = taux_reussiteV2(fct, vt_bin)
        
        print("Taux de réussite de l'image " + str(i) + " : " + str(taux))
        file.write("Taux de réussite de l'image " + str(i) + " : " + str(taux) + "\n")

        if (taux>ref_taux):
            nbBon +=1
        
    print("Taux de réussite finale : ", str(nbBon/nbTotal*100))
    file.write("Taux de réussite finale : " + str(nbBon/nbTotal*100))
    file.close()  



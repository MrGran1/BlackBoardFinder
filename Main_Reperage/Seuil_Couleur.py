import numpy as np



def seuilTexteBlanc(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme blanc par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte blanc
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    # conditions à appliquer
    cond1 = (197 <= img[:,:,0]) & (img[:,:,0] <= 224) & (221 <= img[:,:,1]) & (img[:,:,1] <= 248) & (205 <= img[:,:,2]) & (img[:,:,2] <= 216)
    cond2 = (179 <= img[:,:,0]) & (img[:,:,0] <= 215) & (215 <= img[:,:,1]) & (img[:,:,1] <= 237) & (178 <= img[:,:,2]) & (img[:,:,2] <= 201)
    cond3 = (155 <= img[:,:,0]) & (img[:,:,0] <= 180) & (189 <= img[:,:,1]) & (img[:,:,1] <= 219) & (150 <= img[:,:,2]) & (img[:,:,2] <= 185)
    cond4 = (170 <= img[:,:,0]) & (img[:,:,0] <= 197) & (200 <= img[:,:,1]) & (img[:,:,1] <= 215) & (224 <= img[:,:,2]) & (img[:,:,2] <= 244) # image 1
    cond5 = (146 <= img[:,:,0]) & (img[:,:,0] <= 161) & (168 <= img[:,:,1]) & (img[:,:,1] <= 187) & (191 <= img[:,:,2]) & (img[:,:,2] <= 210) # image 1
    cond6 = (146 <= img[:,:,0]) & (img[:,:,0] <= 161) & (168 <= img[:,:,1]) & (img[:,:,1] <= 187) & (164 <= img[:,:,2]) & (img[:,:,2] <= 176) # image 2
    cond7 = (100 <= img[:,:,0]) & (img[:,:,0] <= 138) & (140 <= img[:,:,1]) & (img[:,:,1] <= 170) & (127 <= img[:,:,2]) & (img[:,:,2] <= 159) # image 2

    temps1 = np.logical_or(cond1, cond2)
    temps2 = np.logical_or(cond3,cond4)
    temps3 = np.logical_or(cond5, cond6)
    temps4 = np.logical_or(temps3, cond7)


    # combiner les conditions
    cond = np.logical_or( np.logical_or(temps1, temps2), np.logical_or(temps3, temps4) )

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0], dtype=np.uint8)
    n[cond] = 255

    # for i in range (img.shape[0]):
    #     for j in range(img.shape[1]):
    #         # if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
    #         # if ( (85 <= img[i,j,0] <= 184) and (118 <= img[i,j,1] <= 208) and (107 <= img[i,j,2] <= 242) ): # 2.jpg
    #         if ( (107 <= img[i,j,0] <= 184) and (130 <= img[i,j,1] <= 208) and (161 <= img[i,j,2] <= 242) ): # 1.jpg
    #             n[i,j] = 255
    
    return n




def seuilTexteNoir(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme noir par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte noir
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (15 <= img[i,j,0] <= 100) and (10 <= img[i,j,1] <= 100) and (6 <= img[i,j,2] <= 100) ): # 1.jpg
                n[i,j] = 255
    
    return n




def seuilTexteBleu(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme bleu(clair,normal,fonce) par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte bleu(clair,normal,fonce)
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    # conditions à appliquer
    cond1 = (90 <= img[:,:,0]) & (img[:,:,0] <= 145) & (105 <= img[:,:,1]) & (img[:,:,1] <= 150) & (137 <= img[:,:,2]) & (img[:,:,2] <= 163)
    cond2 = (6 <= img[:,:,0]) & (img[:,:,0] <= 90) & (47 <= img[:,:,1]) & (img[:,:,1] <= 100) & (130 <= img[:,:,2]) & (img[:,:,2] <= 150)
    cond3 = (3 <= img[:,:,0]) & (img[:,:,0] <= 34) & (10 <= img[:,:,1]) & (img[:,:,1] <= 66) & (100 <= img[:,:,2]) & (img[:,:,2] <= 145)

    # combiner les conditions
    cond = np.logical_or(np.logical_or(cond1, cond2), cond3)

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0], dtype=np.uint8)
    n[cond] = 255
    
    return n




def seuilTexteBleuClair(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme bleu clair par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte bleu clair
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (90 <= img[i,j,0] <= 145) and (105 <= img[i,j,1] <= 150) and (137 <= img[i,j,2] <= 163) ): 
                n[i,j] = 255
    
    return n




def seuilTexteBleuNormal(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme bleu normal par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte bleu normal
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (6 <= img[i,j,0] <= 90) and (47 <= img[i,j,1] <= 100) and (130 <= img[i,j,2] <= 150) ): 
                n[i,j] = 255
    
    return n




def seuilTexteBleuFonce(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme bleu fonce par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte bleu fonce
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (3 <= img[i,j,0] <= 34) and (10 <= img[i,j,1] <= 66) and (100 <= img[i,j,2] <= 145) ): 
                n[i,j] = 255
    
    return n




def seuilTexteVert(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme vert par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte vert"""
  
    # conditions à appliquer
    cond1 = (48 <= img[:,:,0]) & ( img[:,:,0] <= 65) & (76 <= img[:,:,1]) & (img[:,:,1] <= 93) & (68 <= img[:,:,2]) & (img[:,:,2] <= 79) 
    cond2 = (69 <= img[:,:,0]) & (img[:,:,0] <= 95) & (101 <= img[:,:,1]) & (img[:,:,1] <= 110) & (86 <= img[:,:,2]) & (img[:,:,2] <= 103)
    cond3 = (97 <= img[:,:,0]) & (img[:,:,0] <= 110) & (120 <= img[:,:,1]) & (img[:,:,1] <= 130) & (108 <= img[:,:,2]) & (img[:,:,2] <= 120)
    cond4 = (85 <= img[:,:,0]) & (img[:,:,0] <= 105) & (99 <= img[:,:,1]) & (img[:,:,1] <= 126) & (90 <= img[:,:,2]) & (img[:,:,2] <= 119)
    cond5 = (102 <= img[:,:,0]) & (img[:,:,0] <= 130) & (119 <= img[:,:,1]) & (img[:,:,1] <= 135) & (114 <= img[:,:,2]) & (img[:,:,2] <= 130)

    # combiner les conditions
    cond = np.logical_or(np.logical_or(np.logical_or(cond1, cond2), np.logical_or(cond3,cond4)), cond5)

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0], dtype=np.uint8)
    n[cond] = 255

    return n




def seuilTexteVertNormal(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme vert par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte vert
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (48 <= img[i,j,0] <= 65) and (76 <= img[i,j,1] <= 93) and (68 <= img[i,j,2] <= 79) ): 
                n[i,j] = 255
    
    return n




def seuilTexteVertClair(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme vert par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte vert
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    for i in range (img.shape[0]):
        for j in range(img.shape[1]):
            if ( (69 <= img[i,j,0] <= 95) and (101 <= img[i,j,1] <= 110) and (86 <= img[i,j,2] <= 103) ): 
                n[i,j] = 255
    
    return n




def seuilTexteVertClair2(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme vert par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte vert
    """
    cond1 = (97 <= img[:,:,0]) & (img[:,:,0] <= 110)
    cond2 = (120 <= img[:,:,1]) & (img[:,:,1] <= 130)
    cond3 = (108 <= img[:,:,2]) & (img[:,:,2] <= 120)

    # combiner les conditions
    cond = np.logical_and(np.logical_and(cond1, cond2), cond3)

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0])
    n[cond] = 255
    return n




def seuilTexteRouge(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme rouge par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte rouge
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    # conditions à appliquer
    cond1 = (145 <= img[:,:,0]) & (img[:,:,0] <= 162) & (77 <= img[:,:,1]) & (img[:,:,1] <= 94) & (78 <= img[:,:,2]) & (img[:,:,2] <= 94)
    cond2 = (89 <= img[:,:,0]) & (img[:,:,0] <= 113) & (33 <= img[:,:,1]) & (img[:,:,1] <= 50) & (46 <= img[:,:,2]) & (img[:,:,2] <= 55)
    cond3 = (59 <= img[:,:,0]) & (img[:,:,0] <= 73) & (39 <= img[:,:,1]) & (img[:,:,1] <= 53) & (37 <= img[:,:,2]) & (img[:,:,2] <= 46)

    # combiner les conditions
    cond = np.logical_or(np.logical_or(cond1, cond2), cond3)

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0], dtype=np.uint8)
    n[cond] = 255
    
    return n




def seuilTexte(img):
    n1 = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)
    n2 = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    n1 = seuilTexteBleu(img)
    n2 = seuilTexteVert(img)

    # créer un tableau booléen avec True si n1 ou n2 est égal à 255
    cond = np.logical_or(n1 == 255, n2 == 255)

    # mettre à jour n1 avec la condition
    n1[cond] = 255

    return n1
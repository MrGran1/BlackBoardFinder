import numpy as np




def seuil_ElementsBlancs(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme blanc par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte blanc
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    # conditions à appliquer
    cond1 = (197 <= img[:,:,0]) & (img[:,:,0] <= 224) & (221 <= img[:,:,1]) & (img[:,:,1] <= 248) & (205 <= img[:,:,2]) & (img[:,:,2] <= 216)
    cond2 = (179 <= img[:,:,0]) & (img[:,:,0] <= 215) & (215 <= img[:,:,1]) & (img[:,:,1] <= 237) & (178 <= img[:,:,2]) & (img[:,:,2] <= 201)
    cond3 = (155 <= img[:,:,0]) & (img[:,:,0] <= 180) & (189 <= img[:,:,1]) & (img[:,:,1] <= 219) & (150 <= img[:,:,2]) & (img[:,:,2] <= 185)
    cond4 = (170 <= img[:,:,0]) & (img[:,:,0] <= 197) & (200 <= img[:,:,1]) & (img[:,:,1] <= 215) & (224 <= img[:,:,2]) & (img[:,:,2] <= 244) 
    cond5 = (146 <= img[:,:,0]) & (img[:,:,0] <= 161) & (168 <= img[:,:,1]) & (img[:,:,1] <= 187) & (191 <= img[:,:,2]) & (img[:,:,2] <= 210) 
    cond6 = (146 <= img[:,:,0]) & (img[:,:,0] <= 161) & (168 <= img[:,:,1]) & (img[:,:,1] <= 187) & (164 <= img[:,:,2]) & (img[:,:,2] <= 176) 
    cond7 = (100 <= img[:,:,0]) & (img[:,:,0] <= 138) & (140 <= img[:,:,1]) & (img[:,:,1] <= 170) & (127 <= img[:,:,2]) & (img[:,:,2] <= 159)

    temps1 = np.logical_or(cond1, cond2)
    temps2 = np.logical_or(cond3,cond4)
    temps3 = np.logical_or(cond5, cond6)
    temps4 = np.logical_or(temps3, cond7)


    # combiner les conditions
    cond = np.logical_or( np.logical_or(temps1, temps2), np.logical_or(temps3, temps4) )

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0], dtype=np.uint8)
    n[cond] = 255
    
    return n




def seuil_ElementsTableauBlanc(img):
    """ Renvoie l'image donnée en paramètre en remplaçant les pixels considérés comme noir par 255 et le reste à 0

    param : 
    img : image sur laquelle on veut seulement afficher le texte noir
    """
    n = np.zeros((img.shape[0],img.shape[1]),dtype = np.uint8)

    # conditions à appliquer
    cond1 = (0 <= img[:,:,0]) & (img[:,:,0] <= 20) & (0 <= img[:,:,1]) & (img[:,:,1] <= 20) & (0 <= img[:,:,2]) & (img[:,:,2] <= 20) #noir
    cond2 = (110 <= img[:,:,0]) & (img[:,:,0] <= 120) & (140 <= img[:,:,1]) & (img[:,:,1] <= 150) & (140 <= img[:,:,2]) & (img[:,:,2] <= 150)#vert clair
    cond3 = (60 <= img[:,:,0]) & (img[:,:,0] <= 70) & (90 <= img[:,:,1]) & (img[:,:,1] <= 100) & (80 <= img[:,:,2]) & (img[:,:,2] <= 90)#vert fonce
    cond4 = (40 <= img[:,:,0]) & (img[:,:,0] <= 50) & (60 <= img[:,:,1]) & (img[:,:,1] <= 70) & (90 <= img[:,:,2]) & (img[:,:,2] <= 100)#bleu
    cond5 = (60 <= img[:,:,0]) & (img[:,:,0] <= 70) & (0 <= img[:,:,1]) & (img[:,:,1] <= 10) & (20 <= img[:,:,2]) & (img[:,:,2] <= 30)#rougefonce

    temps1= np.logical_or(cond1, cond2)
    temps2= np.logical_or(cond4, cond3)

    # combiner les conditions
    cond = np.logical_or(np.logical_or(temps1,temps2),cond5)

    # appliquer les conditions à l'image
    n = np.zeros_like(img[:,:,0], dtype=np.uint8)
    n[cond] = 255
    
    return n
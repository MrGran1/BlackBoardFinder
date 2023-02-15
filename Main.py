import numpy as np

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
    intensité = 0
    for i in range(3):
        intensite += abs(img[x1][y1][i]-img[x2][y2][i])

    if (intensité<50):
        return True
        
    else:
        return False    
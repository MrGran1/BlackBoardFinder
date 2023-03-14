import matplotlib.pyplot as plt
import matplotlib.image as mplimg
import numpy as np

img = mplimg.imread(r"D:\Dossier_chelou\Users\kelli\Documents\L3\S2\Image\Images Projet\0.jpg").copy()

new_img = np.zeros((img.shape[0],img.shape[1]))

def tracerSegment(x1,y1,x2,y2):
  e = x2-x1
  dy = e*2
  dx = (y2-y1)*2
  while (x1 <= x2):
      new_img[x1, y1] = (255) 
      x1 = x1 + 1
      if (e ==  e - dy) <= 0 :
          y1 = y1 + 1 
          e =  e + dx 

tracerSegment(1,6,4,400)
tracerSegment(470,1350,4,400)

plt.figure()
plt.imshow(new_img, cmap=plt.cm.gray)
plt.show()
plt.imshow(img)
plt.show()
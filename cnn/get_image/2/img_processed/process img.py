# /Users/garys/Desktop/cnn project /2018 01 12/process img/image
#/Users/garys/Desktop/cnn project /2018 01 12/process img/image/1.jpg
from PIL import Image
import cv2

from skimage import transform,data
import matplotlib.pyplot as plt

import numpy as np
from sklearn.preprocessing import binarize

count = 1

plt.rcParams.update({'figure.max_open_warning': 0}) #fix the memory error

while (count <= 11000):
    #try:
    img = cv2.imread('/Users/garys/Desktop/get c img/2/img/'+str(count)+'.jpg')
    dst = cv2.fastNlMeansDenoisingColored(img, None, 31, 31 ,7 ,21)
    height, width, channels = img.shape #get img height and width
    
    plt.figure(figsize=(width, height), dpi=100)
    plt.axis('off')
    plt.imshow(dst)
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)#去白邊

    
    plt.savefig('/Users/garys/Desktop/get c img/2/img pr/'+str(count)+'.jpg',dpi=10)
    img2 = cv2.imread('/Users/garys/Desktop/get c img/2/img pr/'+str(count)+'.jpg')
    
    
    ret,thresh = cv2.threshold(img2,127,255,cv2.THRESH_BINARY_INV)#黑白化
    plt.imshow(thresh)
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)#去白邊
    #get img height and width
    height, width, channels = thresh.shape
    
    
    imgarr = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    
    
    imgarr[:,100:width-40] = 0
    imagedata = np.where(imgarr == 255) #find where are white
    
    
    X = np.array([imagedata[1]])
    Y = height - imagedata[0]

    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression

    poly_reg= PolynomialFeatures(degree = 2)
    X_ = poly_reg.fit_transform(X.T)
    regr = LinearRegression()
    regr.fit(X_, Y)

    X2 = np.array([[i for i in range(0,width)]])
    X2_ = poly_reg.fit_transform(X2.T)


    
    for ele in np.column_stack([regr.predict(X2_).round(0),X2[0],] ):
        pos = height - int(ele[0])
        thresh[pos-25:pos+25, int(ele[1])] = 255 - thresh[pos-25:pos+25,int(ele[1])] #這裡可以更改回歸線條上下範圍

    plt.imshow(thresh)
    newdst=transform.resize(thresh, (48, 140)) #resize (h,w)
    plt.close() #close figure of origine size
    plt.figure(figsize=(140, 48), dpi=100) #存成固定大小 (w, h)
    plt.axis('off')
    plt.imshow(newdst)

    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)#去白邊
    plt.savefig('/Users/garys/Desktop/get c img/2/img pr/'+str(count)+'.jpg',dpi=1)
    count += 1

'''
except:
    print("err")
'''


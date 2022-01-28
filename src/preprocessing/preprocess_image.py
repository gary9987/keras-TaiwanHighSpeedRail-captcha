from PIL import Image
import cv2

from skimage import transform,data
import matplotlib.pyplot as plt

import numpy as np
from sklearn.preprocessing import binarize
from pathlib import Path

if __name__ == '__main__':
    dic = [[0] * 2 for i in range(100)]
    for i in range(100):
        dic[i][0]=25
        dic[i][1]=25
    dic[50][0]=26
    dic[50][1]=24
    dic[48][0]=23
    dic[48][1]=30
    dic[46][0]=27
    dic[46][1]=25
    dic[45][0]=21
    dic[45][1]=30

    count = 1
    plt.rcParams.update({'figure.max_open_warning': 0}) #fix the memory error
    Path("./processed_image/").mkdir(parents=True, exist_ok=True)

    while (count <= 8000):

        img = cv2.imread('../download_img/image/'+str(count)+'.jpg')
        dst = cv2.fastNlMeansDenoisingColored(img, None, 31, 31 ,7 ,21)
        height1, width1, channels1 = img.shape #get img height and width

        plt.figure(figsize=(width1, height1), dpi=100)
        plt.axis('off')
        plt.imshow(dst)
        plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)#去白邊


        plt.savefig('./processed_image/'+str(count)+'.jpg',dpi=10)
        img2 = cv2.imread('./processed_image/'+str(count)+'.jpg')


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

        poly_reg = PolynomialFeatures(degree = 2)
        X_ = poly_reg.fit_transform(X.T)
        regr = LinearRegression()
        regr.fit(X_, Y)

        X2 = np.array([[i for i in range(0,width)]])
        X2_ = poly_reg.fit_transform(X2.T)

        for ele in np.column_stack([regr.predict(X2_).round(0),X2[0],] ):
            pos = height - int(ele[0])
            thresh[pos-int(dic[height1][0]):pos+int(dic[height1][1]), int(ele[1])] = 255 - thresh[pos-int(dic[height1][0]):pos+int(dic[height1][1]),int(ele[1])] #這裡可以更改回歸線條上下範圍
            print(dic[height1][0], dic[height1][1])

        plt.imshow(thresh)
        newdst = transform.resize(thresh, (48, 140)) #resize (h,w)
        plt.close() #close figure of origine size
        plt.figure(figsize=(140, 48), dpi=100) #存成固定大小 (w, h)
        plt.axis('off')
        plt.imshow(newdst)

        plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)#去白邊
        plt.savefig('./processed_image/'+str(count)+'.jpg',dpi=1)
        count += 1


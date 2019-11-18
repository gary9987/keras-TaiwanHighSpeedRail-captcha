from PIL import Image, ImageDraw, ImageFont
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils  import np_utils
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
import csv
import time

dic19 = {'2':0, '3':1, '4':2, '5':3, '7':4, '9':5, 'a':6, 'c':7, 'f':8, 'h':9, 'k':10, 'm':11, 'n':12, 'p':13, 'q':14, 'r':15, 't':16, 'y':17, 'z':18}
def to_onelist(text):
    label_list = []
    for c in text:
        onehot = [0 for _ in range(19)]
        onehot[ dic19[c] ] = 1
        label_list.append(onehot)
    return label_list

def to_text2(int):
    text = []
    text.append(list(dic19.keys())[list(dic19.values()).index(int)])
    return "".join(text)


model = load_model('model/cnn_model.hdf5')

def predict():
    index = 1
    x_train = np.stack([np.array(Image.open("get_image/2/img/" + str(index) + ".jpg"))/255.0 for index in range(1, index+1, 1)])

    print('predict start')

    prediction = model.predict(x_train)
    resultlist = ["" for _ in range(index)]
    for predict in prediction:
        for index in range(index):
            resultlist[index] += to_text2(np.argmax(predict[index]))

    return resultlist[0]


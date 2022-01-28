from PIL import Image, ImageDraw, ImageFont
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import np_utils
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

def to_text(l_list):
    text=[]
    pos = []
    for i in range(4):
        for j in range(19):
            if(l_list[i][j]):
                pos.append(j)

    for i in range(4):
        char_idx = pos[i]
        text.append(list(dic19.keys())[list(dic19.values()).index(char_idx)])
        return "".join(text)

def to_text2(int):
    text = []
    text.append(list(dic19.keys())[list(dic19.values()).index(int)])
    return "".join(text)

if __name__ == '__main__':
    print('trained_model loading...')
    model = load_model('./trained_model/cnn_model.hdf5')

    test_num = 1+5000 #test number

    print("Reading data...")
    x_train = np.stack([np.array(Image.open("../download_img/processed_image/" + str(index) + ".jpg"))/255.0 for index in range(1, test_num, 1)])

    print('predict start')
    tStart = time.time()#計時開始

    prediction = model.predict(x_train)
    print('preficted ')
    resultlist = ["" for _ in range(test_num-1)]

    for predict in prediction:
        for index in range(test_num-1):
            resultlist[index] += to_text2(np.argmax(predict[index]))

    tEnd = time.time()#計時結束


    traincsv = open('../download_img/label5000.csv', 'r', encoding='utf8')
    cipher_lebal = [row[0] for row in csv.reader(traincsv)]
    read_label = [to_onelist(row[0]) for row in csv.reader(traincsv)]

    count = 0
    correct = 0
    for result in resultlist:
        print(result, cipher_lebal[count])
        if result == cipher_lebal[count]:
            correct += 1
        count += 1

    print(correct/count) #答對率
    #列印計時結果
    print('It cost %f sec' % (tEnd - tStart)) #會自動做進位



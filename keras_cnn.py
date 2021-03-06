from __future__ import print_function
from __future__ import division
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import tarfile
import time
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os
import time
import pandas as pd
import re
from gensim.models.doc2vec import LabeledSentence, Doc2Vec
import random
from sklearn import metrics
df = pd.read_csv("ldata.csv")
headers = list(df.columns.values)

df = df[df.Praise.notnull()]
df = df[df.Problem.notnull()]
df = df[df.Mitigation.notnull()]
df = df[df.Summary.notnull()]
df = df[df.Solution.notnull()]
df = df[df.Neutrality.notnull()]
df = df[df.Localization.notnull()]

df_x = df.loc[:, ['Comments']]

headers.remove('Comments')
headers = ["Solution"]

df_y = df.loc[:, headers]
df_y.head()
df_y[df_y != 0] = 1
df_y = df_y.round(0).astype(int)
df_y['new'] = 1 - df_y
#load model
model = Doc2Vec.load("comments2vec.d2v")


comments = []
for index, row in df.iterrows():
    line = row["Comments"]
    line = re.sub("[^a-zA-Z?!]"," ", line)
    words = [w.lower().decode('utf-8') for w in line.strip().split() if len(w)>=3]
    comments.append(words)
x_train = []
for comment in comments:
        feature_vec = model.infer_vector(comment)
        x_train.append(feature_vec)


x_test = x_train[len(x_train)-100:len(x_train)]
x_train = x_train[0:len(x_train)-100]
y_train = df_y[0:len(x_train)]
y_test = df_y[len(x_train):]
inputX = np.array(x_train)
inputY = y_train.as_matrix()
outputX = np.array(x_test)
outputY = y_test.as_matrix()
numFeatures = inputX.shape[1]
numEpochs  = 1000
n_classes = 2
x_test=np.array(x_test)
y_test=np.array(y_test)
x_train=np.array(x_train)
y_train=np.array(y_train)
x_train = x_train.reshape(x_train.shape[0], 1, 1, 50)
x_test = x_test.reshape(x_test.shape[0], 1, 1, 50)
x = K.placeholder(shape= (5,5, numFeatures))
y = K.floatx()
input_shape=(1,1,50)
print(input_shape)
keep_rate = 0.8
keep_prob = K.floatx()
print(x_test.shape)
model = Sequential()
model.add(Conv2D(32, kernel_size=(1, 1),activation='relu',input_shape=(1,1,numFeatures)))
model.add(Conv2D(64, (1, 1), activation='relu'))
model.add(MaxPooling2D(pool_size=(1, 1)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(n_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,epochs=numEpochs,verbose=1,validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#!/usr/bin/env python
# coding: utf-8


import math
from pandas_datareader import data as pdr
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import tensorflow as tf




df = pd.read_csv('/home/icarus/Downloads/Stocks/NABIL.csv', index_col = 'Date', parse_dates=True)
df.replace(',','', regex=True, inplace=True)
c = df.select_dtypes(object).columns
df[c] = df[c].apply(pd.to_numeric,errors='coerce')




#create a new dataframe with only the close column
data = df.filter(['LTP'])
#convert the dataframe to a numpy array
dataset = data.values
#get the number of rows to train the model on
training_data_len = round(len(dataset)*  .85)
training_data_len


#scale the data
#apply preprocessing input datas before feeding to lstm model
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset) #the range will be 0 to 1 inclusive



#create the training data set
#create the scaled training data set
train_data = scaled_data[0:training_data_len , :]
#split the data into x_train and y_train
x_train = []
y_train = []

for i in range(60,len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])



x_train, y_train = np.array(x_train), np.array(y_train)



#reshaoe the data lstm expecting three dimensional data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape




# build the lstm model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1], 1 )))
model.add(LSTM(50, return_sequences = False))
model.add(Dense(25))
model.add(Dense(1))



#complile the model
model.compile(optimizer='adam', loss='mean_squared_error')



callback = tf.keras.callbacks.ModelCheckpoint('model.hdf5', 
                                              monitor='loss', 
                                              save_best_only=True, verbose=1)
model.fit(x_train, y_train, batch_size =1, epochs = 300, callbacks=[callback])



model.save('/home/icarus/Downloads/Stocks/model.hdf5')






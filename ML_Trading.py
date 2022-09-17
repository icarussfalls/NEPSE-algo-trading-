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
from numpy import loadtxt
from tensorflow.keras.models import load_model
import warnings
import pandas as pd
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
from datetime import datetime, timedelta
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



class ML():
    scaler = MinMaxScaler(feature_range=(0,1))
    def __init__(self, stock_data, model_path, column_to_read, days_to_predict):
        self.stock_data = stock_data
        self.model = tf.keras.models.load_model(model_path)
        self.column_to_read = column_to_read
        self.days_to_predict = days_to_predict
        
  
    def pred_values(self, a4):
        a4 = a4.reshape(-1,1)
        last_60_dayss = a4[-60:]
        last_60_dayss = self.scaler.fit_transform(last_60_dayss)
        next_test = []
        next_test.append(last_60_dayss)
        next_test = np.array(next_test)
        next_test = np.reshape(next_test, (next_test.shape[0], next_test.shape[1], 1))
        price = self.model.predict(next_test)
        price_scaled = self.scaler.inverse_transform(price)
        return price_scaled
    

    def funct(self, a, b, steps = 1):
          while steps < self.days_to_predict:
            e = np.append(a,b)
            d = self.pred_values(e)
            return self.funct(e,d, steps+1)
          else:
            return np.array(a)
    
    def predictions(self):
        quote = pd.read_csv(self.stock_data)
        a = quote.filter([self.column_to_read])
        a.dropna()
        #get the last 60 days closing values and convert the dataframe to an array
        last_60_days = a[-60:].values
        #scale the data to be values between 0 and 1
        last_60_days_scaled = self.scaler.fit_transform(last_60_days)
        #create an empty list
        X_test = []
        #append the past 60 days to X_test list
        X_test.append(last_60_days_scaled)
        #convert the X_test data set to a numpy array
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        pred_price = self.model.predict(X_test)
        pred_price = self.scaler.inverse_transform(pred_price)
        pred_price  = float(pred_price)
        a1 = a.to_numpy()
        a2 = np.array(pred_price)
        a3 = np.append(a1,a2)
        m = self.pred_values(a3)                   
        return self.funct(a3,m)[len(quote):]
    
    def get_pred(self):
        days = self.days_to_predict
        daterange = []

        for i in range(1, days):
            tomorrow = datetime.now() + timedelta(days=i)
            if tomorrow.weekday() != 5:
                daterange.append(tomorrow.strftime('%m-%d-%y'))
                
        daterange_ = pd.to_datetime(daterange)
        n = len(daterange_)
        preds = self.predictions()[:n]
        df = pd.DataFrame(preds, index = daterange)
        df.columns = ['Predictions']
        return df
    
    def get_dates(self):
        a = self.get_pred()
        my_max_ind = a['Predictions'].idxmax()
        my_min_ind = a['Predictions'].idxmin()
        if my_max_ind > my_min_ind:
            return my_min_ind, my_max_ind
        else:
            return False
        
    def preds(self):
        try:
            listt = self.get_dates()
            return listt
        except:
            print("False flag raised, no trades found")
            return
        
        


# buy_date, sell_date = ML('/home/icarus/Downloads/HIDCL - Sheet1.csv', '/home/icarus/Downloads/hidcl.h5', '%wp_change', 30 ).preds()


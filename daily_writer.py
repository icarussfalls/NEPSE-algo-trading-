#!/usr/bin/env python
# coding: utf-8



import csv
from csv import writer
from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select
import numpy as np
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import warnings
warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
from selenium.webdriver.chrome.service import Service
from multiprocessing import Pool




class daily_writer():
    def __init__(self, url):
        options.add_argument('--no-sandbox')
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(options = options, executable_path='/home/icarus/Downloads/chromedriver_linux64 (1)/chromedriver')
        self.url = url
        self.driver.get(url)
        time.sleep(2)
        self.driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]').click()
        self.driver.implicitly_wait(2)
        
    def df(self):
        time.sleep(2)
        Date = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[2]')
        LTP = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[3]')
        Change = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[4]')
        High = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[5]')
        Low = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[6]')                            
        Open = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[7]')
        Quantity = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[8]')
        Turnover = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr[2]/td[9]')
        data = pd.DataFrame(columns=['Date', 'LTP', 'Change', 'High', 'Low', 'Open', 'Quantity', 'Turnover'])
        for i in range(len(Date)):
            data = data.append({'Date': Date[i].text, 'LTP': LTP[i].text, 'Change': Change[i].text, 'High': High[i].text, 'Low': Low[i].text, 'Open': Open[i].text, 'Quantity': Quantity[i].text, 'Turnover' : Turnover[i].text}, ignore_index = True)
        return data



input_string = input("Enter stocks seperated by space: ")
stocks = input_string.split(" ")
def write_to_file(i):
    x = 'https://merolagani.com/CompanyDetail.aspx?symbol='
    x += str(i)
    y = daily_writer(x).df()
    path =  r'/home/icarus/Downloads/Stocks/'
    path += str(i) +'.csv'
    y.to_csv(path, mode = 'a', index = False, header = False)
    
    
    
if __name__ == '__main__':  
        with Pool() as pool:
            pool.map(write_to_file, stocks)


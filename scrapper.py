#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
import os
from webdriver_manager.chrome import ChromeDriverManager
import time
from fake_useragent import UserAgent
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



class scrapper():
    def __init__(self, url):
        ua = UserAgent()
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("start-maximized")
        options.add_argument("--headless")
        options.add_argument(f'user-agent={ua.random}') # add random user agent
        self.driver = webdriver.Chrome(options = options) #path to chromedriver
        self.url = url
        self.driver.get(url)
        time.sleep(2)
        self.driver.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_lnkHistoryTab"]').click()
        self.driver.implicitly_wait(2)
        
    def df(self):
        time.sleep(2)
        Date = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[2]')
        LTP = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[3]')
        Change = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[4]')
        High = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[5]')
        Low = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[6]')                            
        Open = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[7]')
        Quantity = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[8]')
        Turnover = self.driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[2]/table/tbody/tr/td[9]')
        data = pd.DataFrame(columns=['Date', 'LTP', 'Change', 'High', 'Low', 'Open', 'Quantity', 'Turnover'])
        for i in range(len(Date)):
            data = data.append({'Date': Date[i].text, 'LTP': LTP[i].text, 'Change': Change[i].text, 'High': High[i].text, 'Low': Low[i].text, 'Open': Open[i].text, 'Quantity': Quantity[i].text, 'Turnover' : Turnover[i].text}, ignore_index = True)
        # sort the data by date in ascending order
        #data['Date'] = pd.to_datetime(data['Date'], format='%Y/%m/%d')
        #data = data.sort_values(by='Date', ascending=True).reset_index(drop=True)
        return data

        
    
    def datas(self):
        print("Started")
        data = []
        data.append(self.df())
        time.sleep(1)
        while True:
            try:                
                k = self.driver.find_element("xpath", '//*[@title = "Next Page"]')
                actions = ActionChains(self.driver)
                actions.move_to_element(k).click().perform()
                scrap = self.df()
                data.append(scrap)
            except:
                print("Finished")
                break
        data = pd.concat(data, axis = 0)
        return data


stock = ['NTC', 'NABIL']


def save_datas(i):
    x = 'https://merolagani.com/CompanyDetail.aspx?symbol='
    x += str(i)
    y = scrapper(x).datas()
    filename = f"{i}.csv"
    path = os.path.join(os.getcwd(), filename)
    y.to_csv(path, index=None, header=True)
    print(f"Data saved for {i} in {path}")





if __name__ == '__main__':  
        with Pool() as pool:
            pool.map(save_datas, stock)
# call the same function with different data sequentially

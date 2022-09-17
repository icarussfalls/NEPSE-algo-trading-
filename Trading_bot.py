#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select
import numpy as np
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
driver = webdriver.Chrome(executable_path='/home/icarus/Downloads/chromedriver_linux64 (1)/chromedriver') #path to chromedriver
import sys



#creating the class
class trading_bot():
    loginURL = "https://tms58.nepsetms.com.np/login"
    order_entry_url = 'https://tms58.nepsetms.com.np/tms/me/memberclientorderentry' #broker_url
    
    def __init__(self):
        pass
        
    def login(self, username, password):
        self.username = username
        self.password = password
        print("Loggin in to the tms dashboard")
        self.driver.get(self.loginURL)
        login = self.driver.find_element('xpath','/html/body/app-root/app-login/div/div/div[2]/form/div[1]/input')
        login.send_keys(self.username)
        password = self.driver.find_element("xpath", "/html/body/app-root/app-login/div/div/div[2]/form/div[2]/input")
        password.send_keys(self.password)
        time.sleep(10)
        self.driver.find_element("xpath", "/html/body/app-root/app-login/div/div/div[2]/form/div[4]/input").click()
        print("Successfully logged in")
        
    def buy_request(self, stock, quantity, price):
        self.quantity = quantity
        self.stock = stock
        self.price = price
        self.driver.get(self.order_entry_url)
        time.sleep(5)
        try:
            self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[3]").click()
    
        except:    
            self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/div").click()
            self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[3]").click()
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[2]/input").send_keys(self.stock) #input stock name
        time.sleep(2)
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[2]/typeahead-container/button").click() #select stock from dropdown menu
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[3]/input").send_keys(self.quantity) #quantity to buy
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[4]/input").send_keys(self.price) #price to buy
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[3]/div[2]/button[1]").click() #submit

    def sell_request(self, stock, quantity, price):
        self.quantity = quantity
        self.stock = stock
        self.price = price
        self.driver.get(self.order_entry_url)
        time.sleep(5)
        try:
            self.driver.find_element("xpath",'/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[1]').click()
        except:
            self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[2]").click()
            self.driver.find_element("xpath", '/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[1]/div[2]/app-three-state-toggle/div/div/label[3]' ).click()
        self.driver.find_element(By.XPATH, '/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[2]/input').send_keys(self.stock)
        time.sleep(2)
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[2]/typeahead-container/button/span").click()
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[3]/input").send_keys(self.quantity)
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[2]/div[4]/input").send_keys(self.price)
        self.driver.find_element("xpath", "/html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/form/div[3]/div[2]/button[1]").click()
        
    def buyers_table(self):
        try: 
            rows = WebDriverWait(self.driver,20).until(EC.visibility_of_all_elements_located((By.XPATH, ".//html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/div/div[1]/div/div[1]/div/table/tbody/tr")))
            data = []
            for row in rows:
                order_b = row.find_element("xpath", ".//td[1]").text
                quantity_b = row.find_element("xpath", ".//td[2]").text
                price_b = row.find_element("xpath", ".//td[3]").text
                data.append(("Orders :{},Quantity :{}, Price :{}".format((order_b),quantity_b,price_b)))
            return data
        except:
            return self.buyers_table()
    
    def sellers_table(self):
        try:
            rows_s = WebDriverWait(self.driver,20).until(EC.visibility_of_all_elements_located((By.XPATH, ".//html/body/app-root/tms/main/div/div/app-member-client-order-entry/div/div/div[3]/div/div[1]/div/div[2]/div/table/tbody/tr")))
            data_s = []
            for row_s in rows_s:
                price_s = row_s.find_element("xpath", ".//td[1]").text
                quantity_s = row_s.find_element("xpath", ".//td[2]").text
                order_s = row_s.find_element("xpath", ".//td[3]").text
                data_s.append(("Orders :{}, Quantity :{}, Price :{}".format(order_s,quantity_s,price_s)))
            return data_s

        except:
            return self.sellers_table()










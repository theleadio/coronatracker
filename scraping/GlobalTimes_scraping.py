# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 00:37:44 2020

@author: Heng1222
"""

from selenium import webdriver
from time import sleep
import os, subprocess
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

class GlobalTimeScraper:

	def __init__(
		self,
		row = 0,
		col = 0,
		df = "";
		data = [],
	):

	now = datetime.datetime.now()
	chrome_options = webdriver.ChromeOptions()
	driver = webdriver.Chrome('chromedriver', options=chrome_options)
	driver.get("https://www.globaltimes.cn/content/1177737.shtml")
	WebDriverWait(driver,100000000).until(EC.presence_of_element_located((By.XPATH,'//*[@id="left"]/div[4]/div')))
	news= driver.find_element_by_css_selector('#left > div:nth-child(4) > div')
	df=news.text
	data=df.splitlines()
	#delete unrelevant data
	while ("" in data):
	    data.remove("")
	del data[0]
	del data[-1]
	del data[-1]
	del data[-1]
	del data[-1]
	df=pd.DataFrame(data)
	df.to_csv('GlobalTimes.csv',index=False,header=False)
	print("done")

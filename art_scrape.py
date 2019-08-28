# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:10:15 2018

@author: vball
"""
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
#import urlparse
from selenium import webdriver
from csv import DictWriter
import json


#Step 1. Generating first level urls, for month 1-12, year 1998-2016, possible page range: 1-3
url_list=[]
for i in range(1,13):
    for j in range (2016, 2017):
        for k in range(1,4):
            urll='http://www.christies.com/results/?month='+str(i)+'&year='+str(j)+'&locations=&scids=&action=paging&initialpageload=false&pg='+str(k)
            url_list.append(urll)
            #print urll
print(len(url_list))

#Step 2. Reading url into html files
tmp_list=[]

for url in url_list: 
    
    try:
        auction = urlopen(url)     
        html = auction.read()
        soup = BeautifulSoup(html)
        grand_list = soup.find("ul", {"id": "list-items"})
        #creating a sub_soup
        sub_soup = BeautifulSoup(str(grand_list))
        events = sub_soup.find_all("li", id = re.compile('^day-')) 
        print('.')
    except:
        print(url)
        pass
    print('-')
    #inner loop to construct a dictionary for each event:
    final_result = []
    for event in events:
        try:
            auction = {}
            url_find = event.find("a", {"class": "description"}).get('href').encode('ascii', 'ignore').strip()
            auction['month'] = event.find("span", "month").get_text().encode('ascii', 'ignore').strip()
            auction['date'] = event.find("span", "date").get_text().encode('ascii', 'ignore').strip()
            auction['year'] =  event.find("span", "year").get_text().encode('ascii', 'ignore').strip()
            auction['ID'] = event.find("a", {"class": "sale-number"}).get_text().encode('ascii', 'ignore').strip()
            auction['location'] = event.find("span", "location").get_text().encode('ascii', 'ignore').strip()
            auction['event_name'] = event.find("a", {"class": "description"}).get_text().encode('ascii', 'ignore').strip()
            auction['total_sales'] = event.find("ul", {"class": "auction-links"}).find('a').get_text().encode('ascii', 'ignore').strip()
            auction['url'] = "http://www.christies.com" + url_find
            final_result.append(auction)
            #
            print(auction['month'])
        except Exception as e:
            print(e)
    tmp_list += final_result
    
print(len(tmp_list))
'''


import pandas as pd
import numpy as np

art = pd.read_csv('C:/Users/vball/Downloads/Artworks.csv')
parenth_remove = ['ArtistBio','Nationality','BeginDate','EndDate','Gender']
for i in parenth_remove:
    art[i] = art[i].astype(str)
    art[i] = art[i].str.replace('(','')
    art[i] = art[i].str.replace(')','')
    art[i] = art[i].map(lambda x: x.strip('(').strip(')'))
    
art = pd.concat([art, art['ArtistBio'].str.split(',', expand=True)[0]], axis=1)

art['Date'] = art['Date'].str.extract('(\d+)', expand=False)
art['BeginDate'] = art['BeginDate'].str.extract('(\d+)', expand=False)
art['EndDate'] = art['EndDate'].str.extract('(\d+)', expand=False)
art['Date'] = art['Date'].astype(float)
art['BeginDate'] = art['BeginDate'].astype(float)
art['EndDate'] = art['EndDate'].astype(float)
art['EndDate'] = art['EndDate'].replace(0,2018)
art['artist_age_at_work'] = art['Date'] - art['BeginDate']
art['artist_age_acq'] = art['EndDate'] - pd.to_datetime(art['DateAcquired'], errors = 'coerce').dt.year
art['artist_dead'] = np.where(art['artist_age_acq'] > 0, 0, 1)


how_much = art.loc[art['Artist'] == 'Vincent van Gogh']







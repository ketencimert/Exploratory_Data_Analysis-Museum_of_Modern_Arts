# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 11:11:47 2018

@author: Mert Ketenci
"""

import pandas as pd
import numpy as np
art = pd.read_csv('C:\\Users\\Mert Ketenci\\Desktop\\EDAV\\Term Project\\MOMA_art_cleaned.csv') 



art = art.astype(str)


for i in range(149545):
    if art['DateAcquired'][i] == "NA":
        i=i+1
    else:
        art['DateAcquired'][i] = pd.to_datetime(art['DateAcquired'][i]) 
    

try:
    art['MonthAcquired'] = art['DateAcquired'].month
except:
    art['MonthAcquired'] = "NA"

for i in range(149545):
    if art['DateAcquired'][i] == "NA":
        i=i+1
    else:
        art['MonthAcquired'][i] = pd.to_datetime(art['DateAcquired'][i]).month     

    
art[art['Date'].map(len) != 6] = "NA"
art.replace("nan", 'NA', inplace=True)
art.replace("0", 'NA', inplace=True)
art.replace("0.0", 'NA', inplace=True)
art.replace("Unknown", 'NA', inplace=True)

art.to_csv('C:\\Users\\Mert Ketenci\\Desktop\\EDAV\\Term Project\\MOMA_art_cleaned2.csv', sep=',')
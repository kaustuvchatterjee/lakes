#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
from datetime import datetime


url = "https://memumbai.com/water-levels-of-mumbai-dams-lakes/"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text,"html.parser")


str="Below is the water level reported at 6 a.m. on 22nd June 2021 in million litres (ML)"
dateP = soup.find('p',text = re.compile('Below is the water level reported at*'))
str = dateP.text
x = re.search('\son\s',str)
start = x.end()
x = re.search('\sin\s',str)
end = x.start()
obsDate = str[start:end]
obsDate = re.sub(r"\b([0123]?[0-9])(st|th|nd|rd)\b",r"\1",obsDate)
obsDate = datetime.strptime(obsDate,'%d %B %Y')
print(obsDate)


str = "wptb-preview-table wptb-element-main-table_setting-21257 edit-active"
data_table = soup.find('table',{'class':str})
data = data_table.find_all('tr')
lake = []
level = []
capacity = []
for i in np.arange(2,8,1):
    lake.append(data[i].find_all('td')[0].text.strip())
    level.append(int(data[i].find_all('td')[1].text.strip()))
    capacity.append(int(data[i].find_all('td')[2].text.strip()))

content = 100*np.array(level)/np.array(capacity)


df = pd.read_csv('lakelevels.csv')
df['date'] = pd.to_datetime(df['date'])


if obsDate not in df.values:
    dct = {'date':obsDate, 'lake':lake, 'level':level, 'capacity':capacity, 'content':content}
    df2 = pd.DataFrame(dct)
    df = df.append(df2, ignore_index=True)
    df.to_csv('lakelevels.csv')


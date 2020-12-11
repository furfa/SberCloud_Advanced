#!/usr/bin/env python
# coding: utf-8

# In[16]:


import requests
from bs4 import BeautifulSoup

def BS(html):
    return BeautifulSoup(html, features="lxml")
import pandas as pd
import numpy as np
import re
from datetime import datetime

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request


def get_html(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return urllib.request.urlopen(req).read()


# In[17]:


import sys, os
sys.path.append(os.path.join(sys.path[0], "../..") )
from tools.functions import *


# In[18]:


def get_html_rec(url, max_depth=1, curr_depth=1):
    try:
        html = get_html(url)
        return html
    except UnicodeDecodeError:
        print("UnicodeDecodeError", url)
        sleep(10)
        if curr_depth < max_depth:
            html = get_html_rec(url, max_depth, curr_depth+1)
            return html
        print("Не удалось")
        raise


# In[19]:


prev_years = pd.read_html("https://abit.itmo.ru/pass_rate/", header=0)[0]
prev_years.columns = ['Шифр', 'Направление подготовки (специальность)', 'Предметы',
       'Проходной балл (ЕГЭ+ИД) 2017', 'Средний балл (ЕГЭ) 2017', 
       'Проходной балл (ЕГЭ+ИД) 2018', 'Средний балл (ЕГЭ) 2018', 
       'Проходной балл (ЕГЭ+ИД) 2019', 'Средний балл (ЕГЭ) 2019', 
    ]


# In[20]:


html = get_html("https://abit.itmo.ru/bachelor/rating_rank/all/")
page = BS(html)

fac_list = {}
for fac in page.select_one(".static-page-rule > div:nth-child(1) > ul:nth-child(2)").select("li > a"):
    fac_list[fac.text] = "https://abit.itmo.ru" + fac.attrs['href']
fac_list


# In[21]:


fac_name = '01.03.02 «Прикладная математика и информатика»'


# In[22]:


def parse_ifmo(fac_name):

    url = fac_list.get(fac_name)
    
    html = get_html_rec(url, 7)
        
        

    table = pd.read_html(html, header=1)[0]

    date = BS(html).select_one(".static-page-rule > div:nth-child(1) > p:nth-child(5)").text[23:]

    # print(date)

    header_str = BS(html).select_one(".static-page-rule > div:nth-child(1) > h1:nth-child(1)").text

    def parse_K(s):
        spn = re.search(r",К:\d+", s).span()
        num = s[spn[0]:spn[1]][3:]
        # print("num is " + num)
        return int(num)

    free_places = parse_K(header_str)
    num_olymp = table[table["Условие поступления"] == "без вступительных испытаний"].shape[0]

    if num_olymp < free_places:
        free_places -= num_olymp
    else:
        free_places = 0
    
    scores = table[table["Условие поступления"] == 'по общему конкурсу']["ЕГЭ+ИД"]
    scores = [ int( re.search(r"\d+", str(i)).group(0) ) if str(i)[:3] != "nan" else 0 for i in scores]
    
    scores = np.sort(scores)[::-1]
#     return (scores)

    code = re.search(r"\d{2}.\d{2}.\d{2}",header_str).group(0)
    date_updated = datetime.strptime(date, "%H:%M:%S %d.%m.%Y")

    # print(code)
    
    try:
        prev_years_list = list(
            prev_years[prev_years["Шифр"] == code][ 
                ["Проходной балл (ЕГЭ+ИД) 2017", "Проходной балл (ЕГЭ+ИД) 2018", "Проходной балл (ЕГЭ+ИД) 2019"] 
            ].values[0].astype(int)
        )
    except IndexError:
        prev_years_list = [-1, -1, -1]
        
    budjet_scores = scores[:free_places]
    
    
    
    if free_places == 0:
        last_score = 999
    else:
        last_score = budjet_scores[-1] if len(scores) >= free_places else 0
    

    res = {
        "fac_name" : fac_name,
        "url" : url,
        "date_updated" : f"{str(datetime_to_utc(date_updated) )}",
        "scores" : budjet_scores,
        "last_score" : last_score,
        "free_places" : free_places,
        "olymp_cnt" : num_olymp,
        "prev_years17" : prev_years_list[0] if prev_years_list[0] >= 0 else None,
        "prev_years18" : prev_years_list[1] if prev_years_list[1] >= 0 else None,
        "prev_years19" : prev_years_list[2] if prev_years_list[2] >= 0 else None,
    }
    return res


# In[23]:


# from tqdm import tqdm_notebook as tqdm
from tqdm import tqdm
from time import sleep


# In[24]:


parse_ifmo("09.03.01 «Информатика и вычислительная техника»")


# In[25]:


Parsed_ifmo = []

for name, link in tqdm(fac_list.items() ):
    # print(name, link)
    Parsed_ifmo.append(
        
        parse_ifmo(name)
    
    )
    
    sleep(2)


# In[26]:


pd.DataFrame(Parsed_ifmo)


# In[27]:


for i in Parsed_ifmo:
    i["scores"] =  list( i["scores"] )


# In[28]:


import json


# In[29]:


Parsed_ifmo = (str( datetime.utcnow()), Parsed_ifmo)


# In[30]:


Parsed_ifmo


# In[31]:


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# In[32]:


json_dump = json.dumps(Parsed_ifmo, cls=NumpyEncoder)


# In[33]:


file_name = save_file(json_dump)


# In[34]:


# (Дата создания, [
#     {
#         'fac_name' : Название фака, 
#         'date_updated': Дата с сайта(если есть) или нон есои нет, 
#         'scores': [] Список баллов, 
#         'last_score': Последний балл на бюджет, 
#         'free_places': Количество мест , 
#         'olymp_cnt': Количество бви, 
#         'prev_years17': проходной за 17 год, 
#         'prev_years18': проходной за 18 год, 
#         'prev_years19':  проходной за 19 год,
#     },
#     
# ])

# In[ ]:

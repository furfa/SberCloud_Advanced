import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import math

import sys, os
sys.path.append(os.path.join(sys.path[0], "../..") )
from tools.functions import save_file, datetime_to_utc
import json

facults = {}

def get_abit():
    url = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html'
    list_prefix = 'https://cabinet.spbu.ru/Lists/1k_EntryLists/'

    #data - json about all faculty and date when parser was runned
    data = [str(datetime.utcnow()), []]

    list_html = requests.get(url)
    list_bs = BeautifulSoup(list_html.content, 'html.parser')
    list_hrefs = list_bs.find_all(lambda tag: tag.text == 'Госбюджетная')

    #url = url_prefix + url_postfix 
    urls = list(map(lambda x: list_prefix+x['href'], list_hrefs))

    for direction_url in urls:
        direction_html = requests.get(direction_url)
        direction_bs = BeautifulSoup(direction_html.content, 'html.parser')
        
        info = direction_bs.find_all('p')
        direction = list(info[0])[14][1:]
        free_places = int(list(info[0])[28][1:])
        date = info[1].text
        table = (pd.read_html(direction_html.content))[0]
        
        all_b = direction_bs.find_all('b')
        disciplines = []
        for b_ in all_b:
            b_s = str(b_)
            if 'ВИ' in b_s:
                disciplines.append(b_s[10:-4])
        facults[direction] = disciplines

        abits_raw = list(table['Σ общ'])
        abits = []
        for abit in abits_raw:
            if math.isnan(abit):
                abits.append(None)
            else:
                abits.append(int(abit/10))
        
        out_competition = len(table[table['Тип конкурса'] == 'б/э'])

        #info about one facult
        data[1].append({
            'fac_name': direction,
            'url': direction_url,
            'date_updated': str(datetime_to_utc( datetime.strptime(date, "Время последнего обновления: %d.%m.%Y %H:%M") ) ),
            'scores': abits[:free_places],
            'last_score': abits[free_places-1],
            'free_places': free_places - out_competition,
            'olymp_cnt': out_competition,
            'prev_years17': None,
            'prev_years18': None,
            'prev_years19': None
        })
    return data

abiturients = get_abit()


# for i in facults.keys(): 
#     for j in range(len(facults[i])): 
#         if facults[i][j].startswith("Творческий конкурс"): 
#             facults[i][j] = "Творческий конкурс" 
#         if facults[i][j].startswith("Физическая культура"):  
#             facults[i][j] = "Физическая культура" 

# with open("disciplines.json", "w") as file:
#     file.write( json.dumps( facults) )


save_file(json.dumps(abiturients))
#!/usr/bin/env python
# coding: utf-8

# In[25]:


from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sys, os
sys.path.append(os.path.join(sys.path[0], "../..") )
from tools.functions import save_file, datetime_to_utc


# * date
# * 
# * **fac_name**
# * **date_updated**
# * **scores**
# * **last_score**
# * **free_places**
# * **olymp_count**
# * **url**
# * prev_years 17 18 19

# In[8]:


domain = "http://www.stu.ru"

full_time = "http://www.stu.ru/abiturient/abiturients_table_show.php?type=podavshie_obshii_bud"
distance = "http://www.stu.ru/abiturient/abiturients_table_show.php?type=podavshie_zaoch_bud"


# In[9]:


def parse_facs(url):
    res = {}
    soup = BeautifulSoup(requests.get(url).text, "html5lib")
    table = soup.find_all("table")[0]
    for fac in table.tbody.find_all("tr")[2:]:
        name = fac.find_all("td")[0].text.strip()
        href = fac.find_all("td")[1]
        if href.text != "":
            if href.a is not None:
                res[name] = [a_tag["href"].replace("БЮД", "%C1%DE%C4") for a_tag in href.find_all("a")]
    return res


# In[18]:


facs = parse_facs(full_time)
facs.update(parse_facs(distance))

time_utc_now = datetime.utcnow()

res = [str(time_utc_now), []]

###############
#             #
#   К0СТЫЛЬ   #
#             #
###############
free = {
    "08.03.01": [8, 19],
    "09.03.02": [19],
    "09.03.03": [16],
    "20.03.01": [11],
    "23.03.01": [16],
    "23.03.03": [43],
    "27.03.01": [16]
}

for fac, urls in list(facs.items()):
    for i, url in enumerate(urls):
        print(domain + url)
        info_about_course = {}
        soup = BeautifulSoup(requests.get(domain + url).text, "html5lib")

        info_about_course["fac_name"] = fac + " " + soup.find("div", {"id": "page_text"}).div.find_all("h3")[1].text
        info_about_course["date_updated"] = str(time_utc_now)
        info_about_course["olymp_cnt"] = 0
        info_about_course["url"] = domain + url
        
        scores = []
        table = soup.find("table").tbody
        for st in table.find_all("tr")[2:(free[fac[:8]][i] if fac[:8] in free.keys() else 0)]:
            scores.append(int(st.find_all("td")[6].text))
            
        curr_free = 0
        elem = free.get(fac[:8])
        if elem:
            curr_free = elem[i]
            
            
        info_about_course["free_places"] = curr_free - info_about_course["olymp_cnt"]
        
        info_about_course["scores"] = (scores if len(scores) else None)
        info_about_course["last_score"] = (scores[-1] if len(scores) else None)
        print(curr_free)

    res[1].append(info_about_course)
    


# In[21]:


import json


# In[26]:


save_file(json.dumps(res))


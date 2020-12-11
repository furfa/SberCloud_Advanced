from bs4 import BeautifulSoup
import requests
import json

import sys, os
sys.path.append(os.path.join(sys.path[0], "../..") )
from tools.functions import *
from datetime import datetime

def make_soup(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, features="html5lib")
    return soup

def find_links_to_ratings():
    result = {} 
    
    soup = make_soup("https://www.nstu.ru/entrance/admission_campaign/entrance")
    
    content = soup.find_all("div", {"class": "pleft"})
    tags = [i for i in content[0].children]
    
    for tag in tags:
        if tag.name == "h3":
            faculty_name = tag.text.strip()
            if (faculty_name == "Программы бакалавриата и специалитета, специальности среднего профессионального образования"):
                continue
            if (faculty_name == "Программы магистратуры"):
                break

            result[faculty_name] = {}
        if tag.name == "table":
            if tag.tbody.tr.td.text.strip()[-8:] == "Бакалавр":
                course_name = tag.tbody.tr.td.text.split(",")[0].strip().replace("\xa0", " ")
                link = tag.find("span").a["href"]
                result[faculty_name][course_name] = link
    return result

def get_information_about_course(soup):
    content = soup.find_all("main", {"class": "page-content"})[0]
    
    # date
    idx = content.text.find("Время")

    #datetime.strptime(list_response['info']['date'], "Дата формирования - %d.%m.%Y. Время формирования - %H:%M:%S.")
    date = content.text[idx+49:idx+69].strip()
    date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    date = str( datetime_to_utc(date)  )
    
    # group
    group = content.find_all("b", string="Конкурсная группа: ")[0].next_sibling.strip().replace(" ", "")
    print(group)
    # free
    free_cnt = content.find_all("b", string="Количество бюджетных мест в конкурсной группе по всем условиям поступления: ")
    if len(free_cnt) != 0:
        free_cnt = free_cnt[0].next_sibling
        free_cnt = int("".join([i for i in free_cnt if i.isdigit()]))
    else:
        free_cnt = 0
    
    
    
    # rating
    table = content.table.find_all("tbody")[1].find_all("tr")
    
    k = 0
    scores = []
    for tag in table:
        data = tag.find_all("td")
        if data[0].b is not None:
            if data[0].b.i is not None:
                if data[0].b.i.text == "По конкурсу":
                    k = 1
                    continue
                if data[0].b.i.text == "Не выдержавшие вступительные испытания":
                    break
        if k != 0:
            if k == 1:
                olymp_cnt = int(data[0].text) - 1
                k = 2
            scores.append(int(data[10].b.text))
    scores = scores[olymp_cnt:free_cnt]
    
    return (date, free_cnt, olymp_cnt, scores, group)

def get_comp17():
    with open(os.path.join(sys.path[0],'c17.json') ) as json_file:
        data = json.load(json_file)
    return data

def get_comp18():
    with open(os.path.join(sys.path[0],'c18.json') ) as json_file:
        data = json.load(json_file)
    return data

def get_comp19():
    with open(os.path.join(sys.path[0],'c19.json') ) as json_file:
        data = json.load(json_file)
    return data

def get_subjects():
    with open(os.path.join(sys.path[0],'disciplines.json') ) as json_file:
        data = json.load(json_file)
    return data

data = find_links_to_ratings()
competition2017 = get_comp17()
competition2018 = get_comp18()
competition2019 = get_comp19()
subjects = get_subjects()

res = [str(datetime.utcnow()), []]
for faculty in list(data.keys()):
    for (course, link) in data[faculty].items():
        info_about_course = {}
        soup = make_soup(link)
        
        info_about_course["fac_name"] = faculty + " " + course
        
        info = get_information_about_course(soup)
        info_about_course["date_updated"] = info[0]
        info_about_course["scores"] = info[3]
        if (len(info[3]) != 0):
            info_about_course["last_score"] = info[3][-1]
        else:
            info_about_course["last_score"] = None
        info_about_course["free_places"] = info[1]
        info_about_course["olymp_cnt"] = info[2]
        
        info_about_course["url"] = link
        
        # info_about_course["subjects"] = subjects[info_about_course["fac_name"]]
        
        try:
            info_about_course["prev_years17"] = competition2017[info[4]]
        except KeyError:
            info_about_course["prev_years17"] = None
        try:
            info_about_course["prev_years18"] = competition2018[info[4]]
        except KeyError:
            info_about_course["prev_years18"] = None
        try:
            info_about_course["prev_years19"] = competition2019[info[4]]
        except KeyError:
            info_about_course["prev_years19"] = None 
        
        res[1].append(info_about_course)

save_file(json.dumps(res))
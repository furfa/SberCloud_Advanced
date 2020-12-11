import requests
from bs4 import BeautifulSoup
from datetime import datetime

import sys
import os
sys.path.append(os.path.join(sys.path[0], "../.."))
from tools.repeat_finder import find_repeats
from tools.functions import *
import json

import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

facults = {}
faculties_abiturients = {}
abiturients = []

FREE_PLACES = {
    "ИБ-бюджет (10.03.01 Информационная безопасность)" : 29,
    "ИБТС-бюджет (10.05.02 Информационная безопасность телекоммуникационных систем)" : 46,
    "ИВТ-бюджет (09.03.01 Информатика и вычислительная техника)" : 209,
    "ИКТСС-1-бюджет (11.03.02 Инфокоммуникационные технологии и системы связи)" : 202,
    "ИКТСС-2-бюджет (11.03.02 Инфокоммуникационные технологии и системы связи)" : 40,
    "ИСТ-бюджет (09.03.02 Информационные системы и технологии)" : 50,
    "КТЭС-бюджет (11.03.03 Конструирование и технология электронных средств)" : 40,
    "ПИ-бюджет (09.03.03 Прикладная информатика)" : 30,
    "РСО-бюджет (42.03.01 Реклама и связи с общественностью)" : 15,
    "РТ-бюджет (11.03.01 Радиотехника)" : 40,
    "СРС-бюджет (11.05.02 Специальные радиотехнические системы)" : 14,
    "ТБ-бюджет (20.03.01 Техносферная безопасность)" : 22,
    "ФИИТ-бюджет (02.03.02 Фундаментальная информатика и информационные технологии)" : 21,
    "ЭН-бюджет (11.03.04 Электроника и наноэлектроника)" : 20,
}

def add_repeats_to_data():
    repeats = find_repeats(faculties_abiturients)

    for faculty_index in range(len(abiturients[1])):
        if abiturients[1][faculty_index]['fac_name'] in repeats:
            abiturients[1][faculty_index]['n_severalfac'] = repeats[abiturients[1][faculty_index]['fac_name']]


def get_html(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
        }
    )
    return urllib.request.urlopen(req).read().decode("utf-8")

def get_html_by_page_num(base_url, num):
    return get_html( base_url.replace("page=1", f"page={num}") )


def parse_page(html, num):

    bs = BeautifulSoup( html,  'html.parser')

    if num == 1:
        return [i.text for i in bs.select(".mob ~ span")]

    text = str(bs.text) + "\n\n"
    new_text = ""
    for i in range(len(text) - 1):
        if text[i] == text[i+1] and text[i] == "\n":
            pass
        else:
            new_text += text[i]
    return new_text.replace("\n", " ").split()


def parse_splited_text(new_text):
    data = list()
    i = 0
    while i < len(new_text):
        name = ""
        while not new_text[i].isdigit():
            name += new_text[i] + " "
            i += 1
        name = name[:-1]
        
        summ = int(new_text[i])
        i += 6
        
        data.append( 
            (name, summ)
        )
    return data 

def process_FIO(fio):
    if len(fio) == 3:
        return fio
    if len(fio) > 3:
        return fio[:3]
    return fio + ['"'] * (3-len(fio) )

def get_abit():
    main_url = 'https://sibsutis.ru/abitur/konkursnye-spiski/bachelor/'
    
    #data - json about all faculty and date when parser was runned
    data = [str(datetime.utcnow()), []]

    main_html = get_html(main_url)
    main_bs = BeautifulSoup(main_html, 'html.parser')

    directions_raw = main_bs.find_all('option')
    directions = []
    for direction in directions_raw:
        if 'value' in direction.attrs:
            directions.append([f"https://sibsutis.ru/abitur/konkursnye-spiski/bachelor/konkursnye-spiski/?page=1&competitiveGroupID={direction.attrs['value']}&ajax=Y", direction.string])

    for direction in directions:
        direction_url = direction[0]
        print(direction_url)
        faculty_name = direction[1]

        direction_html = get_html(direction_url)
        direction_bs = BeautifulSoup(direction_html, 'html.parser')
        date_update = list(direction_bs.find_all('h2'))[-1].string

        if date_update.startswith("Отсутствует информация") or ('бюджет' not in faculty_name) or ('внебюджет' in faculty_name):
            continue

        free_places = FREE_PLACES[faculty_name]

        data_scores = list()
        prev_html = ""
        page_num = 1
        curr_html = get_html_by_page_num(direction_url, page_num)

        while prev_html != curr_html:
            
            data_scores.extend(
                parse_splited_text(parse_page(curr_html, page_num))
            )

            page_num += 1
            prev_html = curr_html
            curr_html = get_html_by_page_num(direction_url, page_num)

        data_scores = list(set(data_scores)) # Можно добавить имена

        data_scores.sort(reverse=True, key=lambda x:x[1])

        scores = [i[1] for i in data_scores]

        faculties_abiturients[faculty_name] = [
            process_FIO( i[0].split() ) for i in data_scores[:free_places]
        ]
        #print(scores)

        #idk where free_places on their site
        
        #idk where out_competition on their site
        out_competition = 0
        

        data[1].append({
            'fac_name': faculty_name,
            'url': "https://sibsutis.ru/abitur/konkursnye-spiski/bachelor/konkursnye-spiski/",
            'date_updated': str( datetime_to_utc( datetime.strptime(date_update, "Последнее обновление: %d.%m.%Y %H:%M:%S") ) ),
            'scores': scores[:free_places],
            'last_score': scores[free_places-1],
            'free_places': free_places,
            'olymp_cnt': out_competition,
            'prev_years17': None,
            'prev_years18': None,
            'prev_years19': None
        })

        disciplines = []
        disciplines_raw = list(direction_bs.find_all('th'))[4:]
        for discipline in disciplines_raw:
            disciplines.append(discipline.string)
        
        facults[faculty_name] = disciplines
        

    return data

abiturients = get_abit()

add_repeats_to_data()
# with open("disciplines.json", "w") as file:
#     file.write( json.dumps( facults) )

save_file(json.dumps(abiturients))
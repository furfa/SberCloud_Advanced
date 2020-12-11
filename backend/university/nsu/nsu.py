import requests
from bs4 import BeautifulSoup
from datetime import datetime

import sys, os
sys.path.append(os.path.join(sys.path[0], "../..") )

from tools.repeat_finder import find_repeats
from tools.functions import *
import json

scores_17_19 = {
    'Геолого-геофизический факультет Геология (05.03.01) общий конкурс': [213, 224, 206],
    'Гуманитарный институт Востоковедение и африканистика (58.03.01) общий конкурс': [271, 273, 273],
    'Гуманитарный институт Журналистика (42.03.02) общий конкурс': [None, None, 268],
    'Гуманитарный институт История (46.03.01) общий конкурс': [242, 254, 243],
    'Гуманитарный институт Лингвистика (45.03.02) общий конкурс': [274, 277, 277],
    'Гуманитарный институт Филология (45.03.01) общий конкурс': [253, 259, 269],
    'Гуманитарный институт Фундаментальная и прикладная лингвистика (45.03.03) общий конкурс': [266, 266, 266],
    'Институт медицины и психологии В. Зельмана НГУ Психология (37.03.01) общий конкурс': [238, 238, 249],
    'Институт медицины и психологии В. Зельмана НГУ Лечебное дело (31.05.01) общий конкурс': [None, None, None],
    'Институт философии и права Философия (47.03.01) общий конкурс': [232, 247, 248],
    'Институт философии и права ИФП. Юриспруденция (40.03.01) общий конкурс': [250, 250, 256],
    'Механико-математический факультет Математика (01.03.01) общий конкурс': [229, 238, 249],
    'Механико-математический факультет Математика и компьютерные науки (02.03.01) общий конкурс': [239, 241, 252],
    'Механико-математический факультет Механика и математическое моделирование (01.03.03) общий конкурс': [223, 242, 251],
    'Механико-математический факультет Прикладная математика и информатика (01.03.02) общий конкурс': [242, 242, 258],
    'Факультет естественных наук Биология (06.03.01) общий конкурс': [237, 246, 249],
    'Факультет естественных наук Химия (04.03.01) общий конкурс': [237, 246, 249],
    'Факультет естественных наук Фундаментальная и прикладная химия (04.05.01) общий конкурс': [237, 246, 249],
    'Факультет информационных технологий Информатика и вычислительная техника (09.03.01) общий конкурс': [253, 250, 261],
    'Физический факультет Физика (03.03.02) общий конкурс': [233, 243, 244],
    'Физический факультет Физическая информатика (03.03.02) общий конкурс': [None, None, 246],
    'Экономический факультет Бизнес-информатика (38.03.05) общий конкурс': [254, 251, 258],
    'Экономический факультет Менеджмент (38.03.02) общий конкурс': [248, 249, 256],
    'Экономический факультет Социология (39.03.01) общий конкурс': [233, 237, 248],
    'Экономический факультет Экономика (38.03.01) общий конкурс': [250, 250, 256],
    'Экономический факультет ЭФ. Юриспруденция (40.03.01) общий конкурс': [263, 268, 269]
}

facults = {}
faculties_abiturients = {}
abiturients = []

def add_repeats_to_data():
    repeats = find_repeats(faculties_abiturients)

    for faculty_index in range(len(abiturients[1])):
        if abiturients[1][faculty_index]['fac_name'] in repeats:
            abiturients[1][faculty_index]['n_severalfac'] = repeats[abiturients[1][faculty_index]['fac_name']]

def get_abit(dec_type, dec_condition):
    list_url = 'https://abiturient.nsu.ru/bachelor/list-content'
    auth_url = 'https://abiturient.nsu.ru/'
    directions_url = 'https://abiturient.nsu.ru/bachelor/list-direction'

    #data - json about all faculty and date when parser was runned
    data = [str(datetime.utcnow()), []]

    session = requests.Session()

    auth_html = session.get(auth_url)
    auth_bs = BeautifulSoup(auth_html.content, 'html.parser')
    csrf = auth_bs.select('meta[name=csrf-token]')[0]['content']

    for faculty in range(2, 11):
        directions_data = {
            '_csrf-frontend': csrf,
            'condition': str(dec_condition),
            'faculty': str(faculty)
        }
        directions_response = session.post(directions_url, data=directions_data)
        directions = directions_response.json()

        for direction_raw in directions:
            direction = direction_raw['value']
            
            list_data = {
                '_csrf-frontend': csrf,
                'type': str(dec_type),
                'condition': str(dec_condition),
                'faculty': str(faculty),
                'direction': str(direction)
            }

            list_response = session.post(list_url, data=list_data)
            try:
                list_response = list_response.json()[0]
            except:
                #response may not contain any json data
                print('oops, error in parsing some facult')
                data[1].append({
                    'fac_name': None,
                    'date_updated': None,
                    'scores': None,
                    'last_score': None,
                    'free_places': None,
                    'olymp_cnt': None,
                    'prev_years17': None,
                    'prev_years18': None,
                    'prev_years19': None
                })
                continue
                

            abits_raw = list_response['table']
            faculty_name = list_response['info']['faculty']['name'] + ' ' + direction_raw['label']

            abits = []

            abits_names = []

            out_competition = 0
            for abit in abits_raw:
                if abit['condition'] != 'Без вступительных испытаний':
                    abits.append(int(abit['sumPointTotal']))
                else:
                    out_competition += 1
                abits_names.append(abit['name'].split())

            
            abits.sort()
            abits = abits[::-1]
            free_places = list_response['info']['place']['total']['value'] - out_competition
            
            #works only if abits_raw sorted by scores
            #abits_raw sorted by scores if dec_type = 20
            abits_names = abits_names[:min(free_places, len(abits_names))]

            disciplines = []
            for discipline in list_response['table'][0]['disciplines']:
                disciplines.append(discipline['name'])

            facults[faculty_name] = disciplines

            data[1].append({
                'fac_name': faculty_name,
                'url': "https://abiturient.nsu.ru/bachelor",
                'date_updated': str( datetime_to_utc(
                     datetime.strptime(list_response['info']['date'], "Дата формирования - %d.%m.%Y. Время формирования - %H:%M:%S.")
                )),
                'scores': abits[:free_places],
                'last_score': abits[free_places-1],
                'free_places': free_places,
                'olymp_cnt': out_competition,
                'prev_years17': scores_17_19[faculty_name][0],
                'prev_years18': scores_17_19[faculty_name][1],
                'prev_years19': scores_17_19[faculty_name][2]
            })

            faculties_abiturients[faculty_name] = abits_names
    return data

#types:
#10 - подавшие заявление
#20 - участвующие в конкурсе
#30 - если бы зачисление состоялось сегодня

#conditions:
#10 - бюджет
#20 - особые права
#30 - платная
#40 - целевое

abiturients = get_abit(20, 10)

add_repeats_to_data()

#print(faculties_abiturients)


# with open("disciplines.json", "w") as file:
#     file.write( json.dumps( facults) )

save_file(json.dumps(abiturients))

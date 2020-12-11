import requests
from bs4 import BeautifulSoup
from datetime import datetime

import re
import sys, os
sys.path.append(os.path.join(sys.path[0], "..") )

import json
from tools.functions import save_file
from tqdm import tqdm
import json

import admlist_config

universities = admlist_config.universities

disciplines_dict = admlist_config.disciplines_dict

main_url = 'http://admlist.ru/{}/index.html'
main_faculty_url = 'http://admlist.ru/{}/{}'
url_2019 = 'http://admlist.ru/2019/{}/index.html'
faculty_url_2019 = 'http://admlist.ru/2019/{}/{}'



def get_faculty_num(faculty_name):
    return re.search(r'\(\d*.*\d', faculty_name).group(0)[1:]

faculties_2019 = {}
def get_2019_info(university):

    faculties_url = url_2019.format(university)
    faculties_html = requests.get(faculties_url)
    faculties_bs = BeautifulSoup(faculties_html.content, 'html.parser')
    
    faculties = list(faculties_bs.find_all('a'))[2:]

    faculties = list(map(lambda x: (x.string, x.attrs['href']), faculties))

    for faculty in faculties:
        faculty_url = faculty_url_2019.format(university, faculty[1])
        faculty_name = faculty[0]
        faculty_num = get_faculty_num(faculty_name)

        faculty_html = requests.get(faculty_url)
        faculty_bs = BeautifulSoup(faculty_html.content, 'html.parser')

        table = faculty_bs.find_all('table')[-1].find('tbody').find_all('tr')

        for abiturient in table:
            break
        
        break


def get_info(university):

    #data - json about all faculty and date when parser was runned
    data = [str(datetime.today()), []]

    faculties_url = main_url.format(university)
    faculties_html = requests.get(faculties_url)
    faculties_bs = BeautifulSoup(faculties_html.content, 'html.parser')

    faculties = list(faculties_bs.find_all('a'))[2:]

    faculties = list(map(lambda x: (x.string, x.attrs['href']), faculties))

    disciplines = []

    for faculty in tqdm(faculties):
        faculty_url = main_faculty_url.format(university, faculty[1])
        faculty_name = faculty[0]

        faculty_html = requests.get(faculty_url)
        faculty_bs = BeautifulSoup(faculty_html.content, 'html.parser')

        table = faculty_bs.find('table', {'class':'tableFixHead'})
        table_headers = list(map(lambda x: x.string, list(table.find('tr'))))
        table = list(table.find('tbody').find_all('tr'))

        scores = []
        scores_filtered = []

        for abiturient in table:
            abiturient_fields = list(abiturient.find_all('td'))
            abiturient_type = abiturient_fields[5].string
            
            if ('[Б' in abiturient_type) and (abiturient_type[0] =='О'):
                if len(list(abiturient.find_all('b'))) == 0:
                    scores_filtered.append(int(abiturient_fields[-2].string))
                scores.append(int(abiturient_fields[-2].string))
        
        info = list(list(faculty_bs.find_all('tr'))[1].find_all('td'))

        free_places = int(info[0].string)
        out_competition = int(info[-4].string.split('/')[0])

        free_places = max(0, free_places - out_competition)

        try:
            last_score = scores[free_places-1]
        except IndexError:
            last_score = 999

        try:
            last_score_filter = scores_filtered[free_places-1]
        except IndexError:
            last_score_filter = 999


        dictt = {faculty_name: list() }

        for x in table_headers[6:-4]:
            if x in disciplines_dict.keys():
                dictt[faculty_name].append(disciplines_dict[x])

        disciplines.append(dictt)

        data[1].append({
            'fac_name': faculty_name,
            'url': faculty_url,
            'date_updated': str(datetime.strptime(faculty_bs.find('h2').string.split('\n')[1], "%Y-%m-%d %H:%M")),
            'scores': scores,
            'scores_filter': scores_filtered,
            'last_score': last_score,
            'last_score_filter': last_score_filter,
            'free_places': free_places,
            'olymp_cnt': out_competition,
            'prev_years17': None,
            'prev_years18': None,
            'prev_years19': None
        })

    return data, disciplines


for university, info in universities.items():

    try:

        if university == "msu":
            continue

        folder_name = university+"(adm)"
        uni_dir = os.path.join(sys.path[0], folder_name)



        abiturients, disciplines = get_info(university)


        if not os.path.exists(uni_dir):
            os.mkdir(uni_dir)

        save_file(
            json_dump=json.dumps(abiturients, ensure_ascii=False),
            custom_path=uni_dir
        )



        with open( os.path.join(uni_dir, "info.json"), "w" ) as file:
            file.write(
                json.dumps(
                    info, 
                    ensure_ascii=False,
                    indent=4
                )
            )


        with open( os.path.join(uni_dir, "disciplines.json"), "w" ) as file:
            file.write(
                json.dumps(
                    info, 
                    ensure_ascii=False,
                    indent=4
                )
            )
    except:
        print(university, "non parsed")

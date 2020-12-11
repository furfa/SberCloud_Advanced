#! /usr/bin/python

import re
import json
from tqdm import tqdm
from tools.functions import modification_date, is_datafile
import os
from os import path
from os.path import join as join_dir

from datetime import datetime


def upload_state(text):
    # seconds_since_epoch = int(datetime.utcnow().timestamp())
    # filename = join_dir("site_states", f"{seconds_since_epoch}.json")
    filename = join_dir("site_states", f"last_state.json")
    with open(filename, "w") as file:
        file.write(text)

    color = '\x1b[47m' + '\x1b[31m'
    print(f"Saved -> {color}{filename}")


def from_iso_to_timestamp(s):
    try:
        return int(
            datetime.fromisoformat(s).timestamp() * 1000
        )
    except TypeError:
        return None


def parse_int(a):
    if(a == None):
        return 0
    else:
        return int(a)


def filter_points(ts):
    new_ts = list()
    for i in ts:
        if len(new_ts) == 0:
            new_ts.append(i)
            continue

        if i[1] > new_ts[-1][1]:
            new_ts.append(i)
    return new_ts


uniq_dis = ['Биология', 'Иностранный язык', 'Информатика и ИКТ', 'История',
            'Литература', 'Математика', 'Обществознание', 'Русский язык',
            'Творческий конкурс', 'Физика', 'Химия', 'География', "Физическая культура"]
# Bin encode
dis_powers = {i: 1 << power for power, i in enumerate(uniq_dis)}


def encode_disciplines(discipline_list):
    if discipline_list == None:
        return 2147483647

    res = 0
    for i in discipline_list:
        res += dis_powers[i]
    return res


uni_dir = "university"

TO_RENDER = list()  # [TO_RENDER_ITEM, ...]

TO_RENDER_ITEM = {
    "name": "",  # Имя вуза
    "link": "",  # Ссылка на страницу с факультетами
    "parse_date": "",
    "facs": {
        #       'fac_name' : { # Название фака
        #           'disciplines' : закодированные дисциплины,
        #           'url' : ссылка на страницу направления,
        #           'date_updated': "" Дата с сайта(если есть) или non если нет,
        #           'scores': [] Список баллов,
        #           'last_score': [
        #                           (Дата0, Балл0),
        #                           (Дата1, Балл1),
        #                           ...
        #                           ] Последний балл на бюджет,
        #           'free_places': 0 Количество мест,
        #           'olymp_cnt': 0 Количество бви,
        #           'prev_years': [0,0,0] [проходной за 17 год,  проходной за 18 год, проходной за 19 год],
        #       },
    },

}


allowed_uni = [
    'ifmo',
    'nsu',
    'nstu',
    'stu',
    'sibsutis',
    'spbu',
    'hse-nn(adm)',
    'hse-perm(adm)',
    'hse(adm)',
    'mospoly(adm)',
    'ranepa0(adm)',
    'gaugn(adm)',
    'mipt(adm)',
    'kpfu(adm)',
    # 'spbstu(adm)',
    # 'spbgeu(adm)',
    # 'mgimo(adm)',
    # 'bmstu(adm)',
    # 'mai(adm)',
    # 'guu(adm)',
    # 'msha(adm)',
    # 'mirea(adm)',
    # 'mpgu(adm)',
    # 'mei(adm)',
    # 'ranepa(adm)',
    # 'leti(adm)',
    # 'spbguap(adm)',
    # 'stankin(adm)',
    # 'samsu(adm)',
    # 'mgavm(adm)',
    # 'miet(adm)',
    # 'mtuci(adm)',
    # 'mephi(adm)',
    # 'fu(adm)',
    # 'ranepa1(adm)',
    # 'hse-spb(adm)',
    # 'miit(adm)',
    # 'herzenspb(adm)',
    # 'muctr(adm)',
    # 'rea(adm)',
    # 'misis(adm)',
    # 'vavt(adm)',
    # 'mgppu(adm)',
    # 'msu(adm)',
    # 'rggru(adm)',
    # 'rgung(adm)',
    # 'miigaik(adm)',
]

for uni in allowed_uni:  # os.listdir(uni_dir):

    print(uni)

    pth = join_dir(uni_dir, uni)
    if os.path.isdir(pth) and not uni.startswith(".") and uni != "tools":
        TO_RENDER_ITEM = {}

        info = json.loads(open(join_dir(pth, "info.json"), "r").read())
        print(info)
        TO_RENDER_ITEM = {**info}

        try:
            disciplines = json.loads(
                open(join_dir(pth, "disciplines.json"), "r").read())
            print("Файл дисциплин найден")
        except FileNotFoundError:
            print("Файл дисциплин не найден")
            disciplines = {}

        TO_RENDER_ITEM["facs"] = {}

        data_files = [join_dir(pth, file) for file in os.listdir(pth)
                      if is_datafile(file)
                      ]

        data_files.sort(key=lambda x: modification_date(x),
         reverse=True)  # Самый последний файл первым

        # columns = ['fac_name', 'date_updated', 'scores', 'last_score', 'free_places', 'olymp_cnt', 'prev_years17', 'prev_years18', 'prev_years19']
        for i, file in enumerate(data_files):
            # print(file)
            data = json.loads(open(file, "r").read())
            # init
            if i == 0:
                # print(data)
                TO_RENDER_ITEM["parse_date"] = from_iso_to_timestamp(data[0])

                for fac in data[1]:
                    TO_RENDER_ITEM["facs"][fac['fac_name']] = \
                        {
                            'url': fac.get("url"),
                            'disciplines': encode_disciplines(disciplines.get(fac['fac_name'])),
                            'date_updated': from_iso_to_timestamp(fac['date_updated']),
                            'scores': fac['scores'],
                            'last_score': [
                                (data[0], parse_int(fac['last_score'])),
                            ],
                            'free_places': fac['free_places'],
                            'olymp_cnt': fac['olymp_cnt'],
                            'prev_years': [
                                fac.get('prev_years17'),
                                fac.get('prev_years18'),
                                fac.get('prev_years19'),
                            ],
                            'n_severalfac': fac.get('n_severalfac'),
                    }
            else:
                for fac in data[1]:
                    try:
                        TO_RENDER_ITEM["facs"][fac['fac_name']]['last_score'].append(
                            (data[0], parse_int(fac['last_score']))
                        )

                        if i+1 == len(data_files):
                            # разворачиваем список последних баллов на поступление, чтобы дата была по возрастанию
                            TO_RENDER_ITEM["facs"][fac['fac_name']]['last_score'] = \
                                filter_points(
                                    TO_RENDER_ITEM["facs"][fac['fac_name']]['last_score'][::-1])
                    except KeyError:
                        print(fac['fac_name'], "раньше не существовал")

        TO_RENDER.append(TO_RENDER_ITEM)

print(len(TO_RENDER))

TO_RENDER = (dis_powers, TO_RENDER)

TO_RENDER_JSON = json.dumps(TO_RENDER)

upload_state(TO_RENDER_JSON)

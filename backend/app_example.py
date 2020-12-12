#!/home/furfa/.local/share/virtualenvs/sbercloud-hZFO6era

from flask import Flask, render_template, send_from_directory, url_for, request, jsonify
from flask_cachebuster import CacheBuster
from flask_sitemap import Sitemap
from flask_sqlalchemy import SQLAlchemy

from tools.functions import get_last_state

import os
import subprocess
import config
from pprint import pprint
from flask_cors import CORS

if config.RUN_PARSER:
    subprocess.Popen(["python", "heroku_parse_runner.py"])


app = Flask(__name__)
CORS(app)
ext = Sitemap(app=app)

cache_buster = CacheBuster(
    config={'extensions': ['.js', '.css', '.csv'], 'hash_size': 5})
cache_buster.init_app(app)

# Examples:
universities_example = [
    {
        "name":'nsu',
        "id":0
    },
    {
        "name":'ifmo',
        "id":1
    },
    {
        "name":'spbsu',
        "id":2
    },
    {
        "name":'nstu',
        "id":3
    } 
]
universities_cards_example = [
    (0,"NAME" ,'https://www.nsu.ru/n/', 'https://www.nsu.ru/local/templates/nsu_ru/images/NSU_Russian_logo_Red.svg'),
    (1,"NAME" ,'https://www.nsu.ru/n/', 'https://www.nsu.ru/local/templates/nsu_ru/images/NSU_Russian_logo_Red.svg'),
    (2,"NAME" ,'https://www.nsu.ru/n/', 'https://www.nsu.ru/local/templates/nsu_ru/images/NSU_Russian_logo_Red.svg'),
    (3,"NAME" ,'https://www.nsu.ru/n/', 'https://www.nsu.ru/local/templates/nsu_ru/images/NSU_Russian_logo_Red.svg')
]
universities_tables_example = [
    {
        'faculty_name': ('ФИТ', 'ММФ', 'ФИЯ'),
        'last_score': (270, 260, 275),
        'last_year_score': (268, 257, 270),
        'places': (150, 100, 80),
        'last_update': (None, None, None),
        'id': 0
    },
    {
        'faculty_name': ('ifmo-ФИТ', 'ifmo-ММФ', 'ifmo-ФИЯ'),
        'last_score': (270, 260, 275),
        'last_year_score': (268, 257, 270),
        'places': (150, 100, 80),
        'last_update': (None, None, None),
        'id': 1
    },
    {
        'faculty_name': ('spbsu-ФИТ', 'spbsu-ММФ', 'spbsu-ФИЯ'),
        'last_score': (270, 260, 275),
        'last_year_score': (268, 257, 270),
        'places': (150, 100, 80),
        'last_update': (None, None, None),
        'id': 2
    },
    {
        'faculty_name': ('nstu-ФИТ', 'nstu-ММФ', 'nstu-ФИЯ'),
        'last_score': (270, 260, 275),
        'last_year_score': (268, 257, 270),
        'places': (150, 100, 80),
        'last_update': (None, None, None),
        'id': 3
    }
]

@app.route("/get_list")
def get_universe_list():
    return jsonify(universities_example)

@app.route("/get_card")
def get_university_card():
    id = int(request.args.get('id', 0))
    try:
        card = universities_cards_example[id]
        return jsonify({
            "id" : card[0],
            "name" : card[1],
            "link" : card[2],
            "description" : "ФВЫфвфывфывфыв",
            "city": "СПБ",
        })
    except Exception:
        return jsonify(None)

@app.route("/get_table")
def get_university_table():
    id = int(request.args.get('id', 0))
    try:
        return jsonify(universities_tables_example[id])
    except Exception:
        return jsonify(None)
         

@app.route("/get_univer_item")
def add():
    number = int(request.args.get('number', 0))
    print(number)
    raw_data = get_last_state_update()
    data = raw_data[1]

    if number >= len(data):
        return "END"
    if number < 0:
        return page_not_found(None)
    return render_template("univer_item.html", univer = data[number])


if __name__ == "__main__":
    # app.run(host="192.168.105.22", port="8001", debug=True)
    # app.run(host="0.0.0.0", port="8001", debug=True)
    app.run(port="8001", debug=True)
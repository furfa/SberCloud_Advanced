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

if config.RUN_PARSER:
    subprocess.Popen(["python", "heroku_parse_runner.py"])


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Igor:1122@localhost:5432/egengine'
db = SQLAlchemy(app)
ext = Sitemap(app=app)

cache_buster = CacheBuster(
    config={'extensions': ['.js', '.css', '.csv'], 'hash_size': 5})
cache_buster.init_app(app)


# class University(db.Model):
#     __tablename__ = 'universities'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     url = db.Column(db.String())
#     img_url = db.Column(db.String())

#     def __init__(self, name, url, img_url):
#         self.name = name
#         self.url = url
#         self.img_url = img_url

#     def __repr__(self):
#         return f"<University {self.name}>



@ext.register_generator
def indexx():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
    yield 'index', {}

@app.template_filter()
def checkseveralfac(d):
    # print(list(d.values()))
    try:
        return list(d.values())[0]["n_severalfac"] != None
    except:
        return False

def get_last_state_update():
    raw_data = get_last_state()
    if config.YADISK_DOWNLOAD_STATE:
        subprocess.Popen(["python", "yadisk_sync.py", "--download_state"])
    return raw_data

@app.route('/index.html')
@app.route('/')
def index():

    raw_data = get_last_state_update()

    data = raw_data[1]
    disciplines = raw_data[0]
    # return jsonify(data)
    return render_template("index.html", data=data, disciplines=disciplines)

def get_universe_list(score):
    print('get_universe_list')

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
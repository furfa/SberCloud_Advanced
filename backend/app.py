#!/home/furfa/.local/share/virtualenvs/sbercloud-hZFO6era

from flask import Flask, render_template, send_from_directory, url_for, request, jsonify
from flask_cachebuster import CacheBuster
from flask_sitemap import Sitemap

from tools.functions import get_last_state

import os
import subprocess
import config
from pprint import pprint

if config.RUN_PARSER:
    subprocess.Popen(["python", "heroku_parse_runner.py"])


app = Flask(__name__)

ext = Sitemap(app=app)


@ext.register_generator
def indexx():
    # Not needed if you set SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS=True
    yield 'index', {}


cache_buster = CacheBuster(
    config={'extensions': ['.js', '.css', '.csv'], 'hash_size': 5})
cache_buster.init_app(app)


@app.template_filter()
def checkseveralfac(d):
    # print(list(d.values()))
    try:
        return list(d.values())[0]["n_severalfac"] != None
    except:
        return False


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/robots.txt')
def robotstxt():
    return send_from_directory(app.static_folder, "robots.txt")

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



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    # app.run(host="192.168.105.22", port="8001", debug=True)
    # app.run(host="0.0.0.0", port="8001", debug=True)
    app.run(port="8001", debug=True)
import os
from flask import json
from datetime import datetime
import sys
import re

def is_datafile(file_name):
    return re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}=\d{2}=\d{2}.*.json", file_name)

def datetime_to_utc(date):
    gmt = datetime.now() - datetime.utcnow()
    return date - gmt

def modification_date(raw_filename):
    filename = os.path.basename(raw_filename)
    if is_datafile(filename):
        filename = filename.replace("=", ":")
        return datetime.fromisoformat(filename[:-5])

    return os.path.getmtime(raw_filename)


def get_last_state():
    
    folder = "site_states"

    states = [os.path.join(folder,state) for state in os.listdir( folder )]

    last_state = max(states, key=lambda x:modification_date(x))
    print("loading last_state:", last_state)

    return json.loads( open(last_state, "r").read() )

def prep_filename(s):
    return s.replace(":", "=")

def save_file(json_dump, custom_path=""):
    # Сохраняет в дирректорию исполняемого файла
    date = prep_filename( 
        str( datetime.utcnow() )
    )
    if custom_path == "":
        file_name = os.path.join(sys.path[0], f"{date}.json")
    else:
        file_name = os.path.join(custom_path, f"{date}.json")

    with open(file_name, "w") as file:
        file.write(json_dump)
    
    print("Saved to "+file_name)
    return file_name

if __name__ == "__main__":
    print("HELLO")
from flask import json
import numpy as np
import os, sys
import re
from datetime import datetime
from tqdm import tqdm
import yadisk

PROJ_LOCAL_ROOT = sys.path[0]
DISK_ROOT = "/egengine"
UNI_FOLDER = "university"

ya_disk_token = os.getenv("EGENGINE_YADISK")

y = yadisk.YaDisk(token=ya_disk_token)

def prep_filename_from(s):
    return s.replace("=", ":")


def create_folder_if_not_exists(pth):
    if not y.exists(pth):
        y.mkdir(pth)
        print(f"{pth} folder upload")
        
def upload_file_if_not_exists(loc_pth, disk_pth):
    
    if not y.exists(disk_pth):
        y.upload(loc_pth, disk_pth)
        print(f"{disk_pth} file upload")

def download_file_if_not_exists(disk_pth, loc_pth):
    
    if not os.path.isfile(loc_pth):
        y.download(disk_pth, loc_pth)
        print(f"{disk_pth} file download")

def create_main_folder():
    create_folder_if_not_exists(DISK_ROOT)
    print("DISK ROOT CREATED")

def init_univer_folders():
    uni_folders = os.listdir(UNI_FOLDER)
    
    for folder in uni_folders:
        path = os.path.join(DISK_ROOT, folder)
        
        create_folder_if_not_exists(path)
        
def upload_univer_parses():
    init_univer_folders()
    uni_folders = os.listdir(UNI_FOLDER)
    
    for folder in uni_folders:
        data_files = [file for file in os.listdir( os.path.join(UNI_FOLDER, folder) ) 
            if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}=\d{2}=\d{2}.*.json", file)
        ]
        
        for file in tqdm(data_files):
            
            #print(f"{lp=} \n{dp=}")
            
            upload_file_if_not_exists(
                loc_pth = os.path.join(PROJ_LOCAL_ROOT, UNI_FOLDER, folder, file),
                disk_pth = os.path.join(DISK_ROOT, folder, file)
            )

def download_univer_parses():
    uni_folders = os.listdir(UNI_FOLDER)
    
    for folder_pth in uni_folders:
        data_files = [os.path.basename(i["path"]) for i in y.listdir( os.path.join(DISK_ROOT, folder_pth) )]
        
        for file in tqdm(data_files):
            
            download_file_if_not_exists(
                loc_pth = os.path.join(PROJ_LOCAL_ROOT, UNI_FOLDER, folder_pth, file),
                disk_pth = os.path.join(DISK_ROOT, folder_pth, file)
            )

def upload_last_state():
    y.remove("/egengine/last_state.json")
    upload_file_if_not_exists("site_states/last_state.json", "/egengine/last_state.json")

def download_last_state():
    if y.exists("/egengine/last_state.json"):
        os.remove("site_states/last_state.json")
        download_file_if_not_exists("/egengine/last_state.json", "site_states/last_state.json")
        print("STATATE DOWNLOADED")
            
def sync_univer_parses():
    upload_univer_parses()
    download_univer_parses()
    print("sync complete!!!")


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Ya disk sync script')
    parser.add_argument('--logging', dest='logging', action='store_true')
    parser.set_defaults(logging=False)
    parser.add_argument('--sync_uni', dest='sync_uni', action='store_true')
    parser.set_defaults(sync_uni=False)
    parser.add_argument('--upload_state', dest='upload_state', action='store_true')
    parser.set_defaults(upload_state=False)
    parser.add_argument('--download_state', dest='download_state', action='store_true')
    parser.set_defaults(download_state=False)
    args = parser.parse_args()

    if not args.logging:
        def nop(it, *a, **k):
            return it
        tqdm = nop
    if args.sync_uni:
        sync_univer_parses()

    if args.upload_state:
        upload_last_state()

    if args.download_state:
        download_last_state()
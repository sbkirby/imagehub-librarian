#!/usr/bin/env python3
""" USAGE
 purge_folders.py is run by crontab once a day to purge a list of image folders and their contents.
 This module uses the purge_folders entry in the config.json file for the file name containing the
 list of folders to purge.

 Copyright (c) 2021 by Stephen B. Kirby.
 License: MIT, see LICENSE for more details.
"""

import time
import json
import os
import shutil


# read data from config file. json only
def load_config():
    # define Working Directory
    wrk_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(wrk_dir, 'config.json')) as json_data_file:
        return json.load(json_data_file)


# Read config.json file for settings
data = load_config()
# JSON data file location and name
purge_folders = os.path.join(data["imagehub_data"], data["purge_folders"])

# check to see if the Modified Time of file is greater than last_read variable
if os.path.isfile(purge_folders):
    # read file
    with open(purge_folders, 'r') as myfile:
        data = myfile.read()
    # JSON parse file
    try:
        obj = json.loads(data)
    except:
        print('JSON Error: reading ', purge_folders)
    # loop thru entries in file
    for num, folders in enumerate(obj):
        folder = folders['folder']
        try:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        time.sleep(1)

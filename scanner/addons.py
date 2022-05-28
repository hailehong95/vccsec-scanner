#!/usr/bin/env python

import os
import csv
import time
import logging
import platform
import traceback
import subprocess

from scanner.setting import DATA_DIR, BIN_DIR, BROWSERADDONSVIEW_BIN
from scanner.crypto import secure_string_random
from scanner.utils import write_dicts_to_json_file


def addon_csv_to_dicts(csv_file):
    try:
        data = list()
        reader = csv.DictReader(open(csv_file))
        reader.fieldnames = [x.replace(' ', '_').lower() for x in reader.fieldnames]
        for row in reader:
            data.append(row)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


def addon_scan_on_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        browseraddonsview_bin = os.path.join(BIN_DIR, BROWSERADDONSVIEW_BIN)
        csv_file = os.path.join(DATA_DIR, '.'.join([secure_string_random(6), 'tmp']))
        browseraddonsview_cmd = [browseraddonsview_bin, '/scomma', csv_file]
        browseraddonsview_output = subprocess.run(browseraddonsview_cmd, stdout=subprocess.PIPE)
        time.sleep(1)
    except Exception as e:
        logging.error(traceback.format_exc())
    return csv_file


def get_addon_windows():
    try:
        data = list()
        addon_csv = addon_scan_on_windows()
        if os.path.exists(addon_csv):
            data = addon_csv_to_dicts(addon_csv)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


# Get Browser add-on on system
def addons_task():
    addon_data = list()
    os_platform = platform.system()
    if os_platform == 'Windows':
        addon_data = get_addon_windows()
    elif os_platform == 'Linux':
        pass
    elif os_platform == 'Darwin':
        pass
    else:
        return addon_data.append("Operating system is not detected.")
    write_dicts_to_json_file(addon_data, 'addon.json')
    return len(addon_data)

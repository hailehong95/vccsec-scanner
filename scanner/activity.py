#!/usr/bin/env python

import os
import csv
import time
import logging
import platform
import traceback
import subprocess

from scanner.setting import DATA_DIR, BIN_DIR, LASTACTIVITYVIEW_BIN
from scanner.crypto import secure_string_random
from scanner.utils import write_dicts_to_json_file


def activity_csv_to_dicts(csv_file):
    try:
        data = list()
        reader = csv.DictReader(open(csv_file))
        reader.fieldnames = [x.replace(' ', '_').lower() for x in reader.fieldnames]
        for row in reader:
            data.append(row)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


def activity_scan_on_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        lastactivityview_bin = os.path.join(BIN_DIR, LASTACTIVITYVIEW_BIN)
        csv_file = os.path.join(DATA_DIR, '.'.join([secure_string_random(6), 'tmp']))
        lastactivityview_cmd = [lastactivityview_bin, '/scomma', csv_file]
        lastactivityview_output = subprocess.run(lastactivityview_cmd, stdout=subprocess.PIPE)
        time.sleep(1)
    except Exception as e:
        logging.error(traceback.format_exc())
    return csv_file


def get_activity_windows():
    try:
        data = list()
        activity_csv = activity_scan_on_windows()
        if os.path.exists(activity_csv):
            data = activity_csv_to_dicts(activity_csv)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


# Last Activity on system (Windows)
def activity_task():
    activity_data = list()
    os_platform = platform.system()
    if os_platform == 'Windows':
        activity_data = get_activity_windows()
    elif os_platform == 'Linux':
        pass
    elif os_platform == 'Darwin':
        pass
    else:
        return activity_data.append("Operating system is not detected.")
    write_dicts_to_json_file(activity_data, 'activity.json')
    return len(activity_data)

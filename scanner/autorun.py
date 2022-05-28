#!/usr/bin/env python

import os
import csv
import time
import logging
import platform
import traceback
import subprocess

from scanner.setting import BIN_DIR, DATA_DIR, AUTORUN_BIN
from scanner.crypto import secure_string_random
from scanner.utils import write_dicts_to_json_file


# Ref: https://stackoverflow.com/a/38370569
def autorun_csv_to_dicts(csv_file):
    try:
        data = list()
        reader = csv.DictReader(open(csv_file))
        reader.fieldnames = [x.replace(' ', '_').replace('-', '').lower() for x in reader.fieldnames]
        for row in reader:
            if row['imp'] != '' and row['imp'] is not None:
                data.append(row)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


# Scanning autoruns key on windows
def autorun_scan_on_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        autorun_bin = os.path.join(BIN_DIR, AUTORUN_BIN)
        autorun_csv = os.path.join(DATA_DIR, '.'.join([secure_string_random(6), 'tmp']))
        autorun_cmd = [autorun_bin, '-accepteula', '-nobanner', '-a', '*', '-c', '-h', '-s', '-m', '-o', autorun_csv]
        autorun_output = subprocess.run(autorun_cmd, stdout=subprocess.PIPE)
        time.sleep(1)
    except Exception as e:
        autorun_csv = ''
        logging.error(traceback.format_exc())
    return autorun_csv


# Autoruns keys on Windows
def get_autorun_windows():
    try:
        data = list()
        autorun_csv = autorun_scan_on_windows()
        if os.path.exists(autorun_csv):
            data = autorun_csv_to_dicts(autorun_csv)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


# Get Autoruns key: bootstart, persistent, autostart program
def autorun_task():
    autorun_data = list()
    os_platform = platform.system()
    if os_platform == 'Windows':
        autorun_data = get_autorun_windows()
    elif os_platform == 'Linux':
        pass
    elif os_platform == 'Darwin':
        pass
    else:
        return autorun_data.append("Operating system is not detected.")
    write_dicts_to_json_file(autorun_data, 'autorun.json')
    return len(autorun_data)


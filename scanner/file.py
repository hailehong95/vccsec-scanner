#!/usr/bin/env python

import os
import csv
import time
import logging
import platform
import traceback
import subprocess

from scanner.setting import BIN_DIR, DATA_DIR, SIGCHECK_BIN, MAX_SIZE_FILE
from scanner.crypto import secure_string_random
from scanner.utils import write_dicts_to_json_file


def sigcheck_csv_to_dicts(csv_file):
    try:
        data = list()
        reader = csv.DictReader(open(csv_file, encoding='utf-16'))
        reader.fieldnames = [x.replace(' ', '_').lower() for x in reader.fieldnames]
        for row in reader:
            data.append(row)
    except Exception as error:
        pass
    return data


# Sigcheck Recurse subdirectories
# Return list of csv report file name
def sigcheck_scan_on_windows():
    user_dirs = ['Public', 'AppData', 'Temp', 'ProgramData']
    system_dirs = ['Temp', 'Debug']
    
    try:
        target_dir = list()
        sigcheck_csv = list()
        sigcheck_bin = os.path.join(BIN_DIR, SIGCHECK_BIN)
        for dir in user_dirs:
            target_dir.append(os.getenv(dir))
        for dir in system_dirs:
            target_dir.append(os.path.join(os.getenv('windir'), dir))
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        for dir in target_dir:
            csv_file = os.path.join(DATA_DIR, '.'.join([secure_string_random(6), 'tmp']))
            sigcheck_cmd = [sigcheck_bin, '-accepteula', '-nobanner', '-a', '-c', '-e', '-h', '-w', csv_file, '-s', dir]
            sigcheck_output = subprocess.run(sigcheck_cmd, stdout=subprocess.PIPE)
            sigcheck_csv.append(csv_file)
            time.sleep(1)
    except Exception as e:
        logging.error(traceback.format_exc())
    return sigcheck_csv


def get_sigcheck_windows():
    try:
        sigcheck_data = list()
        sigcheck_csv = sigcheck_scan_on_windows()
        for csv_ in sigcheck_csv:
            if os.path.exists(csv_):
                tmp = sigcheck_csv_to_dicts(csv_)
                sigcheck_data = sigcheck_data + tmp
    except Exception as e:
        logging.error(traceback.format_exc())
    return sigcheck_data


# Check files in some location of malware
def files_task():
    files_data = list()
    os_platform = platform.system()
    if os_platform == 'Windows':
        files_data = get_sigcheck_windows()
    elif os_platform == 'Linux':
        pass
    elif os_platform == 'Darwin':
        pass
    else:
        return files_data.append("Operating system is not detected.")
    write_dicts_to_json_file(files_data, 'files.json')
    return len(files_data)

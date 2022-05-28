#!/usr/bin/env python

import os
import psutil
import logging
import platform
import traceback

from scanner.setting import DATA_DIR
from scanner.utils import pe_signature_check, get_hash_file
from scanner.utils import write_dicts_to_json_file


# Process running on Windows, Linux, macOS
def get_process_running():
    try:
        data = list()
        os_platform = platform.system()
        attrs = ['pid', 'name', 'status', 'create_time', 'username', 'exe', 'cmdline']
        procs = psutil.process_iter(attrs, ad_value=None)
        for x in procs:
            if x.info['exe'] and os.path.exists(x.info['exe']):
                x.info['hash'] = get_hash_file(x.info['exe'])
                if os_platform == 'Windows':
                    x.info['verified'] = pe_signature_check(x.info['exe'])
            else:
                x.info['hash'] = None
                x.info['verified'] = None

            data.append(x.info)
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


# Get Process running on system
def process_task():
    process_data = list()
    if platform.system() in ['Windows', 'Linux', 'Darwin']:
        process_data = get_process_running()
    else:
        process_data.append("Operating system is not detected.")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    write_dicts_to_json_file(process_data, 'process.json')
    return len(process_data)

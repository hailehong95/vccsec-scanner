#!/usr/bin/env python

from utils.setting import BIN_DIR, KEY_DIR, DATA_DIR, EXE_LAUNCHER_NAME
from utils.setting import RELEASE_DIR, BUILD_DIR, BASE_DIR

import os
import time
import shutil
import logging
import traceback


# Clean Task: Remove all binaries dependencies in 'bin' directory.
def clean_task():
    try:
        print("[TASK] Clean temporary working files.")
        py_cache_dir = os.path.join(BASE_DIR, "__pycache__")
        dirs_delete = [BIN_DIR, KEY_DIR, DATA_DIR, RELEASE_DIR, BUILD_DIR, py_cache_dir]
        files_delete = [os.path.join(BASE_DIR, EXE_LAUNCHER_NAME + ".spec")]
        for dir_ in dirs_delete:
            if os.path.isdir(dir_):
                shutil.rmtree(dir_, ignore_errors=True)
                time.sleep(1)
        for file_ in files_delete:
            if os.path.isfile(file_):
                os.remove(file_)
                time.sleep(1)
        print("[+] Clean done!\n")
    except Exception as e:
        logging.error(traceback.format_exc())

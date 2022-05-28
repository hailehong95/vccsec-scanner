#!/usr/bin/env python

from utils.setting import BIN_DIR, PACKAGE_DIR
from utils.setting import SYS_INTERNAL_EXE, NIR_SOFT_ZIP
from utils.utils import unzip_file

import os
import time
import shutil
import logging
import platform
import traceback

# Extract Task: unzip and copy binaries dependencies to 'bin' directory.
def extract_task():
    try:
        print("[TASK] Extracting VCCSEC Scanner.")
        if not os.path.isdir(BIN_DIR):
            os.mkdir(BIN_DIR)
        os_platform = platform.system().lower()
        if os_platform == "windows":
            print("[+] Platform is: {}".format("Windows"))
            print("[+] Copy SysInternal file: {}".format(SYS_INTERNAL_EXE))
            for _exe in SYS_INTERNAL_EXE:
                shutil.copyfile(os.path.join(PACKAGE_DIR, _exe), os.path.join(BIN_DIR, _exe))
                time.sleep(0.5)
            print("[+] Extract Zip and copy Nirsoft file: {}".format(NIR_SOFT_ZIP))
            for _zip in NIR_SOFT_ZIP:
                unzip_file(os.path.join(PACKAGE_DIR, _zip), BIN_DIR)
                time.sleep(0.5)
            extensions = {".txt", ".chm"}
            files = os.listdir(BIN_DIR)
            files_removed = list()
            for file_ in files:
                for ext in extensions:
                    if file_.endswith(ext):
                        files_removed.append(file_)
                        os.remove(os.path.join(BIN_DIR, file_))
                        time.sleep(0.5)
            print("[+] Removed {} optional files: {}".format(len(files_removed), files_removed))
            print("[+] Extract done!\n")
    except Exception as e:
        logging.error(traceback.format_exc())

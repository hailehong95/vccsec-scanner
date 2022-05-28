#!/usr/bin/env python

from utils.setting import PACKAGE_DIR
from utils.setting import SYS_INTERNAL_EXE, NIR_SOFT_ZIP
from utils.setting import SYS_INTERNAL_URL, NIR_SOFT_URL

from utils.utils import download_file_from_url

import os
import time
import logging
import platform
import traceback


# Update Task: Download latest version of binaries dependencies from SysInternal Suite and Nirsoft Packages.
def update_task():
    try:
        print("[TASK] Updating binaries dependencies.")
        if not os.path.exists(PACKAGE_DIR):
            os.mkdir(PACKAGE_DIR)
        os_platform = platform.system().lower()
        if os_platform == "windows":
            print("[+] Platform is: Windows")
            packs = os.listdir(PACKAGE_DIR)
            if '.gitignore' in packs:
                packs.remove('.gitignore')
            missing_file = list()
            TOTAL_FILE = SYS_INTERNAL_EXE + NIR_SOFT_ZIP
            for bin_ in TOTAL_FILE:
                if bin_ not in packs:
                    missing_file.append(bin_)
            if len(missing_file) > 0:
                print("[+] Missing {} file: {}".format(len(missing_file), missing_file))
            file_downloaded = list()
            print("[+] Downloading binaries dependencies.")
            for file_ in missing_file:
                if file_ in SYS_INTERNAL_EXE:
                    url = SYS_INTERNAL_URL + file_
                    file_downloaded.append(download_file_from_url(url, PACKAGE_DIR))
                elif file_ in NIR_SOFT_ZIP:
                    url = NIR_SOFT_URL + file_
                    file_downloaded.append(download_file_from_url(url, PACKAGE_DIR))
            if len(file_downloaded) > 0:
                print("[+] Total {} file download: {}".format(len(file_downloaded), file_downloaded))
            print("[+] Update done.\n")
        time.sleep(0.5)
    except Exception as e:
        logging.error(traceback.format_exc())

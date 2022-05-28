#!/usr/bin/env python

from utils.crypto import secure_string_random
from utils.setting import PY_LAUNCHER_NAME, EXE_LAUNCHER_NAME
from utils.setting import RELEASE_DIR, PACKER_DIR, BASE_DIR

import os
import time
import logging
import platform
import traceback
import PyInstaller.__main__


def build_task():
    try:
        print("[TASK] Build VCCSEC Scanner.")
        os_platform = platform.system().lower()
        tiny_aes_key = secure_string_random(16)
        release_path = os.path.join(RELEASE_DIR, os_platform)
        icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
        if os_platform == 'windows':
            upx_packer = os.path.join(PACKER_DIR, 'upx_win64')
            PyInstaller.__main__.run(['--clean', '--uac-admin', '--icon', icon_path, '--onefile', '--name', EXE_LAUNCHER_NAME, '--add-data', 'bin;bin', '--add-data', 'key;key',
                                     '--distpath', release_path, '--upx-dir', upx_packer, '--key', tiny_aes_key, PY_LAUNCHER_NAME])
        elif os_platform == 'linux':
            pass
        elif os_platform == 'macosx':
            pass
        else:
            print("[-] Platform does not support!\n")
        time.sleep(0.5)
    except Exception as e:
        logging.error(traceback.format_exc())

#!/usr/bin/env python

from utils.setting import BASE_DIR, KEY_DIR, RSA_KEY_DIR
from utils.setting import RSA_PRI_KEY, RSA_PUB_KEY
from utils.crypto import generate_rsa_keys

import os
import time
import shutil
import logging
import traceback


# Keygen Task: Generate public/private key pair and save to rsa_keys dir
def keygen_task():
    try:
        if not os.path.isdir(RSA_KEY_DIR):
            os.mkdir(RSA_KEY_DIR)
        print("[TASK] Generating RSA Key pair.")
        generate_rsa_keys()
        rsa_keys = os.listdir(RSA_KEY_DIR)
        if '.gitignore' in rsa_keys:
            rsa_keys.remove('.gitignore')
        print("[+] Generate done. Total keys: {}\n".format(rsa_keys))
        time.sleep(0.5)
    except Exception as e:
        logging.error(traceback.format_exc())


# RSA Key Task: Adding rsa encryption key to bin dir
def rsa_key_task():
    try:
        if not os.path.isdir(RSA_KEY_DIR):
            os.mkdir(RSA_KEY_DIR)
        rsa_keys = os.listdir(RSA_KEY_DIR)
        if RSA_PRI_KEY not in rsa_keys or RSA_PUB_KEY not in rsa_keys:
            keygen_task()
        print("[TASK] Copy encryption key.")
        if not os.path.isdir(KEY_DIR):
            os.mkdir(KEY_DIR)
        src_file = os.path.join(RSA_KEY_DIR, RSA_PUB_KEY)
        dst_file = os.path.join(KEY_DIR, RSA_PUB_KEY)
        shutil.copyfile(src_file, dst_file)
        time.sleep(1)
        if os.path.exists(os.path.join(KEY_DIR, RSA_PUB_KEY)):
            print("[+] Copy done!\n")
        else:
            print("[-] Failed to copy key!\n")
    except Exception as e:
        logging.error(traceback.format_exc())

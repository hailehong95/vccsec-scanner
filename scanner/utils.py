#!/usr/bin/env python

import os
import json
import socket
import ctypes
import urllib
import hashlib
import logging
import zipfile
import binascii
import platform
import requests
import traceback
import subprocess

from datetime import datetime
from scanner.crypto import secure_string_random
from scanner.setting import BIN_DIR, SIGCHECK_BIN, DATA_DIR, MAX_SIZE_FILE, CWD_DIR, BASE_DIR


# Ref: https://stackoverflow.com/a/1026626
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


# Ref: https://stackoverflow.com/a/28950776
def get_primary_ip_without_internet(host='10.255.255.255', port=1):
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sk.connect((host, port))
        primary_ip = sk.getsockname()[0]
    except Exception:
        primary_ip = '127.0.0.1'
    finally:
        sk.close()
    return primary_ip


# Ref: https://stackoverflow.com/a/28950776
def get_primary_ip_with_internet(host='www.google.com', port=80, timeout=5):
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sk.settimeout(timeout)
        sk.connect((socket.gethostbyname(host), port))
        primary_ip = sk.getsockname()[0]
    except:
        primary_ip = '127.0.0.1'
    finally:
        sk.close()
    return primary_ip


# Ref: https://stackoverflow.com/a/50558001
def internet_check_by_urllib(url='http://www.google.com/', timeout=5):
    try:
        _ = urllib.request.urlopen(url, timeout=timeout)
        return True
    except:
        pass
    return False


# Ref: https://stackoverflow.com/a/24460981
def internet_check_by_requests(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        pass
    return False


# Ref: https://stackoverflow.com/a/33117579, https://gist.github.com/7h3rAm/a4c3de8e502f755a7253
def internet_check_by_socket(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        pass
    return False


# Check Signature of PE File
def pe_signature_check(pe_file):
    try:
        data = dict()
        sigcheck_bin = os.path.join(BIN_DIR, SIGCHECK_BIN)
        sigcheck_cmd = [sigcheck_bin, '-accepteula', '-nobanner', pe_file]
        sigcheck_output = subprocess.run(sigcheck_cmd, stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore').replace('\t', '').splitlines()
        data['verified'] = sigcheck_output[1].split(':')[-1]
        data['signing_date'] = sigcheck_output[2].split('ate:')[-1]
        data['publisher'] = sigcheck_output[3].split(':')[-1]
        data['machine_type'] = sigcheck_output[9].split(':')[-1]
    except Exception as e:
        logging.error(traceback.format_exc())
    return data


# Ref: https://stackoverflow.com/a/3431838
def get_hash_file(file):
    try:
        hash = dict()
        hash_md5 = hashlib.md5()
        hash_sha1 = hashlib.sha1()
        hash_sha256 = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)
        hash['md5'] = hash_md5.hexdigest()
        hash['sha1'] = hash_sha1.hexdigest()
        hash['sha256'] = hash_sha256.hexdigest()
    except Exception as e:
        logging.error(traceback.format_exc())
    return hash


def is_valid_file(file):
    if os.path.getsize(file) > MAX_SIZE_FILE:
        return False
    extension = ['.exe', '.dll', '.sys', '.drv', '.ocx', '.cpl', '.scr', '.com']
    for ext in extension:
        if file.endswith(ext):
            return True
    try:
        pe_header = b''
        with open(file, 'rb') as fs:
            pe_header = binascii.hexlify(fs.read()[:4])
        if b'4d5a' in pe_header:
            return True
    except:
        pass
    return False


# Ref: https://pythonexamples.org/python-get-list-of-all-files-in-directory-and-sub-directories/
def get_file_recursively(path):
    list_file = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            list_file.append(os.path.join(root,file))
    return list_file


# Ref: https://www.geeksforgeeks.org/python-difference-between-json-dump-and-json-dumps/
def write_dicts_to_json_file(dict_data, file_name):
    try:
        with open(os.path.join(DATA_DIR, file_name), 'w') as fout:
            json.dump(dict_data, fout)
    except Exception as e:
        logging.error(traceback.format_exc())


# Ref: https://stackoverflow.com/a/1855118
def zip_list_file():
    try:
        json_file = list()
        if os.path.exists(DATA_DIR):
            for x in os.listdir(DATA_DIR):
                if x.endswith('.json'):
                    json_file.append(x)
        # tmp_name = '-'.join([platform.node(), secure_string_random(6) + '.zip'])
        tmp_name = '-'.join([platform.system().lower(), platform.node().lower(), datetime.now().strftime('%Y%m%d%H%M%S') + '.zip'])
        zip_name = os.path.join(CWD_DIR, tmp_name)
        os.chdir(DATA_DIR)
        with zipfile.ZipFile(zip_name, 'w') as zipObj:
            for file_ in json_file:
                zipObj.write(file_)
    except Exception as e:
        logging.error(traceback.format_exc())
    finally:
        os.chdir(BASE_DIR)
    return zip_name


# Send report file to server
def send_report_task():
    pass

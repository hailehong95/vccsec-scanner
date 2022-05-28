#!/usr/bin/env python

import os
import shutil
import zipfile
import logging
import platform
import requests
import traceback


# Ref: https://stackoverflow.com/a/39217788, https://gist.github.com/mvpotter/9088499
def download_file_from_url(url, dst_dir):
    try:
        local_filename = os.path.join(dst_dir, url.split('/')[-1])
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        return os.path.basename(local_filename)
    except Exception as e:
        logging.error(traceback.format_exc())


# Ref: https://stackoverflow.com/a/3451150
def unzip_file(zip_file, dst_dir):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dst_dir)
    except Exception as e:
        logging.error(traceback.format_exc())

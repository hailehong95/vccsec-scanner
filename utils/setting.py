#!/usr/bin/env python

import os

# Setting Working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(BASE_DIR, 'bin')
KEY_DIR = os.path.join(BASE_DIR, 'key')
DATA_DIR = os.path.join(BASE_DIR, 'data')
BUILD_DIR = os.path.join(BASE_DIR, 'build')
PACKER_DIR = os.path.join(BASE_DIR, 'packer')
RSA_KEY_DIR = os.path.join(BASE_DIR, 'rsa_keys')
PACKAGE_DIR = os.path.join(BASE_DIR, 'packages')
RELEASE_DIR = os.path.join(BASE_DIR, 'releases')


SYS_INTERNAL_URL = "https://live.sysinternals.com/"
NIR_SOFT_URL = "https://www.nirsoft.net/utils/"
SYS_INTERNAL_EXE = ["autorunsc.exe", "sigcheck.exe"]
NIR_SOFT_ZIP = ["browseraddonsview.zip", "cports.zip", "lastactivityview.zip"]
RSA_PUB_KEY = 'key.pub'
RSA_PRI_KEY = 'key.pri'
PY_LAUNCHER_NAME = 'vccsec-scanner.py'
EXE_LAUNCHER_NAME = 'vccsec-scanner'

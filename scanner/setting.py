#!/usr/bin/env python

import os

# Working directory
TEMP = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(TEMP)
DATA_DIR = os.path.join(BASE_DIR, 'data')
BIN_DIR = os.path.join(BASE_DIR, 'bin')
KEY_DIR = os.path.join(BASE_DIR, 'key')
TEST_DIR = os.path.join(BASE_DIR, 'tests')
CWD_DIR = os.getcwd()
# Please change Base url (s3)
BASE_URL = 'https://your-base-url'

# SysInternal Binary
AUTORUN_BIN = 'autorunsc.exe'
SIGCHECK_BIN = 'sigcheck.exe'

# NirSoft Binary
BROWSERADDONSVIEW_BIN = 'BrowserAddonsView.exe'
LASTACTIVITYVIEW_BIN = 'LastActivityView.exe'
CPORTS_BIN = 'cports.exe'

# Limit size of file: 12MB
MAX_SIZE_FILE = 12 * 1024 * 1024

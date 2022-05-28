#!/usr/bin/env python

import sys
from scanner.info import info_task
from scanner.file import files_task
from scanner.event import event_task
from scanner.addons import addons_task
from scanner.autorun import autorun_task
from scanner.network import network_task
from scanner.process import process_task
from scanner.activity import activity_task
from scanner.utils import internet_check_by_requests
from scanner.utils import send_report_task, zip_list_file, is_admin


def main():
    # Check Administrator
    if not is_admin():
        print('This program requires run as Administrator.')
        sys.exit(1)

    # Check internet connection
    if not internet_check_by_requests():
        print('Please check your internet connection.')
        sys.exit(2)

    info_data = info_task()
    activity_data = activity_task()
    addons_data = addons_task()
    autorun_data = autorun_task()
    event_data = event_task()
    file_data = files_task()
    network_data = network_task()
    process_data = process_task()
    zip_name = zip_list_file()
    print(zip_name)


if __name__ == '__main__':
    main()

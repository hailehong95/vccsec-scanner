#!/usr/bin/env python

import os
import time
import shlex
import socket
import psutil
import distro
import datetime
import platform
import subprocess

from scanner.setting import DATA_DIR
from scanner.crypto import secure_string_random
from scanner.utils import write_dicts_to_json_file
from scanner.utils import get_primary_ip_with_internet, get_primary_ip_without_internet, internet_check_by_requests


# Ref: https://stackoverflow.com/a/43478599
def get_network_info():
    network_info = list()
    primary_ip = [get_primary_ip_with_internet(), get_primary_ip_without_internet()]
    primary_ip = list(set(primary_ip))
    for interface, snicaddrs in psutil.net_if_addrs().items():
        if len(snicaddrs) > 2:
            temp = dict()
            temp['interface'] = interface
            for snic in snicaddrs:
                if snic.family == socket.AF_INET:
                    temp['ipv4'] = snic.address
                    temp['internet_on'] = True if snic.address in primary_ip else False
                elif snic.family == socket.AF_INET6:
                    temp['ipv6'] = snic.address
                else:
                    temp['mac_address'] = snic.address
            network_info.append(temp)
    return network_info

"""
# Ref: https://stackoverflow.com/a/43478599
def get_network_info():
    network_info = list()
    net_data = dict()
    if internet_check_by_requests():
        primary_ip = get_primary_ip_with_internet()
    else:
        primary_ip = get_primary_ip_without_internet()
    for interface, snicaddrs in psutil.net_if_addrs().items():
        for snic in snicaddrs:
            if snic.address == primary_ip:
                network_info = psutil.net_if_addrs()[interface]
                net_data['interface'] = interface
    net_data['ipv4'] = [x.address for x in network_info if x.family == socket.AF_INET][0]
    # net_data['ipv6'] = [x.address for x in network_info if x.family == socket.AF_INET6][0]
    net_data['mac_address'] = [x.address for x in network_info if x.family != socket.AF_INET6 and x.family != socket.AF_INET][0]
    return net_data
"""


# Get all information in Windows, Linux, macOS
def get_system_info():
    sys_info_data = list()
    info = dict()
    os_platform = platform.system()
    try:
        info['platform'] = os_platform
    except:
        info['platform'] = None
    try:
        if os_platform == 'Windows':
            #info['operating_system'] = subprocess.check_output('systeminfo | findstr /B /C:"OS Name"', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').replace('  ','').partition('OS Name:')[2].strip(' \r\n')
            info['operating_system'] = ' '.join(['Microsoft', platform.system(), platform.release(), platform.win32_edition()])
        else:
            info['operating_system'] = ' '.join(distro.linux_distribution())
    except:
        info['operating_system'] = None
    try:
        if os_platform == 'Windows':
            info['kernel_build'] = platform.version()
        else:
            info['kernel_build'] = platform.release()
    except:
        info['kernel_build'] = None
    try:
        info['machine'] = platform.machine()
    except:
        info['machine'] = None
    try:
        info['hostname'] = platform.node()
    except:
        info['hostname'] = None
    try:
        info['username'] = os.getlogin()
    except:
        info['username'] = None
    try:
        info['boot_time'] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    except:
        info['boot_time'] = None
    try:
        info['network'] = get_network_info()
    except:
        info['network'] = None
    try:
        if os_platform == 'Windows':
            wmic_cmd = 'wmic qfe get hotfixid'
            hotfix_ = subprocess.run(shlex.split(wmic_cmd), stdout=subprocess.PIPE).stdout.decode('utf-8', errors='ignore').replace('\r\r\n', '').split(' ')
            hotfix = [x for x in hotfix_ if x != 'HotFixID' and x != '']
            hotfix.sort()
            info['hotfix'] = hotfix
    except:
        info['hotfix'] = None
    sys_info_data.append(info)
    return sys_info_data


# Get information on system
def info_task():
    system_info = list()
    if platform.system() in ['Windows', 'Linux', 'Darwin']:
        system_info = get_system_info()
    else:
        system_info.append("Operating system is not detected.")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    write_dicts_to_json_file(system_info, 'info.json')
    return len(system_info)

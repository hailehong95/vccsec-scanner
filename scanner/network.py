#!/usr/bin/env python

import os
import socket
import psutil
import logging
import platform
import traceback

from scanner.setting import DATA_DIR
from scanner.utils import write_dicts_to_json_file

# Network connection on Windows, Linux, macOS
def get_network_connection():
    proto_map = {
        (socket.AF_INET, socket.SOCK_STREAM): 'tcp',
        (socket.AF_INET6, socket.SOCK_STREAM): 'tcp6',
        (socket.AF_INET, socket.SOCK_DGRAM): 'udp',
        (socket.AF_INET6, socket.SOCK_DGRAM): 'udp6',
    }
    try:
        conn = list()
        proc_names = dict()
        for p in psutil.process_iter(['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']
        for c in psutil.net_connections(kind='inet'):
            data = dict()
            data['protocol'] = proto_map[(c.family, c.type)]
            data['local_address'] = c.laddr.ip
            data['local_port'] = c.laddr.port
            data['remote_address'] = c.raddr.ip if c.raddr else None
            data['remote_port'] = c.raddr.port if c.raddr else None
            data['status'] = c.status
            data['pid'] = c.pid or None
            data['name'] = proc_names.get(c.pid, '?') or ''
            conn.append(data)
    except Exception as e:
        logging.error(traceback.format_exc())
    return conn


# Get Network connection on system
def network_task():
    network_data = list()
    if platform.system() in ['Windows', 'Linux', 'Darwin']:
        network_data = get_network_connection()
    else:
        network_data.append("Operating system is not detected.")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    write_dicts_to_json_file(network_data, 'network.json')
    return len(network_data)

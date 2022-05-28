#!/usr/bin/env python

from Cryptodome.PublicKey import RSA
from utils.setting import RSA_KEY_DIR, RSA_PRI_KEY, RSA_PUB_KEY

import os
import string
import random
import logging
import traceback


# Ref: https://stackoverflow.com/a/2257449
def secure_string_random(n):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(n))


# Ref: https://pycryptodome.readthedocs.io/en/latest/src/examples.html#generate-public-key-and-private-key
def generate_rsa_keys():
    try:
        new_key = RSA.generate(int(2048))
        private_key = new_key.exportKey()
        public_key = new_key.publickey().exportKey()
        with open(os.path.join(RSA_KEY_DIR, RSA_PRI_KEY), 'wb') as f:
            f.write(private_key)
        with open(os.path.join(RSA_KEY_DIR, RSA_PUB_KEY), 'wb') as f:
            f.write(public_key)
    except Exception as e:
        logging.error(traceback.format_exc())

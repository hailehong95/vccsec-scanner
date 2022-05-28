#!/usr/bin/env python
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import os
import zlib
import base64
import string
import random


def secure_string_random(n):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(n))


def generate(keydir):
    new_key = RSA.generate(4096)
    private_key = new_key.exportKey()
    public_key = new_key.publickey().exportKey()
    with open(os.path.join(keydir, 'key.pri'), 'wb') as f:
        f.write(private_key)
    with open(os.path.join(keydir, 'key.pub'), 'wb') as f:
        f.write(public_key)


def get_rsa_cipher(keydir, keytype):
    with open(os.path.join(keydir, f'key.{keytype}')) as f:
        key = f.read()
    rsakey = RSA.importKey(key)
    return (PKCS1_OAEP.new(rsakey), rsakey.size_in_bytes())


def encrypt(keydir, plaintext):
    compressed_text = zlib.compress(plaintext)
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)
    cipher_rsa, _ = get_rsa_cipher(keydir, 'pub')
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    msg_payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    encrypted = base64.encodebytes(msg_payload)
    return(encrypted)


def decrypt(keydir, encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    cipher_rsa, keysize_in_bytes = get_rsa_cipher(keydir, 'pri')
    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    ciphertext = encrypted_bytes.read()
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)
    plaintext = zlib.decompress(decrypted)
    return plaintext


# keydir = scanner.setting.KEY_DIR
# plaintext = b'This is secret message!'
# encrypted = scanner.crypto.encrypt(keydir, plaintext)
# print(encrypted)
# print(scanner.crypto.decrypt(keydir, encrypted))

# -*- coding:utf-8 -*-

import os
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet, MultiFernet

ext = ".four"
BLOCK_SIZE = 32
FCRYPTERAES = True

if FCRYPTERAES:
    from Crypto.Cipher import AES
    from Crypto import Random

def pad(s):
    return s + b"\0" * (BLOCK_SIZE - len(s) % BLOCK_SIZE)

class Fcrypter:
    def __init__(self, key):
        self.key = pad(key.encode())
        self.path = os.getcwd()
        self.extend = os.sep
        self.merge = self.path+self.extend
    def aesCrypt(self, veri):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        cipher_bytes = cipher.encrypt(pad(veri))
        data = iv + cipher_bytes
        return b64encode(data)

    def aesDecrypt(self, crypted_data):
        crypted_data = b64decode(crypted_data)
        iv = crypted_data[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(crypted_data[AES.block_size:]).rstrip(b"\0")
        return decrypted

    def encryptFile(self, file, aes=FCRYPTERAES):
        if not self.extend in file:
            file = self.merge+file
        if aes:
            with open(file, "rb") as _file:
                text = _file.read()
            encrypted = self.aesCrypt(text)
            with open(file + ext, "wb") as encrypted_file:
                encrypted_file.write(encrypted)
                os.remove(file)
        else:
            fernet_cipher = MultiFernet([Fernet(b64encode(self.key)), Fernet(b64encode(self.key[::-1]))])
            with open(file, "rb") as _file:
                data = _file.read()
            crypted = fernet_cipher.encrypt(data)
            with open(file + ext, "wb") as new:
                new.write(crypted)
                os.remove(file)

    def decryptFile(self, file, aes=FCRYPTERAES):
        if not self.extend in file:
            file = self.merge + file
        if aes:
            with open(file, "rb") as _file:
                crypted_text = _file.read()
            decrypted = self.aesDecrypt(crypted_text)
            with open(file[:-int(len(ext))], "wb") as decrypted_file:
                decrypted_file.write(decrypted)
                os.remove(file)
        else:
            fernet_cipher = MultiFernet([Fernet(b64encode(self.key)), Fernet(b64encode(self.key[::-1]))])
            with open(file, "rb") as _file:
                data = _file.read()
            decrypted = fernet_cipher.decrypt(data)
            with open(str(file).rstrip(ext), "wb") as new:
                new.write(decrypted)
                os.remove(file)

    def encryptFolder(self, path, aes=FCRYPTERAES):
        for root, dirs, files in os.walk(path):
            for x in files:
                file = os.path.join(root, x)
                self.encryptFile(file=file, aes=aes)

    def decryptFolder(self, path, aes=FCRYPTERAES):
        for root, dirs, files in os.walk(path):
            for x in files:
                file = os.path.join(root, x)
                self.decryptFile(file=file, aes=aes)
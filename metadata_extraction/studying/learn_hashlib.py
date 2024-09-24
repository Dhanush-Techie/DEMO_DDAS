import hashlib

def fileHashing(fileName):
    hash_blake2b = hashlib.blake2b()
    check = hashlib.blake2b()
    print(hash_blake2b.hexdigest())
    print(check.hexdigest())

    with open(fileName,'rb') as f:
        while True:
            data = f.read(100)
            if not data:
                break

            hash_blake2b.update(data)
    return hash_blake2b.hexdigest()

# print(fileHashing('C:/Users/pravi/Documents/Pravin_Resume.pdf'))

import os
import psutil

drives = [drive.device for drive in psutil.disk_partitions()]
print(drives)

for root_dir in drives:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"Found directory: {dirpath}")
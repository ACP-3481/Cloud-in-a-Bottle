import socket
import os
import sys
from Crypto.Cipher import AES
from base64 import b32encode, b32decode

# Event codes to send to server
# UPD : upload
# DLD : download
# FIN : upload or download finished
# LGN : Login
# USR : submit user account name
# PWD : submit user password
# KEY : submit pre-master secret
# END : end connection to server
# ECR : encrypt file
# DCR : decrypt file


def upload_file(server: socket.socket, filename: str):
    # Get the filesize of the file
    filesize = os.stat(filename).st_size
    # If open(filename, "type").read(bytesize) doesn't get the same number of bytes
    # it just hangs there waiting
    # Solution: calculate how many times we send 4096 bytes then send the remainder
    # the server will do the same on it's end
    size_a = filesize // 4096
    size_r = filesize % 4096

    name_from_path = ""
    for i in range(len(filename) - 1, -1, -1):
        if filename[i] == "\\":
            break
        else:
            name_from_path += filename[i]
    name_from_path = name_from_path[::-1]

    # Save the filename, file size, number of 4096 bytes, and remainder
    format_filename = f"{name_from_path}|{filesize}|{size_a}|{size_r}"
    filename_size = sys.getsizeof(format_filename.encode())
    # After sending acknowledgement, server expects a byte size of 4096 bytes
    # Make the filename 4096 bytes
    if filename_size < 4096:
        for i in range(4096 - filename_size):
            format_filename += " "
    # Send the filename, file size, number of 4096 bytes, and remainder to the server
    server.send(format_filename.encode())

    # Send the file
    with open(filename, "rb") as f:
        for i in range(size_a):
            bytes_read = f.read(4096)
            server.sendall(bytes_read)
        bytes_read = f.read(size_r)
        server.sendall(bytes_read)
        print("File sent")

    # The server is supposed to send "File {filename} {bytesize} bytes received"
    print(server.recv(4096).decode().strip())


def download_file(server, filename: str, destination: str):
    pass


# C:\Users\4225482\Documents\python.py
def encrypt_file(key, file_path):
    filename = file_path[file_path.rfind("\\")+1:]
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    cipher_filename, tag = cipher.encrypt(filename.encode())

    with open(file_path, "rb") as binary_file:
        cipher_file = cipher.encrypt(binary_file.read())

    return nonce, cipher_filename, cipher_file

def decrypt_file(key, nonce, cipher_filename, cipher_file=None):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    filename = cipher.decrypt(cipher_filename)
    if cipher_file == None:
        return filename

#!/usr/bin/python3           # This is client.py file

import socket


# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# connection to hostname on the port.
s.connect((host, port))

# s.send('hello socket'.encode('utf-8'))

import os
filename = os.getcwd() + '/sample/image/dddd.jpg'
print(filename)
f = open(filename,'rb')
data = f.read(1024)
s.send(data)


# Receive no more than 1024 bytes
msg = s.recv(1024)

# s.close()

print(msg.decode('utf-8'))

#!/usr/bin/env python3

############################################
# @author:  Pavol Gumancik                 #
#           xguman01                       #
#           <xguman01@stud.fit.vutbr.cz>   #
############################################

import socket

HOST_NAME = '127.0.0.1'
PORT = 1235


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST_NAME, PORT))
    s.sendall(b'GET /resolve?name=apple.cook&type=A HTTP/1.1')
    data = s.recv(1024)
print('Received', repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST_NAME, PORT))
    s.sendall(b'POST/dns-query HTTP/1.1')
    data = s.recv(1024)
print('Received', repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST_NAME, PORT))
    s.sendall(b'fuck')
    data = s.recv(1024)
print('Received', repr(data))

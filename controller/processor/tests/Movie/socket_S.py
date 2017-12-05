# -*- coding:utf-8 -*-

# socket을 사용하기 위한 python module import
from socket import *
from data_file import *

import pickle
import struct, os


ssock=socket(AF_INET, SOCK_STREAM)
ssock.bind(SocketInfo.ADDR)
ssock.listen(5)
csock=None

f=open("movielist.txt", 'ab+')
test=MInfo(1, "spi", ["01:30"],  MSeat())
test2=MInfo(2, "abc", ["02:00"], MSeat())
movietest=[test, test2]
pickle.dump(movietest, f)
f.close()

def sendCommend(string):
    csock.send(string.encode())

def sendByte(byte):
    csock.send(byte)

def recvCommend():
    return csock.recv(SocketInfo.BUFSIZE).decode()

while True :

    if csock is None :

        f = open("movielist.txt", "rb")
        data = f.read()

        print "waiting for connection..."
        csock, addr_info = ssock.accept()

        sendCommend("MOVIE_INFO")
        commend=recvCommend()

        if commend=="MOVIE_INFO_READY" :
            FILE_SIZE = os.path.getsize("movielist.txt")
            FILE_SIZE = struct.pack('L', FILE_SIZE)
            sendByte(FILE_SIZE)

            while data:
                sendByte(data)
                data = f.read(SocketInfo.BUFSIZE)

            f.close()

        # 파일을 보낸다. 코드와 함께 영화 저장정보를 1차로 전송한다.
        print "Send data to > ", addr_info
        print ""

    else:

        print "waiting for response..."
        commend=recvCommend()
        print "accept >> "+commend
        print ""

        if commend=="CLIENT_START_READY" :
            sendCommend("MOVIE_SYSTEM_START")

        elif commend=="CLIENT_MOIVE_CHOICE" :

            # 선택한 영화에 대한 정보를 저장한다.
            pass

        else: pass
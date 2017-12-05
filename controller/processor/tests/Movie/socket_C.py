# -*- coding:utf-8 -*-

from socket import  *
from sys import exit
from method_C import *
from data_file import *

import struct
import pickle

class SocketInfo(SocketInfo) :
    HOST='127.0.0.1'

movieList=[]
method=Method()
FILE_LEN=0

def sendCommend(string):
    csock.send(string.encode())

def recvCommend():
    return csock.recv(SocketInfo.BUFSIZE).decode()

def recvByte():
    return csock.recv(SocketInfo.BUFSIZE)

csock = socket(AF_INET, SOCK_STREAM)
csock.connect(SocketInfo.ADDR)

while True:
    try:
        commend = recvCommend()
        print " >> server say : ", commend

        if commend=="MOVIE_INFO" :
            sendCommend("MOVIE_INFO_READY")
            print "in MOVIE, wait data response"
            FILE_SIZE = csock.recv(8)
            FILE_SIZE = struct.unpack('L', FILE_SIZE)[0]

            f = open("movielistTemp.txt", "ab+")
            print "File open", "------------------------------------"

            while True:
                data = recvByte()
                if not data: break

                f.write(data)
                FILE_LEN += len(data)
                if FILE_LEN == int(FILE_SIZE): break

            print "close File", "------------------------------------"
            f.close()

            csock.send("CLIENT_START_READY")
            print "------------------------------------------------------------------------------------"

        if commend=="MOVIE_SYSTEM_START":

            f = open("movielistTemp.txt", "r")
            movieList = pickle.load(f)

            print len(movieList)

            inside=method.MovieSystemStart(movieList)
            if inside[0]==1 :
                sendCommend("CLIENT_MOIVE_CHOICE,"+inside[1]+","+inside[2])

            if inside[0]==2 :
                sendCommend("CLIENT_MOVIE_PLANS,"+inside[1]+","+inside[2])


        print "---------------------------"

    except Exception as e :
        print "%s:%s" %(e, SocketInfo.ADDR)
        csock.close()
        exit()

    print "connect is success"




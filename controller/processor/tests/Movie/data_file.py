# -*- coding:utf-8 -*-

import copy

# 소켓에 대한 정보


class SocketInfo():
    HOST = ''
    PORT = 1024
    BUFSIZE = 1024
    ADDR = (HOST, PORT)


class MSeat():
    # 좌석유무 정보를 저장할 data 공간 생성
    def __init__(self):
        mSeat = {}
        for i in range(ord('A'), ord('F')):
            for j in range(1, 6):
                mSeat[(chr(i), j)] = 0


# 영화에 대한 data class
class MInfo():

    # 상영관번호, 영화이름, 상영시간, 좌석
    mRoom = None
    mName = None
    mTime = []
    mTotalSeat = []
    mTotal = None

    # 생성자 정의
    def __init__(self, room, name, time, mSeat):
        self.mRoom, self.mName, self.mTime = room, name, time

        # 여기서 TotalSeat을 초기화 해주지 않으면 그전값이 저장되어있다. why?
        # self.mTotalSeat=[]

        # 각 상영시간에 해당하는 좌석 정보를 저장할 딕셔너리 선언
        # copy로 딕셔너리를 복사해주어야 각각에 해당하는 좌석 예매 정보를 가질 수 있다.
        for i in range(len(self.mTime)):
            self.mTotalSeat.append(copy.copy(mSeat))


# 회원 정보에 대한 data class
class PInfo():

    # 회원 아이디, 패스워드, 이름, 회원등급
    pID = None
    pPW = None
    pName = None
    pGrade = None

    # 생성자 정의
    def __init__(self, id, pw, name):
        self.pID, self.pPW, self.pName = id, pw, name


# 예매 정보에 대한 data class
class BInfo():

    # 예매 번호, 예매 정보(회원아이디, 영화 이름, 상영시간, 좌석정보)
    bID = None
    sInfo = ()

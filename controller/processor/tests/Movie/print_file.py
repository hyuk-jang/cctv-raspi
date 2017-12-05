# -*- coding:utf-8 -*-

def menu():
    print """\n- - - - - - - - - - - - - - - - - -
        1. 영화 예매
        2. 영화 상영시간 확인
        3. 영화 관리
        4. 총 수입확인
        5. 프로그램 종료
- - - - - - - - - - - - - - - - - -"""
    return raw_input(" >> ")


# 좌석에 대한 정보 출력
#class printSeat():

def PrintSeat(mSeat):

    print "\n____________S C R E E N____________\n"
    for i in range(ord('A'), ord('F')):
        print "\t",
        for j in range(1, 6):
            if mSeat.get((chr(i), j))==0: print" o ",
            elif mSeat.get((chr(i), j))==1: print" x ",
        print ""

    print "\n________좌석 예약 상황입니다________"

#    def __init__(self, mSeat): self.mSeat=mSeat


# 영화목록에 대한 정보 출력
"""class printMovie() :

    # var=[(영화이름, (상영시간, ...)), ... ]
    var=[]"""

def PrintMovie(movieList):
    print "\n- - - - 영화를 선택해주세요 - - - - "
    for i in range(len(movieList)) :
        print movieList[i].mName
        for j in range(len(movieList.mTime)) : print movieList[i].mTime[j]+" ",
        print "\n"
    # 영화제목, 상영시간 순으로 입력받기. ( 정규형식 부분 참조하기 )
    #for i in range(0, len(movieList)): print "        " + str(i + 1) + ". " + movieList[i].mName
    print "- - - - - - - - - - - - - - - - - - "
    choice=raw_input("  >> ")

    # 스플릿으로 잘라서 저장하기.
    choice=choice.split(', ')
    chName, chTime=choice[0], choice[1]

    return chName, chTime

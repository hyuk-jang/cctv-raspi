# -*- coding:utf-8 -*-

from print_file import *
from error_check import *

class Method() :

    def MovieSystemStart(self, movieList) :

        while True :
            ch=choice(menu(), 5)+1
            if ch!=False :
                print " chchchchchchchchch >> " + str(ch)
                if ch == 3: pass
                # 영화 관리

                elif ch == 5: pass
                # 프로그램 종료

                else :

                    if len(movieList) == 0:
                        print """\n- - - 상영중인 영화가 없습니다 - - -
죄송죄송 돌아가주세요 영화가 부족해요 티티\n\n\n"""

                    else :
                        if ch==1 or ch==2 :
                            while True :
                                chname, chTime = PrintMovie(movieList)
                                chname, chTime = choice_Movie(chname, chTime, movieList)
                                if not chname or not chTime : continue
                                else : return ch, chname, chTime

                            # 영화 예매 선택 및, 영화 상영시간 확인

                        elif ch == 4 :
                            # 총 수입확인
                            print "\n- - - - 영화 총 수입 입니다 - - - -"
                            result = 0
                            for i in range(len(movieList)):
                                print "  \"%-10s\" ic : %10d won" % (movieList[i].mName, movieList[i].mTotal)
                                result += movieList[i].mTotal
                            print "- - - - - - - - - - - - - - - - - -"
                            print "     Total >> " + str(result)
                            print "- - - - - - - - - - - - - - - - - -"

            else : pass

    def SeatView(self, movieList) : PrintSeat(movieList)




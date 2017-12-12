# -*- coding: utf-8 -*- 

import threading, uuid, os
from apscheduler.schedulers.blocking import BlockingScheduler
from picamera import PiCamera

from ultrasoundHcHr04 import getDictance

import config

import time
 
class CctvMonitoring (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 

        self.controlInfo = config.controlInfo()
        print('self.controlInfo', self.controlInfo)

        self.criticalValue = self.controlInfo['criticalValue']     # 초음파 측정 임계치 (20cm)
        self.recentCalcDistanceNum = self.controlInfo['recentCalcDistanceNum'] # 최근 10개 측정 (10초 )
        self.distanceList = []
        self.currParkingStatus = 'reset'

        # Camera 동작
        self.filePath = os.getcwd() + '/image/'
        self.camera = PiCamera()
        self.camera.start_preview()

    # Thread 시작 (스케줄러 동작)
    def run(self):
        sched = BlockingScheduler()
        sched.add_job(self.measureDistance, 'interval', seconds=self.controlInfo['ultrasoundsInterval'])
        sched.start()

    # 사진 저장 및 File NAme 반환
    def captureImage(self):
        # time.sleep(10)
        fileName = str(uuid.uuid4())
        self.camera.capture(self.filePath + fileName + '.png')
        return fileName


    # main.py에 의해서 호출(1분 단위)되며 distanceList 값에 따라 반환
    def judgeIllegal(self):
        # 최근 10초동안 연속된 주차 데이터가 없다면 불법주차 해제(10초는 사물이 지나가면서 측정될수 있으므로 유예)
        returnValue = ''

        distanceLen = self.distanceList.__len__()

        # 필요 충족 list 개수를 못채웠다면 reset
        if distanceLen < self.recentCalcDistanceNum:
            returnValue = 'reset'
        else :
            for dist in self.distanceList[-self.recentCalcDistanceNum:]:
                # print('dist', dist)
                if dist < self.criticalValue:
                    returnValue = 'reset'
                    break

            # 불법 주차가 해제되지 않을 경우
            if returnValue != 'reset':
                # 불법 주차 내역 추출
                less_than_critical = list(filter(lambda x: x < self.criticalValue, self.distanceList))
                # 1 분동안 모두 불법주차한 데이터라면
                if less_than_critical.__len__() == 0:
                    # 이전 상태가 정상이라면 new
                    if self.currParkingStatus == 'reset':
                        returnValue = 'new'
                    else:
                        returnValue = 'continue'
                # 나머지 상태는 모두 New
                else:
                    returnValue = 'new'
        
        # list를 비움. 
        del(self.distanceList[:])
        # print('self.distanceList  Empty', self.distanceList)
        # 현재 상태 저장
        self.currParkingStatus = returnValue
        print('returnValue', returnValue)
        return returnValue

 
    # 쓰레드로 1초에 한번씩 초음파센서 거리 측정값을 리스트에 저장
    def measureDistance(self):
        # '''
        # TEST
        # '''
        # import random
        # distance = random.randrange(30, 50)
        
        distance = getDictance()
        print('distance',distance, self.distanceList.__len__())

        self.distanceList.append(round(distance, 1))



if __name__ == '__main__':
    print('Curr MeasureCctv.py Process ^^^^^^^^^^')
    try:
        cctvMonitoring = CctvMonitoring()
        cctvMonitoring.daemon = True
        cctvMonitoring.start()

        import logging
        logging.basicConfig()

        sched2 = BlockingScheduler()
        sched2.add_job(cctvMonitoring.judgeIllegal, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour='*', minute='*', second='*/10')    
        sched2.start()

        print("### End ###")

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    except:
        print('occur except')





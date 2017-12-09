# -*- coding: utf-8 -*- 

# 예제
import threading, requests, time

from ultrasoundHcHr04 import getDictance

from apscheduler.schedulers.blocking import BlockingScheduler
 
class CctvMonitoring (threading.Thread):
    def __init__(self):
        # self.ultrasoundInfo = ultrasoundInfo
        threading.Thread.__init__(self) 

        self.criticalValue = 20     # 초음파 측정 임계치 (20cm)
        self.distanceList = []
        self.currParkingStatus = 'reset'

        # self.url = url

    # 스케줄러 동작
    def run(self):
        sched = BlockingScheduler()
        sched.add_job(self.measureDistance, 'interval', seconds=1)
        sched.start()

    # main.py에 의해서 호출(1분 단위)되며 distanceList 값에 따라 반환
    def judgeIllegal(self):
        # 최근 10초동안 연속된 주차 데이터가 없다면 불법주차 해제(10초는 사물이 지나가면서 측정될수 있으므로 유예)
        returnValue = ''
        for dist in self.distanceList[-10:]:
            if dist < self.criticalValue:
                returnValue = 'reset'
        less_than_critical = list(filter(lambda x: x < self.criticalValue, self.distanceList))
        # 1 분동안 모두 불법주차한 데이터라면
        if less_than_critical.__len__() == 0:
            # 이전 상태가 정상이라면 new
            if self.currParkingStatus == 'reset' :
                returnValue = 'new'
            else:
                returnValue = 'continue'
        # 나머지 상태는 모두 New
        else:
            returnValue = 'new'
        
        # list를 비움. 
        self.distanceList.clear()

        return returnValue

 
    # 쓰레드로 1초에 한번씩 초음파센서 거리 측정값을 리스트에 저장
    def measureDistance(self):
        # distance = 111
        distance = getDictance()
        # print('distance',distance, self.distanceList)

        self.distanceList.append(round(distance, 1))




cctvMonitoring = CctvMonitoring()
cctvMonitoring.start()

# t = HtmlGetter('http://google.com')
# t.start()
 
print("### End ###")

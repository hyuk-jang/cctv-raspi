

import threadModle
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

import time

# sched = BlockingScheduler()
# sched.add_job(threadModle.test, 'interval', seconds=2)
# sched.start()

print('alksjdsl')


def sleepGo():
    while(True):
        threadModle.test()
        time.sleep(1)

def runGo():
    t = threading.Thread(target=threadModle.init)
    t.start()    

def cronTest():
    itNum = threadModle.getNum()
    print('itNum', itNum)

def test(num, maxNum):
    print('hi', num, maxNum)
    return num    
    

# sleep 으로 호출할 경우 진행 안되는 현상 확인
# sleepGo()

# Tread로 돌릴 경우 정상적으로 진행
runGo()

sched = BlockingScheduler()
sched.add_job(cronTest, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour='*', minute='*', second='*/10')    
sched.start()
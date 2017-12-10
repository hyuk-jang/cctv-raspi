

from apscheduler.schedulers.blocking import BlockingScheduler

def init():
    sched = BlockingScheduler()
    sched.add_job(test, 'interval', seconds=1)
    sched.start()


num = 0

def test():
    global num
    num = num + 1
    print('hi', num)
    # return num

def getNum():
    global num
    returnValue = num
    num = 0
    return returnValue


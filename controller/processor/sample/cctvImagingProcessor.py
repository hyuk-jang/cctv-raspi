import datetime
import uuid
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# piCamera를 이용하여 영상 캡쳐
# @return {string} Capture 한 File 명
def captureImage():
    dt = datetime.datetime.now()
    print(dt.strftime("%Y-%m-%d %H:%M:%S"))
    # TODO Image Capture
    fileName = uuid.uuid4()

    return fileName

# 불법주차여부 판단
# @param {dictionary} prev, curr
# @return {string} 불법 주차 여부 'continue': 불법주차지속, 'new': 신규 불법주차, 'reset': 불법주차 해제
# TODO 불법주차 판단 Code 작성
def judgeIllegalParking(picStorage):
    # TODO 불법주차된 차량이 없다는 판단 코드 (curr Image만 판단)
    if True:
        return 'reset'

    # 아래는 2장의 Image 비교
    # TODO 불법 주차된 차량이 계속 있다는 판단 코드 
    if True:
        return 'continue'

    # TODO 불법 주차된 차량이 교체되었다는 판단 코드
    if True:
        return 'reset'


def init():
    # 1분마다 실행 스케줄러
    sched.add_job(captureImage, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour='*', minute='*', second='0')

# Scheduler Cron 을 이용한 1분단위 실행 ( 1번만 실행해야 함)
def runCron():
    print('runCron')
    sched.start()
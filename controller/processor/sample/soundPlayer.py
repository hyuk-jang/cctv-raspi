#-*- coding: utf-8 -*-

from gtts import gTTS
import os

import platform


# 최초 1회 실행. mp3 파일을 생성하여 저장
# TODO def 에서 datetime 을 받아서 실시간으로 mp3를 생성하는 로직 필요
def init():
    currentPath = os.getcwd()
    folderPath = currentPath + '/sound/'

    filePath = folderPath + 'silentAlarm.mp3'
    tts = gTTS(text='    ', lang='ko')
    tts.save(filePath)

    filePath = folderPath + 'firstAlarm.mp3'
    tts = gTTS(text='       불법 주정차 시간이 15분을 경과하였습니다. 신속히 차량을 이동하여 주십시오', lang='ko')
    tts.save(filePath)

    filePath = folderPath + 'secondAlarm.mp3'
    tts = gTTS(text='       불법 주정차 시간이 20분을 경과하였습니다. 신속히 차량을 이동하여 주십시오', lang='ko')
    tts.save(filePath)

    filePath = folderPath + 'thirdAlarm.mp3'
    tts = gTTS(text='       불법 주정차 시간이 25분을 경과하였습니다. 30분을 경과하면 범칙금이 납부될 예정이오니 신속히 차량을 이동하여 주십시오', lang='ko')
    tts.save(filePath)

    filePath = folderPath + 'fourthAlarm.mp3'
    tts = gTTS(text='       불법 주정차 시간이 30분을 경과하였습니다. 범칙금이 부과되었습니다.', lang='ko')
    tts.save(filePath)

# init에서 생성한 mp3 4개를 depth(1~4) 에 따라서 방송
# params {int} illegalityParkingImgList length
# return {boolean} 음성 재생 성공 실패
def startAlarm(illegalLength):
    print('startAlarm illegal length', illegalLength)
    folderPath = os.getcwd() + '/sound/'
    storageLen = illegalLength
    quotient = storageLen // 5  # 몫
    remainder = storageLen % 5  # 나머지

    # 나머지가 0이 아닐경우 무음
    if remainder != 0:
        filePath = folderPath + 'silentAlarm.mp3'
    # 최초
    elif quotient == 3 :
        filePath = folderPath + 'firstAlarm.mp3'
    elif quotient == 4:
        filePath = folderPath + 'secondAlarm.mp3'
    elif quotient == 5:
        filePath = folderPath + 'thirdAlarm.mp3'
    elif quotient == 6:
        filePath = folderPath + 'fourthAlarm.mp3'
    else:
        filePath = folderPath + 'silentAlarm.mp3'

    # print (platform.system(), platform.release())
    # 윈도우일 경우
    if platform.system() == 'Windows':
        print('Windows')
        os.system(filePath)
    else:   # 라즈비안일 경우
        print('Shell', filePath)
        os.system("mplayer " + filePath)
    
    return True


if __name__ == '__main__':
    print('Curr soundPlayer.py Process ^^^^^^^^^^')
    try:
        startAlarm(20)
        print("### End ###")

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")

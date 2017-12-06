import requester
import soundPlayer
import cctvImagingProcessor

import config

# CCTV Main Processor Def
def main():
    # 이전 사진, 현재 캡쳐 사진을 저장할 변수
    picStorage = {'prev':'', 'curr': ''}
    # 불법주차 이미지 명 리스트
    illegalityParkingImgList = []
    # illegalityParkingImgList = ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
    # 30분이 지나도록 불법주차가 유지될 경우 False로 전환하고 main logic 불법주차 처리 하지 않음
    hasObserve = True

    info = config.getSocketInfo()
    # print(info, info['host'])


    # 음성 파일 만들고 시작
    # soundPlayer.init()
    
    # 음성 출력
    # resAlarm = soundPlayer.startAlarm(illegalityParkingImgList)
    # print('resAlarm', resAlarm)

    # Requst Http Get
    # result = requester.requestGetHttp('http://localhost:3333')

    # Send Image With Socket
    # requester.submitImgWithSocket('aaaa', False, info)

main()

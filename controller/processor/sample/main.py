

import requester

import soundPlayer

# 음성 파일 만들고 시작
# soundPlayer.init()


# 이전 사진, 현재 캡쳐 사진을 저장할 변수
picStorage = {'prev':'', 'curr': ''}
# 불법주차 이미지 명 리스트
illegalityParkingImgList = []
# illegalityParkingImgList = ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']

hasObserve = True

# 음성 출력
resAlarm = soundPlayer.startAlarm(illegalityParkingImgList)
print('resAlarm', resAlarm)

# http get request 
# result = requester.requestGetHttp('http://localhost:3333')
# print(result)

# http post image submit
# result = requester.requestPostHttp('http://localhost:3333/img-receiver', 'dddd', 'jpg')

requester.submitImgWithSocket('aaaa', False)

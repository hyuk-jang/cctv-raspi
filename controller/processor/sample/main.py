from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
# Customize Module
import requester, soundPlayer, cctvImagingProcessor, config

class MainProcessor() :
    def __init__(self, basePictureName):
        # 기준사진, 이전 사진, 현재 캡쳐 사진을 저장할 변수
        self.picStorage = {'base':basePictureName, 'prev':'', 'curr': ''}
        # 불법주차 이미지 명 리스트
        self.illegalityParkingImgList = []
        # self.illegalityParkingImgList = ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']
        # 30분이 지나도록 불법주차가 유지될 경우 False로 전환하고 main logic 불법주차 처리 하지 않음
        self.hasObserve = True
        
        # 음성 파일 만들고 시작
        # soundPlayer.init()

        # 1분마다 실행 스케줄러 등록
        # self.sched = BlockingScheduler()
        # self.sched.add_job(self.main, 'cron', year='*', month='*', day='*', week='*', day_of_week='*', hour='*', minute='*', second='0')

    # def runScheduler(self):
    #     self.sched.start()

    # CCTV Main Processor Def
    def main(self):
        '''
            카메라 capture
        '''
        dt = datetime.datetime.now()
        illegalStatus = self.imageProcessing()

        '''
            Web Server에서 불법 주차 전환 여부 확인 후 조치
        '''
        # NOTE 이번 Project에서는 구현하지 않도록 함


        '''
            음성 출력 (bluetooth speaker)
        '''
        # FIXME Bluetooth Speaker가 Sound 재생이 없으면 Sleep 상태로 전환됨. 전환 방지를 위해 Speaker 실행토록 함.
        # sleep 상태를 방지 할 수 있는 옵션을 넣는다면 불 필요
        resAlarm = soundPlayer.startAlarm(self.illegalityParkingImgList)
        print('resAlarm', resAlarm)


        '''
            Web Server로 Processor 상태값 및 Image 전송
        '''
        self.sendCctvStatus2WebServer(illegalStatus, dt)


    # Web Server로 현재 cctv processor 상태 값을 전송
    # @param {string} illegalStatus 불법 주차 여부 'continue': 불법주차지속, 'new': 신규 불법주차, 'reset': 불법주차 해제
    # @param {datetime} dt Capture 시각
    def sendCctvStatus2WebServer(self, illegalStatus, dt):
        ts = int(dt.utcnow().timestamp())
        # print('captureTime', dt.utcnow(), captureTime, ts)

        # 현재 저장되어 있는 이미지 리스트 길이
        illegalLength = self.illegalityParkingImgList.__len__()
        '''
            Http GET Protocol 전송
        '''
        webServerInfo = config.getWebServerInfo()
        cctvProcessorInfo = config.getCctvProcessorInfo()
        socketInfo = config.getSocketInfo()
        
        count = illegalLength   # 현재 불법 주차 count
        cctvId = cctvProcessorInfo['cctvId']

        # cctv 상태 값을 받는 Web Server Url
        cctvStatusManagerUrl = webServerInfo['host'] + webServerInfo['cctvStatusManagerUrl']
        # cctv 이미지를 받는 Web Server Url
        imageReceiveManagerUrl = webServerInfo['host'] + webServerInfo['imageReceiveManagerUrl']
        # cctv 이미지를 받는 Socket Url
        imageReceiveManagerUrl = socketInfo['host'] + webServerInfo['imageReceiveManagerUrl']

        # Requst Http Get
        query = 'cctvid=' + cctvId + '&count=' + str(count) + '&status=' + illegalStatus + '&img=' + self.picStorage['curr'] + '&ts=' + str(ts)
        result = requester.requestGetHttp(cctvStatusManagerUrl, query)

        # TODO 사진 전송 POST
        # result = requester.requestPostHttp(imageReceiveManagerUrl, self.picStorage['curr'])
        result = requester.submitImgWithSocket(self.picStorage['curr'], False, socketInfo)
        
    


    # @return {string} 'reset': 불법주차 해제, 'new': 신규 불법주차, 'continue': 불법주차 지속, 'end': 불법주차 30분 초과
    def imageProcessing(self):
        # 현재 찍은 이미지명 저장
        captureName = cctvImagingProcessor.captureImage()
        # 이미지 지정 재정의
        self.picStorage['prev'], self.picStorage['curr'] = self.picStorage['curr'], captureName

        '''
            불법 주차 여부 판단 및 ImageList 조절
        '''
        # 불법주차 여부 판단
        judgeResult = cctvImagingProcessor.judgeIllegalParking(self.picStorage)
        # 현재 저장되어 있는 이미지 리스트 길이
        illegalLength = self.illegalityParkingImgList.__len__()
        # 불법 주차가 해제 되었다면
        if judgeResult == 'reset' or judgeResult == 'new':
            # 불법 주차 이미지 리스트 초기화
            self.illegalityParkingImgList.clear()
            if judgeResult == 'new':
                print('신규 불법 주차 감시 시작')
                self.illegalityParkingImgList.append(captureName)
        # 동일 불법 주차가 계속되고 있다면
        elif judgeResult == 'continue' :
            if(illegalLength >= 30):
                print('더이상 해당 차량에 대해서는 불법주차를 감시하지 않음')
                self.hasObserve = False
                return 'end'
            # 불법 주차 리스트에 현재 사진명 추가
            self.illegalityParkingImgList.append(captureName)

        return judgeResult

'''
    Main Start
'''
mainProcessor = MainProcessor('')

# mainProcessor.runScheduler()
# mainProcessor.main()


'''
    Main Test Code
'''
## TEST Interval
## main Test 용
mainProcessor.main()

## Invter val Test 용
# sched = BlockingScheduler()
# sched.add_job(mainProcessor.main, 'interval', seconds=2)
# sched.start()


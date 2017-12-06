from apscheduler.schedulers.blocking import BlockingScheduler
# Customize Module
import requester, soundPlayer, cctvImagingProcessor, config

class MainProcessor() :
    def __init__(self):
        # 이전 사진, 현재 캡쳐 사진을 저장할 변수
        self.picStorage = {'prev':'', 'curr': ''}
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
        hasClearMsgSubmit = self.imageProcessing()
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


       

        info = config.getSocketInfo()
        # print(info, info['host'])

        # Send Image With Socket
        # requester.submitImgWithSocket('aaaa', False, info)

    # Web Server로 현재 cctv processor 상태 값을 전송
    def sendCctvStatus2WebServer(self):
        # 현재 저장되어 있는 이미지 리스트 길이
        illegalLength = self.illegalityParkingImgList.__len__()
        '''
            15분 이상 불법 주차 시 Http GET Protocol 전송
        '''
        webServerInfo = config.getWebServerInfo()
        cctvProcessorInfo = config.getCctvProcessorInfo()

        count = illegalLength   # 현재 불법 주차 count
        cctvId = cctvProcessorInfo['cctvId']

        cctvStatusManagerUrl = webServerInfo['host'] + webServerInfo['cctvStatusManagerUrl']
        imageReceiveManagerUrl = webServerInfo['host'] + webServerInfo['imageReceiveManagerUrl']

        if illegalLength < 15:
            return
        # 불법 주정차 15분에 도달할 경우
        elif illegalLength == 15:
            # TODO 현재 상태 값 전송 GET
            # Requst Http Get
            query = 'cctvId' + cctvId + '&count=' + count + '&img=' + self.illegalityParkingImgList[0]
            result = requester.requestGetHttp(cctvStatusManagerUrl, query)
            # TODO 최초 사진 전송 POST
            result = requester.requestPostHttp(imageReceiveManagerUrl, self.illegalityParkingImgList[0])
        
        # Requst Http Get
        result = requester.requestGetHttp('http://localhost:3333')
        # TODO 현재 사진 전송 POST


    # @return {boolean} True: 불법 주차 해제 전송(to Web Server), False: 변화없음
    def imageProcessing(self):
        '''
            카메라 capture
        '''
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
            if(illegalLength > 14):
                # TODO Web Server로 해제 정보 전송
                print('불법 주차 경보 해제 통보 필요')
            return True
        # 동일 불법 주차가 계속되고 있다면
        elif judgeResult == 'continue' :
            if(illegalLength >= 30):
                print('더이상 해당 차량에 대해서는 불법주차를 감시하지 않음')
                self.hasObserve = False
                return False

            self.illegalityParkingImgList.append(captureName)

        return False

mainProcessor = MainProcessor()

# mainProcessor.runScheduler()
mainProcessor.main()


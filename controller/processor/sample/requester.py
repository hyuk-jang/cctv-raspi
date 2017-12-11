# -*- coding: utf-8 -*- 

import os
import requests
import socket

# CCTV 관련 데이터 Http Get 방식으로 보내고자 할 경우
def requestGetHttp(httpPath, params):

    res = requests.get(httpPath, params = params)

    # print('request query',query)
    # url = httpPath + '?' + query if query != '' else httpPath
    # print('url',url)
    # try:
    #     http = urllib3.PoolManager(retries=False)
    #     r = http.request('GET', url)
    #     return True if r.status == 200 else False
    # except (urllib3.exceptions.NewConnectionError) as e:
    #     print(e)
    #     return False
    # except:
    #     print('default Error')
    #     return False

# Image를 Http Post 방식으로 보내고자 할 경우 
def requestPostHttp(httpPath, fileName):
    print('requestPostHttp', httpPath, fileName)
    url = httpPath + '/' + fileName
    # "http://localhost:3333/image_receiver/t_ta"
    filePath = os.getcwd() + '/image/%s.png' % fileName
    # print('filePath', filePath)
    # headers = {'Content-Type': 'image/jpeg'}
    files ={'image':open(filePath,'rb')}
    r = requests.post(url, files=files)
    return r

'''
# Image 를 Socket을 이용한 전송. 
# Image의 확장자는 png만 사용
# 접속이 종료되면 Server측은 그동안 수신된 Buffer를 합쳐 image 파일로 만들어야함
'''
def submitImgWithSocket(fileName, hasSendAll, socketInfo):
    # HOST = socket.gethostname()
    print('submitImgWithSocket socketInfo\t', socketInfo)
    HOST = socketInfo['host']
    PORT = socketInfo['port']

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[+] Connected with Server")

    # get file name to send
    # TEST Code
    fileName = 'aaaa'
    # TEST Code
    f_send = os.getcwd() + '/image/' + fileName + '.png'
    # open file
    file_name = open(f_send,'rb')

    # 한번에 보내고자 할 경우
    if hasSendAll:
        byteList = b''
        while True:
            line = file_name.readline()
            if not line:
                break
            else:
                byteList += line
        print('byteList', byteList.__len__())
        print("[+] Sending file...")
        client.send(byteList)
    # Image를 readline()을 이용하여 계속하여 전송
    else:
        while True:
            line = file_name.readline()
            if not line:
                break
            else:
                client.send(line)
    
    file_name.close()
    client.close()

    print("[+] Data sent successfully")


if __name__ == '__main__':
    print('Curr requester.py Process ^^^^^^^^^^')
    try:
        import config
        import time

        webServerConfig = config.getWebServerInfo()
        submitObj = {
            'cctv_id': config.getCctvProcessorInfo()['cctvId'],
            'count': '11',
            'img': 'aaaa',
            'measure_date': time.strftime("%Y-%m-%d_%H:%M:%S")
        }
        print (time.strftime("%Y-%m-%d_%H:%M:%S"))
        print('webServerConfig',webServerConfig)
        httpPath = webServerConfig['host'] + webServerConfig['cctvStatusManagerUrl']
        requestGetHttp(httpPath, submitObj)

        httpPath = webServerConfig['host'] + webServerConfig['imageReceiveManagerUrl']
        requestPostHttp(httpPath, 'aaaa')


        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    # except e:
    #     print('occur except', e)
    
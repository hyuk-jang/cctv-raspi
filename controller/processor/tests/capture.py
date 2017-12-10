# -*- coding: utf-8 -*- 

import uuid
import os

from picamera import PiCamera
from time import sleep


# piCamera를 이용하여 영상 캡쳐 (png only)
# @return {string} Capture 한 File 명 
def captureImage():
    filePath = os.getcwd() + '/image/'
    fileName = str(uuid.uuid4())

    camera = PiCamera()
    # camera.rotation = 180
    camera.start_preview()
    # 파이 카메라 조도가 설정되는 시간을 기다려주기 위해 사진을 찍기 전 최소 2초 정도 여유를 두는 것
    sleep(12)
    camera.capture(filePath + fileName + '.png')
    camera.stop_preview()

    return fileName


captureImage()



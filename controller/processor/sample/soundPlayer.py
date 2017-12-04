#-*- coding: utf-8 -*-
# import sys
# # reload(sys)
# sys.setdefaultencoding('utf-8')

from gtts import gTTS
import os

fullPath = os.getcwd() + '/tttt.wav'

tts = gTTS(text='Hello 한글 테스트 뷁 퉷 영 녘  Boy', lang='ko')
tts.save(fullPath)
os.system('tttt.wav')



# from pygame import mixer # Load the required library

# mixer.init()
# mixer.music.load(fullPath)
# mixer.music.play()
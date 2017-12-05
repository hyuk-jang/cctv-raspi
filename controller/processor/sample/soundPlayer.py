#-*- coding: utf-8 -*-

from gtts import gTTS
import os


import platform
print (platform.system(), platform.release())


fullPath = os.getcwd() + '/tttt.mp3'

tts = gTTS(text='Hello 한글 테스트 뷁 퉷 영 녘  Boy', lang='ko')
tts.save(fullPath)
print('fullPath', fullPath)


if platform.system() == 'Windows':
  print('Windows')
  os.system(fullPath)
else:
  os.system("mplayer " + fullPath)
  pass




# mixer.init()
# mixer.music.load(fullPath)
# mixer.music.play()
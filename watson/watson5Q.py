# -*- coding: utf-8 -*-

import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import random
import json
import sys
import requests
from watsonC import Watson
#from PepperStream import PepperModuleClass
import cv2
import threading
import time
#from naoqi import (ALProxy, ALBroker, ALModule)

PEPPER_IP = "192.168.1.2"

class WatsonMain():

    def __init__(self,Wstream):
        self.stop_event = threading.Event() #停止させるかのフラグ
        self.inc_event = threading.Event()  #なんかのフラグ
        #スレッドの作成と開始
        self.Wstream=Wstream
        self.thread = threading.Thread(target = self.target)
        self.thread.setDaemon(True)
        self.thread.start()

    def target(self):
        self.Wstream.run()
        
    def start(self):
        self.Wstream.start()
        
    def send(self,input):
        self.Wstream.send(input, is_binary=True)

    def stop(self):
        """スレッドを停止させる"""
        self.Wstream.stop()
        self.thread.join()    #スレッドが停止するのを待つ


def get_token(watson):
    r = watson.get_token()
    if r.status_code != 200:
        exit(1)
    return r.text

if __name__ == '__main__':
 cam = cv2.VideoCapture(0)
 frame = cam.read()[1]
 url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
 username = 'a750d434-bf0b-427f-a35b-e1c4e73e0f75'
 password = 'BSR0JXMftGa5'
 audio_path="C:\\Anaconda\\work\\audio\\temp.wav"
 CHUNK=2730
 RATE=16000
 FORMAT = pyaudio.paInt16
 CHANNELS=1
 p=pyaudio.PyAudio()
 stream = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 output=True,
                 frames_per_buffer=CHUNK)
 watson = Watson(username, password, url)
 token = get_token(watson)
 Wstream = watson.recognize_stream(token)
 #myBroker = ALBroker("myBroker","0.0.0.0",0,PEPPER_IP,9559)
 #PepperModule = PepperModuleClass("PepperModule")
 #PepperModule.startRecord()
 h = WatsonMain(Wstream)
 time.sleep(3)
 while stream.is_active():
     try:
       frame = cam.read()[1]
       cv2.waitKey(1)
       cv2.imshow("frame",frame)
       input = stream.read(CHUNK)
       #output=PepperModule.inputBuff
       #stream.write(output)
       h.send(input)
       txt,flag =h.Wstream.result()
       if flag==1:
          print txt
          if txt[0:3]==u"チーズ":
            print "test"
            cv2.imwrite("frame.png",frame)
            cv2.imshow("shot",frame)
          #PepperModule.talk(txt)
     except KeyboardInterrupt:
       "終了中"
       break
 h.stop()
 stream.stop_stream()
 stream.close()
 p.terminate()
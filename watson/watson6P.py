# -*- coding: utf-8 -*-

import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import random
import json
import re
import sys
import requests
from watsonC import Watson
from PepperStream import PepperModuleClass
import threading
import time
from naoqi import (ALProxy, ALBroker, ALModule)

PEPPER_IP = "192.168.1.6"

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

    def state(self):
        return self.Wstream.state

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
 myBroker = ALBroker("myBroker","0.0.0.0",0,PEPPER_IP,9559)
 PepperModule = PepperModuleClass("PepperModule")
 PepperModule.startMemory()
 time.sleep(3)
 PepperModule.startRecord()
 output=[]
 h=None
 
 while stream.is_active():
     try:
       #input = stream.read(CHUNK,exception_on_overflow = False)
       
       if PepperModule.RecStatus=="run": #イベントが"runだったら"
         if h is None:
           h = WatsonMain(Wstream)
         if h.state() == "open":
           PepperModule.raiseRecEvent("running") #ここでイベントを”runnig”立てる
         while h.state() == "open":
             output +=PepperModule.inputBuff
             if len(output)>=16000: #buffが溜まっていたら
               output2=np.array(output[:16000])
               del output[:16000]
               stream.write(output2.tostring())
               if PepperModule.RecStatus=="listen": #イベントが"runだったら"
                  h.send(output2.tostring()) #watsonに送信
                  txt,flag =h.Wstream.result()
                  if flag==1:
                    txt=re.sub(" ","",txt)
                    h.stop()
                    h=None
                    print txt
                    PepperModule.raiseRecEvent(txt) #ここでイベントを”recognized”立てる
                    break
               elif PepperModule.RecStatus=="stop": #イベントが"runだったら"
                    h.stop()
                    h=None
                    break
 
 
     except KeyboardInterrupt:
       print "終了中"
       break
 myBroker.shutdown()
 try:
   h.stop()
 except KeyboardInterrupt:
   print "watson failed"
 stream.stop_stream()
 stream.close()
 p.terminate()
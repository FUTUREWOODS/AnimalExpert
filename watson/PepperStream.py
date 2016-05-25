# -*- coding: utf-8 -*-

import time
import json
import websocket
from functools import partial
from websocket._abnf import ABNF
import pyaudio
from naoqi import (ALProxy, ALBroker, ALModule)

class PepperModuleClass(ALModule):
    def __init__(self, name, PEPPER_IP = "192.168.1.6"):
        ALModule.__init__(self, name)
        #
        self.PEPPER_IP=PEPPER_IP
        self.BIND_PYTHON( self.getName(),"callback" );
        self.tts = ALProxy("ALTextToSpeech", PEPPER_IP, 9559)
        self.mem = ALProxy("ALMemory")
        self.tts.setLanguage("Japanese")
        self.inputBuff=[]
        self.status="stop"
        #self.tts.say("腹話術を開始します")
        print "PepperModule Initialyze"
    
    def startRecord(self):
        
        #
        self.pepperMicrophone = ALProxy("ALAudioDevice", self.PEPPER_IP, 9559)
        #
        # 16KHzのモノラル音声でFront(3)マイク１つのみを指定
        self.pepperMicrophone.setClientPreferences(self.getName(), 16000, 3, 0)
        #
        # 録音開始
        self.pepperMicrophone.subscribe(self.getName())
    
    def startMemory(self):
        self.mem.subscribeToEvent("AnimalExpert/RecFlag",self.getName(), "pythondatachanged")
    
    def pythondatachanged(self, key, value, message):
        """callback when data change"""
        print "FLAG: "+value
        self.status=value
    
    def raiseEvent(self,message):
        self.mem.raiseEvent("AnimalExpert/RecFlag",message)
    
    def talk(self,txt):
        print txt
        self.tts.say(txt)
    
    def processRemote(self, inputChannels, inputSamples, timeStamp, inputBuff):
        self.inputBuff.append(inputBuff)
    
    def stop(self):
        # 終了
        self.pepperMicrophone.unsubscribe(self.getName())
        time.sleep(1)
        self.tts.say("腹話術を終了しました")

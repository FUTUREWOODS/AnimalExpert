#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""IBM Watson Developer Cloud ‚Ì Txt to Speach
"""
import os
import sys
import json
import cv2
import pyaudio
import codecs
import requests
from pit import Pit

def Speak(input,stream):
  password="k27g5SgmsVT1"
  username="0c182558-2c2f-4858-8049-b588a31ec31e"
  url = "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"
  voice="ja-JP_EmiVoice"
  #voice="en-US_AllisonVoice"
  accept="audio/wav"
  text=(input).decode('Shift_JIS')

  res = requests.post(
    url, auth=(username,password),
    params={'text': text, 'voice': voice, 'accept': accept}
    )
    
  with open('test.wav', 'wb') as fd:
    for chunk in res.iter_content(1024):
        #fd.write(chunk)
        stream.write(chunk)
    
CHUNK=1024
RATE=22050
p=pyaudio.PyAudio()
stream=p.open(	format = pyaudio.paInt16,
		channels = 1,
		rate = RATE,
		frames_per_buffer = CHUNK,
		output = True) # input‚Æoutput‚ð“¯Žž‚ÉTrue‚É‚·‚é
    
while 1:
    txt=raw_input(' please input > ') 
    Speak(txt,stream)
    

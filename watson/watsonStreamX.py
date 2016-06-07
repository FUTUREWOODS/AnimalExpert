# -*- coding: utf-8 -*-

import time
import json
import websocket
from functools import partial
from websocket._abnf import ABNF

class watsonStream:

   DEFAULT_START_PARAMS = {
        'action': 'start',
        'content-type': 'audio/l16; rate=16000; channels=1',
        'max_alternatives': 10,
        'interim_results': True,
        'continuous': True,
        'timestamps': True
   }
    
   DEFAULT_STOP_PARAMS = {'action': 'stop'}

   def __init__(self, url, start_params={}):
        self.url = url
        self.state = "none"
        self.start_params = dict(self.DEFAULT_START_PARAMS, **start_params)
        self.ws = None
        self.speachtxt="ううん"
        self.confidence=0.1
        self.flag=0

   def run(self, on_message=None, on_error=None, on_close=None, on_open=None, keep_running=True):
        self.ws = websocket.WebSocketApp(self.url,  # header={'Transfer-encoding': 'chunked'},
                                         on_message=self._on_message,
                                         on_error= self._on_error,
                                         on_close= self._on_close,
                                         on_open= self._on_open,
                                         keep_running=keep_running)
        self.ws.run_forever()

   def result(self):
    flag=self.flag
    self.flag=0
    return self.speachtxt,flag

   def stop(self):
    if self.state != "close":
        self.ws.send(json.dumps(self.DEFAULT_STOP_PARAMS))
        time.sleep(3)
        self.ws.close()

   def send(self, data, is_binary=False):
        self.ws.send(data, ABNF.OPCODE_BINARY if is_binary else ABNF.OPCODE_TEXT)

   def _on_message2(self, ws, message):
        d = json.loads(message)
        print d
        words = [[x["transcript"].encode("euc-jp"), x["confidence"]] for x in d["results"][0]["alternatives"]]
        for word in words:
          txt= word[0].decode("euc-jp").encode("utf-8")
          self.speachtxt = txt
          self.flag=1
   
   def _on_message(self, stream, message):
        d = json.loads(message)
        if not d or not d["results"] or len(d["results"]) == 0 or not d["results"][0]["final"]:
            return
        print "Recognishon finished"
        txt=""
        for x in d["results"][0]["alternatives"]:
             txt=txt+","+x["transcript"]
             
        self.speachtxt = txt
        self.flag=1



   def _on_error(self, user_func, ws, error):
        print "error"

   def _on_close(self, ws):
        self.state = "closing"
        self.stop()

   def _on_open(self, ws):
        self.state = "open"
        ws.send(json.dumps(self.start_params))

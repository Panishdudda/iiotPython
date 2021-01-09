import requests as req
import json


def holdMachine(self,):
      HOLD_MACHINE_URL = self.HOLD_MACHINE_URL
      LOCAL_HEADER = self.HEADERS
      try:
            result=req.post(HOLD_MACHINE_URL,json.dumps({"State":"Hold"}),headers=LOCAL_HEADER,timeout=2)
            print("holding machine")                
        #   result=req.post(LIVE_SIGNAL_API,json.dumps({"liveSignal":signal}),headers=LOCAL_HEADER,timeout=2)
        #   print(signal,"live signal send to local server")  
      except Exception as e:
            print(e)
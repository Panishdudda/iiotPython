from package import HOLD_MACHINE_API,LOCAL_HEADER,LIVE_SIGNAL_API
import requests as req
import json


def updateLiveSignal(signal):
      try:
          if(signal=="Alarm ON" or signal=="Machine Idle"):
              result=req.post(HOLD_MACHINE_API,json.dumps({"State":"Hold"}),headers=LOCAL_HEADER,timeout=2)
              print(signal,"holding machine")  
              
          result=req.post(LIVE_SIGNAL_API,json.dumps({"liveSignal":signal}),headers=LOCAL_HEADER,timeout=2)
          print(signal,"live signal send to local server")  
      except Exception as e:
          print(e)
import RPi.GPIO as GPIO
from datetime import datetime
from ._globalVariables import PRODUCTION_ARRAY
from ._signalsFlags import getFlagStatus,setFlagStatus
from ._productionOk import productionOk
from ._saveSignals import insertSignalToLocalDb
from ._liveStatus import updateLiveStatus
from ._globalVariables import LIVE_STATUS_CODES
from ._holdMachine import holdMachine


TEMP_PRODUCTION_ARRAY =  []

def getCurrentSignal(self,InputPin,processOn,processOff):

    flag=int(getFlagStatus(processOn))
    #Read signal from the Raspberry pi 
    SignalStatus=GPIO.input(InputPin)
    #check the time at which this signal is raised
    timeObj = datetime.now()
    timeStamp=timeObj.strftime("%Y/%m/%d %H:%M:%S")

    #machine on conditions
    if(flag == 0 and SignalStatus==1):
        process=processOn
        print(process)
        print(timeStamp)
        setFlagStatus(process,1)
        insertSignalToLocalDb(self,self.machineId,process,timeStamp)
        if process=="alarmON":
            updateLiveStatus(self,LIVE_STATUS_CODES['alarm'],"alarmON","red")
            holdMachine(self,)
        elif process=="machineON":
            updateLiveStatus(self,LIVE_STATUS_CODES['machineIdle'],"MachineIdle","orange")
            holdMachine(self,)
        elif process=="emergencyON":
            updateLiveStatus(self,LIVE_STATUS_CODES['emergency'],"emergencyON","red")
        elif process=="cycleON":
            TEMP_PRODUCTION_ARRAY=[]
            TEMP_PRODUCTION_ARRAY.append(process)
            updateLiveStatus(self,LIVE_STATUS_CODES['cycle'],"cycleON","green")                          
        else:
            pass



    #machine off condition
    if(flag == 1 and SignalStatus == 0):
        process=processOff
        print(process)
        print(timeStamp)
        setFlagStatus(process,0)
        insertSignalToLocalDb(self,self.machineId,process,timeStamp)
        if (process=="emergencyOFF" or process=="cycleOFF" or process=="alarmOFF"):
            updateLiveStatus(self,LIVE_STATUS_CODES['machineIdle'],"machineIdle","orange") 
            holdMachine(self,)
        elif process=="m30OFF":
            TEMP_PRODUCTION_ARRAY.append(process)
        if(PRODUCTION_ARRAY==TEMP_PRODUCTION_ARRAY):
            print("Array matched")
            productionOk(self,)                                                                       
        else:
            pass




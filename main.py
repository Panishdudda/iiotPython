################################################################################################
#######      AUTHOR NAME   : GAUTAM S PATIL FROM LETZZBUILD                              #######       
#######      DATE          : 20-DEC-2020                                                 #######               
#######      TITLE         : IIOT BASED CNC SIGNALS COLLECTION SCRIPT                    #######
#######      WEBADDRESS    : LETZZBUILD.COM                                              #######
#######      CODE VERSION  : 3.0                                                         #######                 
################################################################################################



#BELOW ARE ALL THE SIGNALS MENTIONED ALONG WITH THEIR PIN NUMBERS CONNECTED TO RELAYS
#   MACHINE                     
#   CYCLE          
#   RESET
#   M30
#   ALARM
#   EMERGENCY
#   SPINDLE
#   RUNOUTNOTOK 


#importing required libraries
from datetime import datetime
import os
import RPi.GPIO as GPIO
from package import conn,curs,PRODUCTION_ARRAY,liveStatusCodes,COLOR,SIGNAL_NAME
from package.initilization import getMachineName,getPinNumbers,setSignalPins,liveStatusInitialRow,getMachineType
from package.liveSignal import updateLiveSignal
from package.liveStatus import updateLiveStatus
from package.signalFlags import getFlagStatus,setFlagStatus
from package.initilization import cycleSignalInputPin,machineSignalInputPin,spindleSignalInputPin,resetSignalInputPin,runOutNotOkSignalInputPin,m30SignalInputPin,alarmSignalInputPin,emergencySignalInputPin
from package.saveSignals import insertSignalToLocalDb 
#VARIABLE TO STORE MACHINE NAME
machineId = ""


machineId=getMachineName() #get the machine name 
getPinNumbers() #get the pins stored in local db
setSignalPins() #set the pins as inputs to raspberry pi channel
machineType=getMachineType()
liveStatusInitialRow(machineId,machineType,liveStatusCodes['machineIdle'],COLOR,SIGNAL_NAME) # insert a liveStatus row if doesnot exits


#TEMP PRODUCTION ARRARY STORE LIVE SIGNAL VALUES SO THAT IT CAN BE COMPARED WITH ACTUAL PRODUCTION ARRAY
tempProductionArray=[]


#STORES WHETHER THE PROCESS IS OFF/ON  EX:CYCLEON/CYCLEOFF
process=""



#*****************************MAIN PROGRAM STARTS************************************************
#PROGRAM CONTAINS A CLASS WHICH HAS A CONSTRUCTOR WHICH WILL BE CALLED WHEN AN OBJECT IS CONSTRUCTED
#FOR EVERY SIGNAL 
print("****************************MAIN PROGRAM STARTED*********************************")


class getCurrentStatus:


   #Constructor that will be called when an object is created
   def __init__(self,InputPin,processOn,processOff):
   
         global machineId,conn,PRODUCTION_ARRAY,tempProductionArray
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
             insertSignalToLocalDb(machineId,process,timeStamp)

             if process=="alarmON":
                 updateLiveSignal("Alarm ON")
                 updateLiveStatus(liveStatusCodes['alarm'],"alarmON","red")
             elif process=="machineON":
                 updateLiveSignal("Machine Idle")
                 updateLiveStatus(liveStatusCodes['machineIdle'],"MachineIdle","orange")
             elif process=="emergencyON":
                 updateLiveSignal("Emergency ON")
                 updateLiveStatus(liveStatusCodes['emergency'],"emergencyON","red")
             elif process=="cycleON":
                 print("temperary production array status {}".format(tempProductionArray))
                 tempProductionArray=[] 
                 tempProductionArray.append(process)
                 updateLiveSignal("Cycle ON")
                 updateLiveStatus(liveStatusCodes['cycle'],"cycleON","green")                          
             else:
                 pass



         #machine off condition
         if(flag == 1 and SignalStatus == 0):
             process=processOff
             print(process)
             print(timeStamp)
             setFlagStatus(process,0)
             insertSignalToLocalDb(machineId,process,timeStamp)

             if (process=="emergencyOFF" or process=="cycleOFF" or process=="alarmOFF"):
                  updateLiveSignal("Machine Idle")
                  updateLiveStatus(liveStatusCodes['machineIdle'],"machineIdle","orange") 
             elif process=="m30OFF":
                  tempProductionArray.append(process)
                  if(PRODUCTION_ARRAY==tempProductionArray):
                      print("Array matched")
                      self.ProductionOk()                                                                       
             else:
                  pass


   def ProductionOk():
      data=curs.execute("SELECT MAX(id) FROM production")
      lastId=curs.fetchone()[0]
      sql="update production set status=? where id=?"
      values=("1",lastId)
      try:
          result=curs.execute(sql,values)
          conn.commit()
          print("updated status  1 to last production job ")
      except:   
          print("failed to update status  1 to last production job") 



if __name__ == "__main__":
      
    while(True):
           #object for cycle on/off signal
           getCurrentStatus(cycleSignalInputPin,"cycleON","cycleOFF")

           #object for machine on/off signal
           getCurrentStatus(machineSignalInputPin,"machineON","machineOFF")

           #object for m30 on/off signal
           getCurrentStatus(m30SignalInputPin,"m30ON","m30OFF")

           #object for spindle on/off signal
           getCurrentStatus(spindleSignalInputPin,"spindleON","spindleOFF")

           #object for reset on/off signal
           getCurrentStatus(resetSignalInputPin,"resetON","resetOFF")

           #object for emergency on/off signal
           getCurrentStatus(emergencySignalInputPin,"emergencyON","emergencyOFF")


           #object for alarm on/off signal
           getCurrentStatus(alarmSignalInputPin,"alarmON","alarmOFF")

           #object for runOutNotOk on/off signal
           getCurrentStatus(runOutNotOkSignalInputPin,"runoutNotOkON","runoutNotOkOFF")
                    








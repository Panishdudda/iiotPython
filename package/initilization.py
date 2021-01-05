################################################################################################
#######      AUTHOR NAME   : GAUTAM S PATIL FROM LETZZBUILD                              #######       
#######      DATE          : 20-DEC-2020                                                 #######               
#######      TITLE         : INITILIZATION OF ALL DATBASES                               #######
#######      WEBADDRESS    : LETZZBUILD.COM                                              #######
#######      CODE VERSION  : 3.0                                                         #######                 
################################################################################################



from package import conn,curs
import sqlite3 as sqlite
import RPi.GPIO as GPIO
from package import cycleSignalInputPin,machineSignalInputPin,spindleSignalInputPin,resetSignalInputPin,runOutNotOkSignalInputPin,m30SignalInputPin,alarmSignalInputPin,emergencySignalInputPin






#GETTTING ALL THE ACTUAL PIN NUMBERS FROM DATABASE 
def getPinNumbers(): 
   curs.execute("SELECT * FROM pinout")
   for row in curs.fetchall():
      if(row[2]=="machine"):
          machineSignalInputPin=int(row[3])  
      elif(row[2]=="cycle"):
          cycleSignalInputPin=int(row[3])
      elif(row[2]=="alarm"):
          alarmSignalInputPin=int(row[3])
      elif(row[2]=="emergency"):
          emergencySignalInputPin=int(row[3])
      elif(row[2]=="reset"):
          resetSignalInputPin=int(row[3])
      elif(row[2]=="m30"):
          m30SignalInputPin=int(row[3])
      elif(row[2]=="runoutnotok"):
          runOutNotOkSignalInputPin=int(row[3])
      else:
          pass








#GET THE MACHINE NAME FROM THE LOCAL DATABASE
def getMachineName():
   curs.execute("select * from other_settings")
   machineId=curs.fetchone()[1]
   print("machine Id set as = {}".format(machineId))  
   return machineId

#GET THE MACHINE TYPE FROM THE LOCAL DATABASE
def getMachineType():
   curs.execute("select * from other_settings")
   machineType=curs.fetchone()[7]
   print("machine Id set as = {}".format(machineType))  
   return machineType 



#for the first time the device is installed check if live status table is empty 
# if empty then insert a row with machine idle.
def liveStatusInitialRow(machineId,machineType,status,color,signalName):
    try:
       result=curs.execute("select count(*) from live_status ")
       print(curs.fetchall())
       if result!=1:
           query="insert into live_status(machineId,machineType,status,color,signalName)values(?,?,?,?,?)"
           values=(machineId,machineType,status,color,signalName)
           curs.execute(query,values)
           conn.commit()
           print("live Status is set for the initial time")
       else:
           print("already the row exists")
    except Exception as e:
       print(e,"failed to insert to liveStatus for the initial time")



#SETTING THE GPIO PINS OF RASPBERRY PI AND THE PINMODE
def setSignalPins():
    print("Initilizing the gpio pins of raspberry pi .....")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(machineSignalInputPin,GPIO.IN)
    GPIO.setup(cycleSignalInputPin,GPIO.IN)
    GPIO.setup(m30SignalInputPin,GPIO.IN)
    GPIO.setup(emergencySignalInputPin,GPIO.IN)
    GPIO.setup(resetSignalInputPin,GPIO.IN)
    GPIO.setup(alarmSignalInputPin,GPIO.IN)
    GPIO.setup(runOutNotOkSignalInputPin,GPIO.IN)
    GPIO.setup(spindleSignalInputPin,GPIO.IN)

    #setting warnings false 
    GPIO.setwarnings(False)


import sqlite3 as sqlite


DATABASE_NAME =  'erp.db'
DATABASE_PATH =  ''
HOLD_MACHINE_API = "http://127.0.0.1:5002/HoldMachine"
LIVE_SIGNAL_API =  "http://127.0.0.1:5002/liveSignals"
LOCAL_HEADER = {'Content-type': 'application/json', 'Accept': 'application/json'}
#PRODUCION ARRAY TO MATCH TO CHECK IF PRODUCTION HAS COMPLETED SUCESSFULLY
PRODUCTION_ARRAY=["cycleON","m30OFF"]

#INITIAL CONDITIONS OF MACHINE
SIGNAL_NAME = "Machine Idle"
COLOR = 'orange'

#DICTONARY WHICH STORES THE DEFAULT STATUS VALUES FOR EVERY LIVE STATUS SIGNAL
liveStatusCodes =  {
    "machineIdle" : 0,
    "cycle" : 2,
    "emergency" : 3,
    "alarm" : 4
       }

#variables which hold pin numbers of raspberry pi to collecct signals
spindleSignalInputPin = 7 
runOutNotOkSignalInputPin = 8
m30SignalInputPin = 9
resetSignalInputPin =  10
emergencySignalInputPin = 11
alarmSignalInputPin  = 12 
cycleSignalInputPin  = 13
machineSignalInputPin = 14


#global FLAG VARIABLES WHICH KEEPS A TRACK OF STATUS OF THE EVERY SIGNAL , WHETHER THE SIGNAL IS ON OR OFF
#FLAG = 0  SIGNAL IS OFF 
#FLAG = 1 SIGNAL IS ON
cycleflag=0
spindleflag=0
resetflag=0
emergencyflag=0
alarmflag=0
runoutnotokflag=0
machineflag=0
m30flag=0


#MAKE THE CONNECTION WITH THE LOCAL DATABASE
conn=sqlite.connect(DATABASE_NAME)
curs=conn.cursor()
print("connection done successfully")



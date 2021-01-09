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

def getFlagStatus(process):
          if(process=="cycleON" or process=="cycleOFF"):
              return cycleflag
          elif(process=="spindleON" or process=="spindleOFF"):
              return spindleflag
          elif(process=="machineON" or process=="machineOFF"):
              return machineflag
          elif(process=="m30ON" or process=="m30OFF"):
              return m30flag
          elif(process=="resetON" or process=="resetOFF"):
              return resetflag
          elif(process=="emergencyON" or process=="emergencyOFF"):
              return emergencyflag
          elif(process=="alarmON" or process=="alarmOFF"):
              return alarmflag
          else:
              return  runoutnotokflag


def setFlagStatus(process,flag):
          if(process=="cycleON" or process=="cycleOFF"):
              cycleflag=flag
              return cycleflag
          elif(process=="spindleON" or process=="spindleOFF"):
              spindleflag=flag
              return spindleflag
          elif(process=="machineON" or process=="machineOFF"):
              machineflag=flag
              return machineflag
          elif(process=="m30ON" or process=="m30OFF"):
              m30flag=flag     
              return m30flag
          elif(process=="resetON" or process=="resetOFF"):
              resetflag=flag     
              return resetflag
          elif(process=="emergencyON" or process=="emergencyOFF"):
              emergencyflag=flag     
              return emergencyflag
          elif(process=="alarmON" or process=="alarmOFF"):
              alarmflag=flag     
              return alarmflag
          else:
              runoutnotokflag=flag
              return  runoutnotokflag  
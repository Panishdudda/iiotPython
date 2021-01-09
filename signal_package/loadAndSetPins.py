#GETTTING ALL THE ACTUAL PIN NUMBERS FROM DATABASE
import RPi.GPIO as GPIO


def getAndSetupPins(self):
   conn=self.connection
   curs=self.cursor
   print("FETCHING THE PINS AND SIGNAL NAMES FROM THE DATABASE.....")  
   curs.execute("SELECT * FROM pinout")
   for row in curs.fetchall():
      if(row[2]=="machine"):
          self.machineSignalInputPin=row[3] 
      elif(row[2]=="cycle"):
          self.cycleSignalInputPin=row[3]
      elif(row[2]=="alarm"):
          self.alarmSignalInputPin=row[3]
      elif(row[2]=="emergency"):
          self.emergencySignalInputPin=row[3]
      elif(row[2]=="reset"):
          self.resetSignalInputPin=row[3]
      elif(row[2]=="m30"):
          self.m30SignalInputPin=row[3]
      elif(row[2]=="runoutnotok"):
          self.runOutNotOkSignalInputPin=row[3]
      elif(row[2]=="spindle"):
          self.spindleSignalInputPin=row[3]   

   print("Initilizing the gpio pins of raspberry pi .....")
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(self.machineSignalInputPin,GPIO.IN)
   GPIO.setup(self.cycleSignalInputPin,GPIO.IN)
   GPIO.setup(self.m30SignalInputPin,GPIO.IN)
   GPIO.setup(self.emergencySignalInputPin,GPIO.IN)
   GPIO.setup(self.resetSignalInputPin,GPIO.IN)
   GPIO.setup(self.alarmSignalInputPin,GPIO.IN)
   GPIO.setup(self.runOutNotOkSignalInputPin,GPIO.IN)
   GPIO.setup(self.spindleSignalInputPin,GPIO.IN)
   #setting gpio set warnings false 
   GPIO.setwarnings(False)


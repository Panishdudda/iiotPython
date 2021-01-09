
#for the first time the device is installed check if live status table is empty 
# if empty then insert a row with machine idle.
from ._globalVariables import LIVE_STATUS_CODES


def initialDBSetup(self,):
   conn=self.connection
   curs=self.cursor
   machineId=self.machineId
   try:
      curs.execute("select * from live_status")
      result=curs.fetchone()[0]
      if result!=1:
         query="insert into live_status(machineId,machineType,status,color,signalName)values(?,?,?,?,?)"
         values=(machineId,"Automatic",LIVE_STATUS_CODES['machineIdle'],"orange","alarmON")
         curs.execute(query,values)
         conn.commit()
         print("live Status is set for the initial time")
      else:
        print("already the row exists")
   except Exception as e:
        print(e,"failed to insert to liveStatus for the initial time")


   


def insertSignalToLocalDb(self,machineId,process,timeStamp):
 
      
      sql="INSERT INTO signals(machineId,process,timeStamp) VALUES(?,?,?)"               
      values=(machineId,process,timeStamp)
      try:
          if(self.cursor.execute(sql,values)):
              self.connection.commit()
              print("successfully inserted into local database")
      except:
          print("unable to insert into local database")
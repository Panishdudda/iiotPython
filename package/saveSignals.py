from package import curs,conn

def insertSignalToLocalDb(machineId,process,timeStamp):
      sql="INSERT INTO signals(machineId,process,timeStamp) VALUES(?,?,?)"               
      values=(machineId,process,timeStamp)
      try:
          if(curs.execute(sql,values)):
              conn.commit()
              print("successfully inserted into local database")
      except:
          print("unable to insert into local database")
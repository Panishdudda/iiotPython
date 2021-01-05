from package import curs,conn

def updateLiveStatus(status,signal,color):
      try:
         query = "update live_status set status=?,signalName=?,color=? where id=?" 
         values = (status,signal,color,1) 
         curs.execute(query,values) 
         conn.commit()
         print("live status machine idle updated")  
      except Exception as e:
        print("failed to update live status")          
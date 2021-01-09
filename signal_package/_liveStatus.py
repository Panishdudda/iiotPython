
def updateLiveStatus(self,status,signal,color):
      try:
         query = "update live_status set status=?,signalName=?,color=? where id=?" 
         values = (status,signal,color,1) 
         self.cursor.execute(query,values) 
         self.connection.commit()
         print("live status machine idle updated")  
      except Exception as e:
        print("failed to update live status")          
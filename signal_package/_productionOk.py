def productionOk(self,):
      data=self.cursor.execute("SELECT MAX(id) FROM production")
      lastId=self.cursor.fetchone()[0]
      sql="update production set status=? where id=?"
      values=("1",lastId)
      try:
          result=self.cursor.execute(sql,values)
          self.connection.commit()
          print("updated status  1 to last production job ")
      except:   
          print("failed to update status  1 to last production job")
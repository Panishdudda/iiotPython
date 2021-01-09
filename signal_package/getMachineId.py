
#GET THE MACHINE NAME FROM THE LOCAL DATABASE
def loadMachineNameFromDB(self,):
   conn=self.connection
   curs=self.cursor
   curs.execute("select * from other_settings")
   self.machineId=curs.fetchone()[1]
   print("machine Id set as = {}".format(self.machineId))  
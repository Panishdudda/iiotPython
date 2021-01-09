from ._dbConnection import databaseConnection

def configure(self,databaseName,headers,holdMachineUrl):
    self.DATABASE_NAME = databaseName
    self.HEADERS =  headers
    self.HOLD_MACHINE_URL = holdMachineUrl

    #make the database connection 
    CONNECTION,CURSOR = databaseConnection(self.DATABASE_NAME)
    self.connection = CONNECTION
    self.cursor = CURSOR
    print("Configuration done successfully.....")

    

    
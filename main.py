#import the library which reads all the cnc machine signals and stores in local database.

from signal_package import cncSignalsTracker
import os

base_dir = os.path.dirname(__file__)

#create a cncSignalsTracker object
cnc = cncSignalsTracker()

#pass the configuration paramters 
cnc.configure(
    databaseName=os.path.join(base_dir,'erp.db'),
    headers = {'Content-type': 'application/json'},
    holdMachineUrl = "http://127.0.0.1:5002/HoldMachine"
)

#get all pin numbers from local db and assign it to raspberry pi
cnc.getAndSetupPins()
#gets the machineName from local database 
cnc.loadMachineNameFromDB()
#does all the initial DBBase setup activities
cnc.initialDBSetup()

#starts the process of collecting signals from cnc machine
cnc.start()
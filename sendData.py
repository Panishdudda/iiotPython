#*********This script is used to send all the IIOT data from device to server**************************



#importing of required libraries
from time import sleep 
import sqlite3 
import requests as req
from datetime import datetime


#making a connection with the database
conn2=sqlite3.connect('erp.db')

#create a cursor object to exceute all sql queries
curs2=conn2.cursor()





#Function which sends AlarmInfo  data
#parameters :  endpoint - at which endpoint to send the data
#no return type for the fucntion
def SendAlarmData(endpoint):
   print("****************SENDING ALARM DATA********************")
   try:
             curs2.execute("select * from alarm ")
             data=curs2.fetchall()
             if data is not None:    
               for row in data:
                 Id=row[0]
                 machineId=row[1]
                 operatorName=row[2]
                 jobId=row[3]
                 shift=row[4]
                 component=row[5]
                 modelName=row[6]
                 operation=row[7]
                 timeStamp=row[8]
                 reason=row[9]
                 data={
                       "ID":Id,
                       "MachineID":machineId,
                       "OperatorName":operatorName,
                       "JobID":jobId,
                       "Shift":shift,
                       "Component":component,
                       "ModelName":modelName,
                       "Operation":operation,
                       "TimeStamp":timeStamp,
                       "Reason":reason

                    }
                 response=req.post(endpoint,data=data,timeout=2)
                 if(response.status_code>=200 and response.status_code<=206):
                         curs2.execute("delete from alarm where id=(?)",(Id,))
                         conn2.commit()
                         print("{} entry send to server and deleted from local database ").format(Id)
                 else:
                    print(response.status_code) 
                    print("didnot get good response from server") 
                    return        
                            
             else:
                print("no data to send ...")
   except Exception as e:
              print("Exception occured : ",e)
              return




          

#Function which sends liveStatus data
#parameters :  endpoint - at which endpoint to send the data
#no return type for the fucntion
def SendLiveStatus(endpoint):                    
         print("****************SENDING LIVE SIGNALS DATA********************")
         try:
           curs2.execute("select * from live_status")
           data=curs2.fetchone()
           if data is not None: 
             Id=str(data[0])
             machineId=data[1]
             machineType=data[2]
             status=str(data[3])
             signalColor=data[4]
             signalName=data[5]
             response=req.post(endpoint+"?ID="+Id+"&MachineID="+machineId+"&MachineType="+machineType+"&Status="+status+"&SignalName="+signalName+"&SignalColor="+signalColor,timeout=2)
             if(response.status_code>=200 and response.status_code<=206):
                    print("Current Live Status : {}".format(signalName))
                    print(" Live Status data successfully sent ")
             else:
                 print("didnot get good response from server")
                 return             
           else:
               print("no data to send....")
         except Exception as e:
              print("Exception occured : ",e)
              return






#Function which sends production data
#parameters :  endpoint - at which endpoint to send the data
#no return type for the fucntion
def SendProductionData(endpoint):
   print("********************SENDING PRODUCTION DATA****************************")
   try:
           curs2.execute("select * from production")
           data=curs2.fetchall()
           if data is not None:
             for row in data:
                Id=str(row[0])
                machineId=row[11]
                operatorName=row[1]
                jobId=row[2]
                shift=row[3]
                component=row[4]
                modelName=row[5]
                operation=row[6]
                cycleTime=row[7]
                inspectionStatus=row[8]
                status=row[9]
                timeStamp=datetime.strptime(row[10], '%Y/%m/%d %H:%M:%S') 
                data={
                           "ID" :Id,
                           "MachineID":machineId,
                           "Operation":operation,
                           "OperatorName":operatorName,
                           "JobID":jobId,
                           "ModelName":modelName,
                           "Component":component,
                           "CycleTime":float(cycleTime),
                           "TimeStamp":timeStamp,
                           "Status":bool(status),
                           "Shift":shift,
                           "InspectionStatus":inspectionStatus
                        }
                response=req.post(endpoint,timeout=2,data=data)
                if(response.status_code>=200 and response.status_code<=206):
                        curs2.execute("delete from production where id=(?)",(Id,))
                        conn2.commit()
                        print("{} entry sent to server and  deleted from local database..".format(Id))    
                else:
                      print("didnot get good response from server")
                      return        
           else:
               print("no data to send ...")
   except Exception as e:
            print("Exception occured : ",e)
            return
 




#continously run the loop to send data to server every 2 seconds 
while(1):

    #Function call of 'SendLiveStatus' Function
    SendLiveStatus("http://182.75.179.210/be/api/iiot/PostMachineStatus")

    #Function call of 'SendProductionData' Function
    SendProductionData("http://182.75.179.210/be/api/iiot/Production")

    #Function call of 'SendAlarmData' Function
    SendAlarmData("http://182.75.179.210/be/api/iiot/AlarmInfo")
    
    #wait for 2 seconds 
    sleep(2)
        
                              







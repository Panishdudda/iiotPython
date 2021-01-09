
from flask import Flask,request,jsonify

from flask import render_template,redirect,url_for,session

from flask_sqlalchemy import SQLAlchemy

import os

from sqlalchemy import exc,cast,Date,func,and_

from werkzeug.utils import secure_filename

import requests as req

import json

from datetime import datetime,timedelta

from datetime import time as t

import RPi.GPIO as GPIO

import zipfile,shutil

from io import StringIO

from flask_cors import CORS, cross_origin



holdingPin = 7
holdingStatus = ""
GPIO.setmode(GPIO.BCM)
GPIO.setup(holdingPin,GPIO.OUT)




liveSignal="Machine Idle"



app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'erp.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



db=SQLAlchemy(app)



class signals(db.Model):
      id=db.Column(db.INT,primary_key=True)

      machineId=db.Column(db.String)

      process=db.Column(db.String)

      timeStamp=db.Column(db.String)


class pinout(db.Model):

      id=db.Column(db.INTEGER,primary_key=True)

      signalName=db.Column(db.String)

      pinNumber=db.Column(db.INTEGER)

      status=db.Column(db.String)



     



class production(db.Model):

      id=db.Column(db.INTEGER,primary_key=True)

      operatorName=db.Column(db.String)

      jobId=db.Column(db.String)

      shift=db.Column(db.String)

      component=db.Column(db.String)

      modelName=db.Column(db.String)

      operation=db.Column(db.String)

      cycleTime=db.Column(db.String)

      inspectionStatus=db.Column(db.INTEGER)

      status=db.Column(db.INTEGER)

      timeStamp=db.Column(db.String)

      machineId=db.Column(db.String)

      date=db.Column(db.String)

class liveStatus(db.Model):
      id=db.Column(db.INT,primary_key=True)
      machineId=db.Column(db.String)
      machineType=db.Column(db.String)
      status=db.Column(db.String)
      color=db.Column(db.String)
      signalName=db.Column(db.String)


     

class ShiftData(db.Model):

      id=db.Column(db.INTEGER,primary_key=True)

      shift=db.Column(db.String)

      fromTime=db.Column(db.String)

      toTime=db.Column(db.String)

     



class alarm(db.Model):

      id=db.Column(db.INTEGER,primary_key=True)

      machineId=db.Column(db.String)

      operatorName=db.Column(db.String)

      jobId=db.Column(db.String)

      shift=db.Column(db.String)

      component=db.Column(db.String)

      modelName=db.Column(db.String)

      operation=db.Column(db.String)

      timeStamp=db.Column(db.String)

      reason=db.Column(db.String)


class idleTimeout(db.Model):

      id=db.Column(db.INTEGER,primary_key=True)

      machineId=db.Column(db.String)

      operatorName=db.Column(db.String)

      shift=db.Column(db.String)

      component=db.Column(db.String)

      modelName=db.Column(db.String)

      operation=db.Column(db.String)

      timeStamp=db.Column(db.String)

      reason=db.Column(db.String)



class energyMeter(db.Model):

      id=db.Column(db.INTEGER,primary_key=True)

      voltage1=db.Column(db.String)

      voltage2=db.Column(db.String)

      voltage3=db.Column(db.String)

      voltage1=db.Column(db.String)

      current1=db.Column(db.String)

      current2=db.Column(db.String)

      current3=db.Column(db.String)

      power=db.Column(db.String)

      energy=db.Column(db.String)

class serverConf(db.Model):
   id=db.Column(db.INT,primary_key=True)
   endpoint=db.Column(db.String)
  

class networkConf(db.Model):
      id=db.Column(db.INT,primary_key=True)
      ip=db.Column(db.String)
      gateway=db.Column(db.String) 
      dns=db.Column(db.String)


class otherSettings(db.Model):
      id=db.Column(db.INT,primary_key=True)
      machineId=db.Column(db.String)
      batchSize=db.Column(db.String)
      holdingRelay=db.Column(db.String)
      machineBypass=db.Column(db.String)
      cleaningInterval=db.Column(db.String)
      idleTimeout=db.Column(db.String)
      machineType=db.Column(db.String)  




#get the holding pin number and status
try : 
    result=otherSettings.query.get(1)
    holdingPin=int(result.holdingRelay)
    holdingStatus=result.machineBypass
    print(holdingPin)
    print(holdingStatus)
except Exception as e:
   print(e,"error getting status of holding ")
   holdingPin=7
   holdingStatus="ByPass Machine" 





@app.route('/login', methods=['GET', 'POST'])

def login():

   machineId=request.get_json()['machineId']
   username=request.get_json()['username']
   password=request.get_json()['password']

   resultData={}
   #calculate the current shift
   TimeObj=datetime.now().time()

   print("Current Time :" + str(TimeObj))

   query=db.session.query(ShiftData).filter(and_(func.time(ShiftData.fromTime)<=TimeObj,func.time(ShiftData.toTime)>=TimeObj)) 

   for row in query.all():  
     if(row.id==1):
            print("Shift 1")
            resultData['Shift']=row.shift 
            
     elif(row.id==2):

         print("Shift 2")

         resultData['Shift']=row.shift 

     elif(row.id==3):

         print("Shift 3")

         resultData['Shift']=row.shift                         

     else: 

         pass


   #check for admin user 
   if(username=="admin" and password=="IIotAdmin"):
      return jsonify({"result": {"status":1,"admin":True,"message":"success"}})   


   #check for a valid user or no       
   loginUrl="http://182.75.179.210/be/api/iiot/Login"
   headers = {'Content-type': 'application/json'}  
   try:

         res=req.post(loginUrl,headers=headers,data=json.dumps({"UserID":username,"Password":password,"MachineCode":machineId}),timeout=4)     

         componentList=[]

         modelList=[]

         data=res.json() 
         print(data)

         if(data['Error']!=None):

              print("error")    

              return jsonify({"result": {"status":0,"admin":False,"message":"invalid username or password"}}) 

         else:

              resultData['FullName']=data['FullName']

              data1=data['Components']

              data2=data['ProductModels']

              #print(data2)

              for datas in data1:

                 componentList.append(datas['Code'])

              for datas in data2:

                 modelObj={}

                 modelObj['code']=datas['Code']

                 modelObj['value']=datas['Value']   

                 modelList.append(modelObj)       

              

              resultData['Components']=componentList

              resultData['Models']=modelList
              print(resultData);
              return jsonify({"result": {"status":1,"admin":False,"message":"success","data":resultData}})

       

   except Exception as e:
         
         print("error while connecting to server for login details",e)

         return jsonify({"result": {"status":0,"admin":False,"message":"Something Went Wrong, Check Network Connection"}})

             

       

                          

      
   

@app.route('/', methods=['GET', 'POST'])
def loadScreen():
   #save shift data to databse
   try:
     url="http://182.75.179.210/be/api/iiot/ShiftList"      
     res=req.get(url,timeout=2)
     datas=res.json()
     for data in datas: 
       idNew=data['ID']
       shiftNew=data['Name']
       fromTimeNew=data['FromTime']
       toTimeNew=data['ToTime']
       fromTimeNew=datetime.strptime(fromTimeNew,"%Y-%m-%dT%H:%M:%S")
       toTimeNew=datetime.strptime(toTimeNew,"%Y-%m-%dT%H:%M:%S")
       shiftObj=ShiftData(id=idNew,shift=shiftNew,fromTime=fromTimeNew,toTime=toTimeNew)
       try:
          result=ShiftData.query.filter_by(id=idNew).scalar() 
          if(result!=None):
              pass
          else:    
            db.session.add(shiftObj)
            db.session.commit() 
            print("added shift data to datbase") 
       except exc.IntegrityError:
           db.session.rollback()        
   except:
        print("something went wrong while getting shift data...." )

   #response data will be stored in this variable
   data={}
   #fetch all the reasons for the alarm signal from server
   # try:
   #   url="http://127.0.0.1:5001/BE/api/iiot/GetAlarmReasonsList"      
   #   res=req.get(url,timeout=2)
   #   datas=res.json()
   #   print(datas)
   #   result=alarmReasons.query.get(id=1)
   #   if(result!=None):
   #      for data in datas:
   #         reasonsObj=alarmReasons(reasons=data['Reasons'])
   #         db.session.add(reasonsObj)
   #         db.session.commit()

   # except Exception as e:
   #    print("something went wrong with alarm reasons",e)     



        
   #load all the other settings data like machineId,idleTimeout from local db to store in session variable     
  
   try:
      result=otherSettings.query.get(1)
      if(result!=None):
         data['machineId']=result.machineId
         data['idleTimeout'] = result.idleTimeout
         data['batchSize']= result.batchSize
         holdingPin = result.holdingRelay
      else:
         print("no other settings data in database")

      return jsonify({"result": {"message":"success","status":1,"data":data}})      

   except Exception as e:
      return jsonify({"result": {"messgae":"something went wrong","status":0,"data":{}}})





@app.route("/operator", methods=["GET", "POST"])

def operatorScreen():

    global liveSignal

    result=request.get_json()

    shift=result['shift']

    username=result['fullName']

    component=result['componentName']

    model=result['modelName']

    operation=result['operationName']  

    machineId=result['machineId']

    jobId=result['jobId']
    #calculate the current shift

    TimeObj=datetime.now().time()

   #  print("Current Time :" + str(TimeObj))

    query=db.session.query(ShiftData).filter(and_(func.time(ShiftData.fromTime)<=TimeObj,func.time(ShiftData.toTime)>=TimeObj)) 

    for row in query.all():

         # print("resulted rows : ")     

         if(row.id==4 or row.id==5):

            pass

         elif(row.id==1):

            print("Shift 1")

            nowShift=row.shift 

         elif(row.id==2):

           print("Shift 2")

           nowShift=row.shift 

         elif(row.id==3):

           print("Shidt 3")

           nowShift=row.shift                         

         else: 

           nowShift="Second" 

           




    timeObj = datetime.now()
    time=timeObj.strftime("%Y/%m/%d %H:%M:%S")
    CurrentDate=datetime.now().date()
    CurrentTime=datetime.now().time()
    sihTime=t(6, 59,59)

    if(CurrentTime<=sihTime):

          date=CurrentDate-timedelta(1)

    else:

          date=CurrentDate



    presentDate=date.strftime("%Y-%m-%d")


    productionObj=production(operatorName=username,jobId=jobId,shift=shift,component=component,modelName=model,operation=operation,cycleTime="5.5",inspectionStatus="0",status="0",timeStamp=time,machineId=machineId,date=presentDate)

    try:
              db.session.add(productionObj)

              db.session.commit()

              print("inserting into databse")

    except Exception as e:

          print(e)


    try:

         # print("releasing machine")

         releaseUrl="http://127.0.0.1:5002/HoldMachine"

         headers = {'Content-type': 'application/json'}


         res=req.post(releaseUrl,headers=headers,data=json.dumps({"State":"Release"}),timeout=2)
         
         return jsonify({"result": {"status":1,"message":"job Status Ok , proceed to cycle ","data":{"shift":nowShift}}})


    except :

         return jsonify({"result": {"status":0,"message":"something went wrong please fill details once more","data":{}}})





@app.route('/shutdown', methods=['GET', 'POST'])

def shutdown():

   print("shutting down")   

   os.system("sudo shutdown -h now ") 

   return("",204)





@app.route('/HoldMachine', methods=['POST'])

def hold_machine():

    data=request.get_json()

    state=data['State']

    if(holdingStatus=="Hold Machine"):
      if(state=='Hold'):
         # holding the machine
          print("holding machine....")
          GPIO.output(holdingPin,False)
          

        

      elif(state=='Release'):
            # holding the machine
            print("releasing machine....")
            GPIO.output(holdingPin,True)
         

      else:

          pass 
    else:

         if(state=='Hold'):
           # holding the machine
            print("holding machine....")
           

        

         elif(state=='Release'):
            # holding the machine
            print("releasing machine....")   
            

         else:

            pass          

    return ("",204)

  
       


@app.route('/alarmScreen', methods=['GET','POST'])

def alarmScreen():

    result=request.get_json()

    shift=result['shift']

    username=result['fullName']

    component=result['componentName']

    model=result['modelName']

    operation=result['operationName']  

    machineId=result['machineId']
    
    reason=result['alarmReason']

    if result['jobId'] != "":

       jobId=result['jobId']

    else:
       jobId="No Job Placed"

    

    

    timeObj = datetime.now()

    time=timeObj.strftime("%Y/%m/%d %H:%M:%S")



    alarmObj=alarm(operatorName=username,jobId=jobId,shift=shift,component=component,modelName=model,operation=operation,timeStamp=time,machineId=machineId,reason=reason) 

    try:

           db.session.add(alarmObj)

           db.session.commit()

           print("inserting into database")

    except Exception as e:

           print(e)   

           db.session.rollback()
           return jsonify({"result": {"status":0,"message":"something went wrong"}})



    releaseUrl="http://127.0.0.1:5002/HoldMachine"

    headers = {'Content-type': 'application/json'}

    try:

          res=req.post(releaseUrl,headers=headers,data=json.dumps({"State":"Release"}),timeout=2)

          print(res.status_code)

    except:

           print("error..")  
           return jsonify({"result": {"status":0,"message":"something went wrong"}})   



    return jsonify({"result": {"status":1,"message":"successfully data saved"}})




@app.route('/idleTimeout', methods=['GET','POST'])

def IdleTimeout():

    result=request.get_json()

    shift=result['shift']

    username=result['fullName']

    component=result['componentName']

    model=result['modelName']

    operation=result['operationName']  

    machineId=result['machineId']
    
    reason=result['idleReason']

    timeObj = datetime.now()

    time=timeObj.strftime("%Y/%m/%d %H:%M:%S")



    idleTimeoutObj=idleTimeout(operatorName=username,shift=shift,component=component,modelName=model,operation=operation,timeStamp=time,machineId=machineId,reason=reason) 

    try:

           db.session.add(idleTimeoutObj)

           db.session.commit()

           print("inserting into database")

    except Exception as e:

           print(e)   

           db.session.rollback()
           return jsonify({"result": {"status":0,"message":"something went wrong"}})



    releaseUrl="http://127.0.0.1:5002/HoldMachine"

    headers = {'Content-type': 'application/json'}

    try:

          res=req.post(releaseUrl,headers=headers,data=json.dumps({"State":"Release"}),timeout=2)

          print(res.status_code)

    except:

           print("error..")  
           return jsonify({"result": {"status":0,"message":"something went wrong"}})   



    return jsonify({"result": {"status":1,"message":"successfully data saved"}})



@app.route('/liveSignals', methods=['POST'])

def getcurrentSignal():

  global liveSignal

  liveSignal=request.json['liveSignal']

  print(liveSignal)

  return (jsonify({"message":liveSignal}))

  







@app.route('/getCurrentSignal', methods=['GET', 'POST'])

def returnCurrentSignal():

  global liveSignal

  username=request.get_json()['userName'];

  print("liveSignal={}".format(liveSignal))
  
  CurrentDate=datetime.now().date()

  CurrentTime=datetime.now().time()

  endTime=t(0, 00,00)

  sihTime=t(6, 59,00)

  if(CurrentTime>=endTime and CurrentTime<=sihTime):

               filterDate=CurrentDate-timedelta(1)

  else:

               filterDate=CurrentDate

  presentDate=filterDate.strftime("%Y-%m-%d")

  print(presentDate) 

  try:  

      result=db.session.query(production).filter(and_(production.status.like("1"),production.operatorName.like(username),production.date.like(presentDate))).count()

      print(result)
 
      return (jsonify({'result':{"status":1,"liveSignal":liveSignal,"production":result}}))

  except:
      return (jsonify({'result':{"status":0,"liveSignal":liveSignal,"production":0}}))



@app.route('/getServerIP', methods=['GET'])
def getServerIP():
   try:
       result=serverConf.query.get(1)
       if result != None:
          serverIp=result.endpoint
          print(serverIp)
          return jsonify({"result": {"status":1,"data":serverIp,"message":"success"}})
       else:
          return jsonify({"result":{"status":1,"message":"no previous data found","data":""}})  
   except Exception as e:
       print(e)
       return jsonify({"result":{"status":0,"data":"","message":"failed"}})



@app.route('/updateServerIP', methods=['POST'])
def serverConfiguration():
  endpoint=request.get_json()['endpoint'] 
  try:
      result=serverConf.query.filter_by(id=1).scalar()
      if result!=None:
         db.session.query(serverConf).filter(serverConf.id == 1).update({serverConf.endpoint:endpoint})
         result.endpoint=endpoint
         db.session.commit()
         return jsonify({"result":{"message":"server credentials updated successfully","status":1}})
      else:
         serverConfObj=serverConf(id=1,endpoint=endpoint)
         db.session.add(serverConfObj) 
         db.session.commit()
         return jsonify({"result":{"message":"server credentials saved successfully","status":1}})  

  except Exception as e:
     print(e)   
     return jsonify({"result":{"message":"something went wrong","status":0}})



@app.route('/updateNetworkDetails', methods=['POST'])
def UpdatenetworkDetails():
   ip=request.get_json()['ip']
   gateway=request.get_json()['gateway']
   dns=request.get_json()['dns']

   networkFileData="interface eth0 \n static ip_address={}\n static routers={}\n static domain_name_servers={}".format(ip,gateway,dns)
   print(networkFileData)
   try:
      result = networkConf.query.filter_by(id=1).scalar()
      if result != None:
         db.session.query(networkConf).filter(networkConf.id==1).update({"ip":ip, "gateway":gateway,"dns":dns})
         db.session.commit()
         with open('/etc/dhcpcd.conf','w') as f:
            f.write(networkFileData)
            f.close()
         return jsonify({"result": {"status" : 1, "message":"network details  updated successfully"}})
      else:
         networkConfObject = networkConf(ip=ip,gateway=gateway,dns=dns)
         db.session.add(networkConfObject)
         db.session.commit()
         with open('/etc/dhcpcd.conf','w') as f:
            f.write(networkFileData)
            f.close()
         return jsonify({"result": {"status" : 1,"message":"network details saved successfully"}})   
   except Exception as e:
         return jsonify({"result": {"status" : 0,"message":"something went wrong"}})



@app.route('/updateSIgnalsDetails', methods=['POST'])
def UpdateSignalskDetails():
   resultList=[]
   objinList={}
   for i in range(1,13):
      objinList["signal"+str(i)]=request.get_json()['signal'+str(i)]
      objinList["pin"+str(i)]=request.get_json()['pin'+str(i)]
      objinList['enable'+str(i)]=request.get_json()['enable'+str(i)]
      # print(objinList)
      resultList.append(objinList)
      objinList={}

   try:
      result = pinout.query.filter_by(signalName='cycle').scalar()
      if result != None:
         db.session.query(pinout).delete()
         db.session.commit()
      
      for i,data in enumerate(resultList):
         pinoutObject=pinout(machineId="JG-20",signal=data['signal'+str(i+1)],pin=data['pin'+str(i+1)],status=data['enable'+str(i+1)])
         db.session.add(pinoutObject)
         db.session.commit()
      return jsonify({"result": {"status" : 1,"message":"network details saved successfully"}})   
   except Exception as e:
         print(e)
         return jsonify({"result": {"status" : 0,"message":"something went wrong"}})         


@app.route('/getNetworkConf', methods=['GET'])
def getNetworkConf():
   data={}
   try:
      result=networkConf.query.get(1)
      if result!=None:
         data['ip']=result.ip
         data['dns']=result.dns
         data['gateway']=result.gateway
         return jsonify({"result": {"status":1,"data":data,"message":"successfully fetched saved data"}})
      else:
         return jsonify({"result":{"status":1,"message":"no previous data found","data":{}}})

   except Exception as e:
      print(e)
      return jsonify({"result":{"status":0,"data":{},"message":"failed"}})      



@app.route('/updateOtherSettings', methods=['POST'])
def otherSettingsFunction():
   machineId=request.get_json()['machineId']
   batchSize=request.get_json()['batchSize']
   holdingRelay=request.get_json()['holdingRelay']
   machineBypass=request.get_json()['machineBypass']
   idleTimeout=request.get_json()['idleTimeout']
   cleaningInterval=request.get_json()['cleaningInterval']
   machineType=request.get_json()['machineType']
   try:
      result = otherSettings.query.filter_by(id=1).scalar()
      if result != None:
         db.session.query(otherSettings).filter(otherSettings.id==1).update({"machineId":machineId, "batchSize":batchSize,"holdingRelay":holdingRelay,"machineBypass":machineBypass,"idleTimeout":idleTimeout,"cleaningInterval":cleaningInterval,"machineType":machineType})
         db.session.commit()
         return jsonify({"result": {"status" : 1, "message":"other settings updated successfully"}})
      else:
         otherSettingsConfObject = otherSettings(machineId=machineId,batchSize=batchSize,holdingRelay=holdingRelay,machineBypass=machineBypass,idleTimeout=idleTimeout,cleaningInterval=cleaningInterval,machineType=machineType)
         db.session.add(otherSettingsConfObject)
         db.session.commit()
         return jsonify({"result": {"status" : 1,"message":"other settings saved successfully"}})   
   except Exception as e:
         print(e)
         return jsonify({"result": {"status" : 0,"message":"something went wrong"}})  


@app.route('/getOtherSettings', methods=['GET'])
def getOtherSettings():
   data={}
   try:
      result=otherSettings.query.get(1)
      if result!=None:
         data['machineId']=result.machineId
         data['batchSize']=result.batchSize
         data['holdingRelay']=result.holdingRelay
         data['machineBypass']=result.machineBypass
         data['idleTimeout']=result.idleTimeout
         data['cleaningInterval']=result.cleaningInterval
         data['machineType']=result.machineType
         
         return jsonify({"result": {"status":1,"data":data,"message":"successfully fetched saved data"}})
      else:
         return jsonify({"result":{"status":1,"message":"no previous data found","data":{}}})

   except Exception as e:
      print(e)
      return jsonify({"result":{"status":0,"data":{},"message":"failed"}}) 
     

if __name__ == "__main__":

    app.run(port=5002,threaded=True,debug=True)






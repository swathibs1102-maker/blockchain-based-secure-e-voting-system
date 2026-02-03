from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import pymysql
from django.http import HttpResponse
import os
import json
from web3 import Web3, HTTPProvider
from datetime import datetime
from datetime import date
import smtplib
from email.message import EmailMessage
import random
import shutil
import csv
import cv2
import face_recognition
import numpy as np
import pandas as pd
import sqlite3
import train_faces as trainface
import cv2
import pickle
import face_recognition
import datetime
import sqlite3 
import time

global contract, web3
contract = None
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages(id,name):
    co=['Id']
    df=pd.read_csv("PersonDetatils\PersonDetails.csv",names=co)
    
    namess = df['Id']
    ides=[]

    #print'Id:'
    #print namess
    
    Id=id
    
    ides=Id
    #print 'Id='
    #print ides
    name=name
    
    estest=0
    if ides in namess:
        estest=1
    else:
        estest=0
    #print estest
    if (estest==0):
        if(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            img_counter = 0
            DIR=f"./Dataset/{name}_{ides}"
            try:
                os.mkdir(DIR)
                print("Directory " , name ,  " Created ") 
            except FileExistsError:
                print("Directory " , name ,  " already exists")
                img_counter = len(os.listdir(DIR1))
            while(True):
                ret, frame = cam.read()
                cv2.imshow("Video", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = f"./Dataset/{name}_{ides}/opencv_frame_{img_counter}.png"
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + str(Id) +" Name : "+ name
            row = [Id , name]
            with open('PersonDetatils\PersonDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                
            if(name.isalpha()):
                res = "Enter Numeric Id"
               
        
    else:
        res = "Already Id Exist"
    return res
       
def getCurrentHour():
    now = datetime.datetime.now()
    dt = str(now)
    arr = dt.split(" ")
    arr = arr[1].strip().split(":")
    return int(arr[0])
def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})
def Signup(request):
    global otp,username
    if request.method == 'POST':
        uid = request.POST.get('uid', False)
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            otp=random.randint(1000,50000)
            print("Otp==",otp)
            msg=EmailMessage()
            msg.set_content(str(username)+" OTP is : "+str(otp))
            msg['Subject']='OTP'
            msg['From']="evotingotp4@gmail.com"
            msg['To']=email
            s=smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login("evotingotp4@gmail.com","xowpojqyiygprhgr")
            s.send_message(msg)
            s.quit()
            output=TakeImages(int(uid),username)
            context= {'data':'Signup Process Completed'+str(output)}
            return render(request, 'val.html', context)
        else:
            context= {'data':'Error in signup process'}
            return render(request, 'Register.html', context)
def regotpverify(request):
    if request.method == 'POST':
        global email_id,otp
        uotp = request.POST.get('username', False)
        if int(uotp)==otp:
            context={'data':'Otp Verified Sucessfully'}
            return render(request, 'Login.html', context)
        else:
            context={'data':'Otp Verification Failed'}
            return render(request, 'Register.html', {})
def otpverify(request):
    if request.method == 'POST':
        global email_id,otp1,username
        uotp = request.POST.get('username', False)
        if int(uotp)==otp1:
            context= {'data':'<center><font size="3" color="black">Welcome '+username+' <br/><br/><br/><br/><br/>'}
            return render(request, 'UserScreen.html', context)
        else:
            context={'data':'Otp Verification Failed'}
            return render(request, 'Login.html', context)

def trainmodel(request):
    if request.method=='GET':
        trainface.trainer()
        context={'data':'Model Trainned Successfully'}
        return render(request,'AdminScreen.html',context)
def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.5):

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    # X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    # print(closest_distances)
    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]



def identify_faces(video_capture):

    buf_length = 10
    known_conf = 5
    buf = [[]] * buf_length
    i = 0

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="./models/trained_model.clf")
            # print(predictions)

        process_this_frame = not process_this_frame

        face_names = []
        current_date=datetime.datetime.today().strftime('%Y-%m-%d')

        for name, (top, right, bottom, left) in predictions:

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            print("Recognized name==",name)
            if name!="UNKNOWN" or name!="unknown" or name!="UnKnown":
               return name
               break



            #identify1(frame, name, buf, buf_length, known_conf)

            face_names.append(name)

        buf[i] = face_names
        i = (i + 1) % buf_length


        # print(buf)


        # Display the resulting image
        cv2.imshow('In Camera', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def UserLogin(request):
    if request.method == 'POST':
        global otp1,email_id,username,const
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    email_id = row[3]
                    const= row[4]
                    status = 'success'
                    break
        if status == 'success':
            hour = getCurrentHour()
            if hour >= 9 and hour < 19:
                cam=cv2.VideoCapture(0)
                fname=identify_faces(cam)
                if fname==username:
                    otp1=random.randint(1000,50000)
                    print("Otp1==",otp1)
                    msg=EmailMessage()
                    msg.set_content(str(fname)+"  OTP is : "+str(otp1))
                    msg['Subject']='OTP'
                    msg['From']="evotingotp4@gmail.com"
                    msg['To']=email_id
                    s=smtplib.SMTP('smtp.gmail.com',587)
                    s.starttls()
                    s.login("evotingotp4@gmail.com","xowpojqyiygprhgr")
                    s.send_message(msg)
                    s.quit()
                    file = open('session.txt','w')
                    file.write(username)
                    file.close()
                    context= {'data':'<center><font size="3" color="black">Welcome '+username+'<br/><br/><br/><br/><br/>'}
                    return render(request, 'val1.html', context)
                else:
                    context= {'data':'Face is not matched'}
                    return render(request, 'Login.html', context)
            else:
                context= {'data':'Login & Voting will be allowed between 9:00 AM to 6:00 PM'}
                return render(request, 'Login.html', context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)


def saveVote(candidate, name, symbol, voter, aadhar):
    global contract, web3
    if contract == None:
        blockchain_address = 'http://127.0.0.1:9545'
        # Client instance to interact with the blockchain
        web3 = Web3(HTTPProvider(blockchain_address))
        # Set the default account (so we don't need to set the "from" for every transaction call)
        web3.eth.defaultAccount = web3.eth.accounts[0]
        # Path to the compiled contract JSON file
        compiled_contract_path = 'EVoting.json'
        # Deployed contract address (see `migrate` command output: `contract address`)
        deployed_contract_address = '0xDC1604c520310311b9559d54e0aeC9B679749eBd'
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        file.close()
        # Fetch deployed contract reference
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    # Call contract function (this is not persisted to the blockchain)
    msg = contract.functions.markVote(candidate, name, symbol, voter, aadhar).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    return str(msg)


def getVote(candidate):
    global contract, web3
    if contract == None:
        blockchain_address = 'http://127.0.0.1:9545'
        # Client instance to interact with the blockchain
        web3 = Web3(HTTPProvider(blockchain_address))
        # Set the default account (so we don't need to set the "from" for every transaction call)
        web3.eth.defaultAccount = web3.eth.accounts[0]
        # Path to the compiled contract JSON file
        compiled_contract_path = 'EVoting.json'
        # Deployed contract address (see `migrate` command output: `contract address`)
        deployed_contract_address = '0xDC1604c520310311b9559d54e0aeC9B679749eBd'
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        file.close()
        # Fetch deployed contract reference
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    message = contract.functions.getCount(candidate).call()
    return message

def CastVoteAction(request):
    global const,otp2
    if request.method == 'POST':
        candidate_id = request.POST.get('t1', False)
        voter = request.POST.get('t2', False)
        uotp = request.POST.get('t3', False)
        print("User Otp==",uotp)
        print("otp2==",otp2)
        if int(uotp)==int(otp2):
            con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
            with con:
                cur = con.cursor()
                cur.execute("select * FROM castvote where uname='"+voter+"'")
                rows = cur.fetchone()
                if rows==None:
                    cur1 = con.cursor()
                    cur1.execute("select * FROM candidate where cname='"+str(const)+"'")
                    rows1 = cur1.fetchall()
                    print("rows==",rows1)
                    for row in rows1:
                        if int(candidate_id) == int(row[0]):
                            print("candidate_id==",candidate_id)
                            print("row[0]==",row[0])
                            saveVote(int(row[0]),str(row[1]),str(row[2]),voter,const)
                        
                    context= {'data':'Your vote saved inside Ethereum'}
                    db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
                    db_cursor = db_connection.cursor()
                    student_sql_query = "INSERT INTO castvote(uname) VALUES('"+voter+"')"
                    db_cursor.execute(student_sql_query)
                    db_connection.commit()
                    print(db_cursor.rowcount, "Record Inserted")
                    return render(request, 'index.html', context)
                else:
                    context={'data':'You have voted already'}
                    return render(request, 'index.html', context)
        else:
            context={'data':'OTP Verification Failed Try again'}
            return render(request, 'index.html', context)

                  

def Addcand(request):
    if request.method == 'GET':
       return render(request, 'Addcandidate.html', {})
def addcanditate(request):
    if request.method=='POST':
        candname=request.POST.get('t2',False)
        pname=request.POST.get('t3',False)
        cname=request.POST.get('t4',False)
        handle_uploaded_file(request.FILES['t5'], str(request.FILES['t5']))
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO candidate(candname,partyname,cname,fname) VALUES('"+candname+"','"+pname+"','"+cname+"','"+str(request.FILES['t5'])+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context={'data': 'Added success'}
        return render(request, 'Addcandidate.html', context)
def handle_uploaded_file(file, filename):
    if not os.path.exists('EVotingApp/static/upload/'):
        os.mkdir('EVotingApp/static/upload/')

    with open('EVotingApp/static/upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'Welcome Admin'}
            return render(request, "AdminScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'Admin.html', context)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})
def ViewCountes(request):
    if request.method=='POST':
        global const1
        const1 = request.POST.get('t1', False)
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Candidate ID','Candidate Name','Party Name','constitution ','Symbol','View Count']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM candidate where cname='"+str(const1)+"'")
            rows = cur.fetchall()
            print("rows==",rows)
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+row[1]+"</td>"
                output += "<td>"+font+row[2]+"</td>"
                output += "<td>"+font+row[3]+"</td>"
                output+='<td><img src=/static/upload/'+row[4]+' height=100 width=100/></td>'
                output+='<td><a href=\'ViewCountAction?t1='+str(row[0])+'\'><font size=3 color=white>Click Here</font></a></td></tr>'
            context= {'data':output}
            return render(request, 'ViewCount1.html', context)  


def ViewCount(request):
    if request.method == 'GET':
       return render(request, 'ViewCount.html', {})    

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})

def Vote(request):
    global const
    if request.method == 'GET':
        print("const=",const)
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Candidate ID','Candidate Name','Party Name','constitution ','Symbol','Cast Your Vote']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM candidate where cname='"+str(const)+"'")
            rows = cur.fetchall()
            print("rows==",rows)
            for row in rows:
                output += "<tr><td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+row[1]+"</td>"
                output += "<td>"+font+row[2]+"</td>"
                output += "<td>"+font+row[3]+"</td>"
                output+='<td><img src=/static/upload/'+row[4]+' height=100 width=100/></td>'
                output+='<td><a href=\'CastVote?t1='+str(row[0])+'\'><font size=3 color=white>Click Here</font></a></td></tr>'
        
        context= {'data':output}        
        return render(request, 'Vote.html', context)

def CastVote(request):
    if request.method == 'GET':
        global email_id,otp2,username
        otp2=random.randint(1000,50000)
        print("Otp==",otp2)
        msg=EmailMessage()
        msg.set_content(str(username)+"OTP is : "+str(otp2))
        msg['Subject']='OTP'
        msg['From']="evotingotp4@gmail.com"
        msg['To']=email_id
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("evotingotp4@gmail.com","xowpojqyiygprhgr")
        s.send_message(msg)
        s.quit()
        candidate = request.GET.get('t1', False)
        output = '<TR><TH align="left"><font size="" color="white">Candidate&nbsp;ID<TD><Input type=text name="t1" value="'+candidate+'" class="form-control" readonly></TD></TR>'
        context= {'data1':output}        
        return render(request, 'CastVote.html', context)

def ViewCountAction(request):
    if request.method == 'GET':
        global const1
        candidate = request.GET.get('t1', False)
        print("candidate===",candidate)
        count = getVote(int(candidate))
        print(str(count)+"===========================================")
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Candidate ID','Candidate Name','Party','constitution','Total Votes Received']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'evoting',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM candidate where cname='"+str(const1)+"'")
            rows = cur.fetchall()
            print("rows==",rows)
            for row in rows:
                if int(row[0])==int(candidate):
                    output += "<tr><td>"+font+str(row[0])+"</td>"
                    output += "<td>"+font+row[1]+"</td>"
                    output += "<td>"+font+row[2]+"</td>"
                    output += "<td>"+font+row[3]+"</td>"
                    output += "<td>"+font+str(count)+"</td>"        
        context= {'data':output}        
        return render(request, 'ViewResult.html', context)
    

    

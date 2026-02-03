import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import cv2
import face_recognition
import numpy as np
import pandas as pd
import sqlite3
import train_faces as knntrain
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
#import datetime
import time
from datetime import datetime
import incamera as ic
import outcamera as oc



window = tk.Tk()

window.title("Face_Recogniser")


window.configure(background='blue')



window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="Doctor Attendance-System" ,bg="Green"  ,fg="white"  ,width=50  ,height=3,font=('times', 30, 'italic bold underline')) 

message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="yellow" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="yellow"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=315)



lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=400, y=400)

message = tk.Label(window, text="" ,bg="yellow"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=700, y=415)


 
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')        
    res = ""
    message.configure(text= res)


    
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
 
def TakeImages():
    co=['Id']
    df=pd.read_csv("PersonDetatils\PersonDetails.csv",names=co)
    
    namess = df['Id']
    ides=[]

    #print'Id:'
    #print namess
    
    Id=(txt.get())
    
    ides=Id
    #print 'Id='
    #print ides
    name=(txt2.get())
    
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
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('PersonDetatils\PersonDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)
        
    else:
        res = "Already Id Exist"
        message.configure(text= res)

   
def TrainImages():
    knntrain.trainer()
    res = "Trainned Successfull"
    message.configure(text= res)
def TrackImages():
    print("In Camera Started")
    Url="http://192.168.1.11:8080/video"
    cam = cv2.VideoCapture(0)# change 0 to 1 for usb camera
    #'rtsp://eswar:eswar@192.168.1.14:8080/h264_ulaw.sdp'
    ic.identify_faces(cam)
def TrackoutImages():
    print("Out Camera Started")
    cam = cv2.VideoCapture(0)# change 0 to 1 for usb camera
    #'rtsp://eswar:eswar@192.168.1.14:8080/h264_ulaw.sdp'
    oc.identify_faces(cam)
    






  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=200)
  
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=210, y=500)

trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=210, y=600)
trackImg = tk.Button(window, text="Start In camera", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=510, y=500)
trackImg1 = tk.Button(window, text="Start Out camera", command=TrackoutImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg1.place(x=510, y=600)

quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=810, y=550)

 
window.mainloop()

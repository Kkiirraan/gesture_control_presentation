import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

#variable 
width,height=1000,600
folderPath="presentation"

#camera set up
cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#resize the image
new_width = 800
new_height = 600

#Getting the list of presntation images
pathImages=sorted(os.listdir(folderPath),key=len)
# print(pathImages)

#variables
imgNumber=5
hs,ws=int(120*1),int(213*1)
gestureThreshold=300
buttonPressed=False
buttonCounter=0
buttonDelay=30
annotations=[[]]
annotationNumber=0
annotationStart=False
#handdetector
detector=HandDetector(detectionCon=0.8,maxHands=1)

while True:
    #Importing images
    success,img=cap.read()
    img=cv2.flip(img,1)
    pathFullImage=os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent=cv2.imread(pathFullImage)
    
    hands,img=detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10)
    
    if hands and buttonPressed is False:
        hand=hands[0]
        #to check how many fingers are up
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        lmList=hand['lmList']
        
        #constrain values for easiler drawing
        indexFinger=lmList[8][0],lmList[8][1]
        xVal=int(np.interp(lmList[8][0],[width//2,width-300],[0,new_width+1000]))
        yVal=int(np.interp(lmList[8][1],[200,height-200],[0,new_height+1000]))
        indexFinger=xVal,yVal
        # print(fingers)
        
        if cy<=gestureThreshold: # if hand is at the height of the face
            annotationStart=False
            #gesture 1 left
            if fingers==[1,0,0,0,0]:
                annotationStart=False
                print("left")
                if imgNumber>0:
                    imgNumber -=1
                    buttonPressed=True
                    annotations=[[]]
                    annotationNumber=0
                    
            #gesture 2 right
            if fingers==[0,0,0,0,1]:
                annotationStart=False
                print("right")  
                if imgNumber<len(pathImages)-1:
                   imgNumber +=1
                   buttonPressed=True
                   annotations=[[]]
                   annotationNumber=0
                   
        #gesture 3 pointer
        if fingers==[0,1,1,0,0]:
           cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)  
           annotationStart=False     
        #gesture 4 Draw
        if fingers==[0,1,0,0,0]:
            if annotationStart is False:
                annotationStart=True
                annotationNumber+=1
                annotations.append([])
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)  
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart=False
            
        #gesture 5 erase
        if fingers==[0,1,1,1,0]:
            if annotations:
                if annotationNumber>=0:
                    annotations.pop(-1)
                    annotationNumber -=1
                    buttonPressed=True
    else:
        annotationStart=False          
            
    #button pressed iterations
    if buttonPressed:
        buttonCounter +=1
        if buttonCounter>buttonDelay:       
            buttonCounter=0
            buttonPressed=False              
    
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
           if j!=0:
              cv2.line(imgCurrent,annotations[i][j-1],annotations[i][j],(0,0,200),12)
    
    #adding webcam images on the slide
    imgSmall=cv2.resize(img,(ws,hs))
    # Resize the image
    resized_img = cv2.resize(imgCurrent, (new_width, new_height))
    h,w,_=resized_img.shape
    resized_img[0:hs,w-ws:w]=imgSmall
    

    cv2.imshow("image",img)
    cv2.imshow("presentation",resized_img)
    
    key=cv2.waitKey(1)
    if key==ord('q'):
        break
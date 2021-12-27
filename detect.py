import cv2 
import pandas as pd
from datetime import datetime

firstframe=None

statuslist =[None,None]         # list to append status of every frame

times=[]                # list to append time when ever object enter or leave the frame 

df = pd.DataFrame(columns=["Start","End"])  # dataframe to record start and end time when the object is detected

video = cv2.VideoCapture(0)

while True:
    check,frame = video.read()

    status = 0      # status initially 0 as object is not in the frame

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # To convert the frame to grayscale

    blur=cv2.GaussianBlur(gray,(21,21),0)   # To get gaussian blur of the grayscale frame

    if firstframe is None:
        firstframe=blur             # update the first frame
        continue

    deltaframe= cv2.absdiff(firstframe,blur)          # delta frame with diff between first and current frame
    threshdelta=cv2.threshold(deltaframe,30,255,cv2.THRESH_BINARY)[1]
    threshdelta=cv2.dilate(threshdelta,None,iterations=0)
    (cnts,_)=cv2.findContours(threshdelta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour)<1000:
            continue

        status = 1         # status changed as object is detected 

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) # adding rectangle

    statuslist.append(status)  # appending current status of frame at the end

    statuslist = statuslist[-2:]    # keeping only most recent entries of status and descarding rest

    if statuslist[-1]== 1 and statuslist[-2]==0:
        times.append(datetime.now())            ## append date time if object enters
    if statuslist[-1]==0 and statuslist[-2]==1:
        times.append(datetime.now())          ## append date time if object leaves

    cv2.imshow('frame',frame)
    cv2.imshow("Gray",gray)
    cv2.imshow("capturing",blur)
    cv2.imshow("delta",deltaframe)
    cv2.imshow("thresh",threshdelta)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break


print(statuslist)
print(times)

for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True) ## storing times values in the dataframe

print(df)
df.to_csv("times.csv")          ## exporting df to csv file

video.release()
cv2.destroyAllWindows()
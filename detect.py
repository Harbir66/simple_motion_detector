import cv2 
import time 

firstframe=None

video = cv2.VideoCapture(0)

while True:
    check,frame = video.read()

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    blur=cv2.GaussianBlur(gray,(21,21),0)

    if firstframe is None:
        firstframe=blur
        continue

    deltaframe= cv2.absdiff(firstframe,blur)
    threshdelta=cv2.threshold(deltaframe,30,255,cv2.THRESH_BINARY)[1]
    threshdelta=cv2.dilate(threshdelta,None,iterations=0)
    (cnts,_)=cv2.findContours(threshdelta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour)<1000:
            continue
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    cv2.imshow('frame',frame)
    cv2.imshow("Gray",gray)
    cv2.imshow("capturing",blur)
    cv2.imshow("delta",deltaframe)
    cv2.imshow("thresh",threshdelta)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
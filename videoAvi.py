#!/usr/bin/python
import numpy as np
import cv2

cap = cv2.VideoCapture('vtest.avi')
cnt=0
while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cnt = cnt+1
    if cnt%25==0:
        cv2.imwrite('novi/'+str(cnt)+'.jpg', frame)
    #cv2.imshow('frame',gray)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

cap.release()
cv2.destroyAllWindows()

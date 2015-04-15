import cv2
import numpy as np
import sys
cap = cv2.VideoCapture(0)

cnt=0
while(1):
    _, frame = cap.read()
    #print _
    #if _ == False:
        #sys.exit("ne radi mi kamera")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print hsv

    lower_skin_bound = np.array([0,48,80],dtype=np.uint8)
    upper_skin_bound = np.array([20,255,255],dtype=np.uint8)
    
    mask = cv2.inRange(hsv, lower_skin_bound, upper_skin_bound)
    res = cv2.bitwise_and(frame, frame, mask = mask)

    #res = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)

    #if cnt%25==0:
    cv2.imshow('res', res)
    #cnt+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #break
cv2.destroyAllWindows()

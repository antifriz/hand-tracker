import cv2
import numpy as np
cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255

while(1):
    ret, frame2 = cap.read()
    nextt = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame2',nextt)


    flow = cv2.calcOpticalFlowFarneback(prvs,nextt, None, 0.5, 3, 15, 3, 5, 1.2, 0)


    

    mag,ang = cv2.cartToPolar(flow[...,0], flow[...,1])

    print ang



    hsv[...,0] = ang[:,:,0]*180/np.pi/2
    
    hsv[...,2] = cv2.normalize(mag[:,:,0],None,0,255,cv2.NORM_MINMAX)
    rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    
    

    cv2.imshow('frame2',rgb)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv2.imwrite('opticalfb.png',frame2)
        cv2.imwrite('opticalhsv.png',rgb)
    prvs = nextt

cap.release()
cv2.destroyAllWindows()
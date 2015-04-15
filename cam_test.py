#!/usr/bin/python
import cv2
import sys
import time
from os import listdir
from os.path import isfile,join

cameraNum = 1

br=0
count = 0
save = False
"""
badFolder = "bad"

onlyfiles = [ f for f in listdir(badFolder) if isfile(join(badFolder,f))]

for f in onlyfiles:
    br = int(f[2:-4])
    if br>=count:
        count=br

print br
"""

#cascPath = "andol.xml" #sys.argv[1]
#faceCascade = cv2.CascadeClassifier(cascPath)

#cascPath2 = "andol-2.xml" #sys.argv[1]
#faceCascade2 = cv2.CascadeClassifier(cascPath2)

cascPath3 = sys.argv[1]
#cascPath3 = "cascade/cascade.xml" #sys.argv[1]
faceCascade3 = cv2.CascadeClassifier(cascPath3)

#cascPath4 = "cascade-backup/cascade.xml" #sys.argv[1]
#faceCascade4 = cv2.CascadeClassifier(cascPath4)


video_capture = cv2.VideoCapture(0)

#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)

"""

import os
import xml.etree.ElementTree as ET

rects = []

#path ='../palms/cascade-backup-2/cascade.xml'
path = cascPath3

tree = ET.parse(path)
root = tree.getroot()
allrect = root.findall('./cascade/features/_/rects/_')#'./cascade/features/_/rects/_')
for rect in allrect:
     rects.append(rect.text.strip()[:-1].split())
"""
broj = 0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    #frame_cleared = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(5,5))

    #gray = cv2.fastNlMeansDenoisingColored(gray,None,10,10,7,21)
    
    """
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=100,
        minNeighbors=1,
        minSize=(20,20),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    
    faces2 = faceCascade2.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=15,
        minSize=(20,20),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    """
    #blj = []
    #lw = []
    minN = int(sys.argv[2])
    faces3 = faceCascade3.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=minN,
        minSize=(60,90),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
        #rejectLevels=blj,
        #levelWeights=lw,
        #outputRejectLevels=True
    )
    #print str(lw)
    #print str(blj)

    """
        faces4 = faceCascade4.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=40,
            minSize=(40,60),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
   
    for (x, y, w, h) in faces2:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    """

    for (x, y, w, h) in faces3:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    """
        for rect in rects:
            if(int(rect[3])<5):
                continue
            overlay = frame#.copy()

            color = (255,255,255) if (int(rect[4])<0) else (0,0,0)

            prvi = (int(rect[0])*w/20+x,int(rect[1])*h/30+y)
            drugi = ((int(rect[0])+int(rect[2]))*w/20+x,(int(rect[1])+int(rect[3]))*h/30+y)
            cv2.rectangle(overlay,prvi,drugi,color,-1)
            opacity = 0.1
            cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)
    """

    frame = cv2.flip(frame,1)
    # Display the resulting frame

    cv2.imshow('Video', frame)
    """

    if cv2.waitKey(1) & 0xFF == ord('s'):
        if broj%5 ==0:
            cv2.imwrite(badFolder+"/c-%d.jpg" % count, frame_cleared)
            print 'Saving: '+str    (count)+'.jpg'
            count +=1
        broj +=1
    """

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

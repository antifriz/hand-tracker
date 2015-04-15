#!/usr/bin/python
import cv2
import sys
from os import listdir
from os.path import isfile,join

video_capture = cv2.VideoCapture(0)

br=0
count = 0
save = False

onlyfiles = [ f for f in listdir('kokolo') if isfile(join('kokolo',f))]

for f in onlyfiles:
    br = int(f[2:-4])
    if br>=count:
        count=br

print br


cascPath = "../najbolje-od-svega.flac/cascade.xml" #sys.argv[1]
cascade = cv2.CascadeClassifier(cascPath)

broj = 0
while True:
    ret, frame = video_capture.read()
    cropFrame = frame

    hand = cascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=15,
        minSize=(60,90),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
        #rejectLevels=blj,
        #levelWeights=lw,
        #outputRejectLevels=True
    )

    frame2 = frame.copy()

    for (x, y, w, h) in hand:
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)

    if len(hand):
        broj+=1
        print "jej"

    cv2.imshow('Video', frame2)


    if cv2.waitKey(1) & 0xFF == ord('s') or True:
        if broj%25 ==0:
            cv2.imwrite("kokolo/c-%d.jpg" % count, frame)
            print 'Saving: '+str    (count)+'.jpg'
            count +=1
            broj+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video_capture.release()
cv2.destroyAllWindows()

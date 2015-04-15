#!/usr/bin/python
import cv2
import sys
from os import listdir
from os.path import isfile,join

Width = 200
Height = 300

PeekWidth = 300
PeekHeight = 300

MaxWidth = 640
MaxHeight = 300

xMinPeek = (MaxWidth-PeekWidth)/2
xMaxPeek = (MaxWidth-PeekWidth)/2+PeekWidth
yMinPeek = (MaxHeight-PeekHeight)/2
yMaxPeek = (MaxHeight-PeekHeight)/2+PeekHeight

xMin = (PeekWidth-Width)/2
xMax = (PeekWidth-Width)/2+Width
yMin = (PeekHeight-Height)/2
yMax = (PeekHeight-Height)/2+Height

video_capture = cv2.VideoCapture(0)

rootCascade = '../../kaskade!/'

cascades = [cv2.CascadeClassifier(rootCascade+x) for x in listdir(rootCascade) if x.endswith('sanker.xml')]


br=0
count = 0
save = False

onlyfiles = [ f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1],f))]

for f in onlyfiles:
    br = int(f[2:-4])
    if br>=count:
        count=br

print br


broj = 0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    cropFrame = frame[yMinPeek:yMaxPeek,xMinPeek:xMaxPeek]

    cropFlipFrame = cv2.flip(cropFrame,1)

    frame = cropFlipFrame
    folder = sys.argv[1]

    frameMain = frame[yMin:yMax,xMin:xMax]

    hands = [cascade.detectMultiScale(
        frameMain,
        scaleFactor=1.1,
        minNeighbors=0,
        minSize=(60,90),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    ) for cascade in cascades]


#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Draw a rectangle around the faces
    frame2 = frame.copy()
    cv2.rectangle(frame2, (xMin-2, yMin-2), (xMax+2, yMax+2), (80, 255, 80,0), 2)

    flag = False
    for hand in hands:
        for (x, y, w, h) in hand:
            cv2.rectangle(frame2,(x+xMin,y+yMin),(x+xMin+w,y+yMin+h), (80, 80, 80,0), 2)         
        if not len(hand):
            flag = True


    # Display the resulting frame
    cv2.imshow('Video', frame2)


    if cv2.waitKey(1) & 0xFF == ord('s') and flag:
        broj +=1
        if broj%12 ==0:
            cv2.imwrite(sys.argv[1]+"/c-%d.jpg" % count, frameMain)
            print 'Saving: '+str(count)+'.jpg'
            count +=1
            broj = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

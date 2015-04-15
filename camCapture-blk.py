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

br=0
count = 0
save = False

dir = 'blk-condensed'

onlyfiles = [ f for f in listdir(dir) if isfile(join(dir,f))]

for f in onlyfiles:
    br = int(f[2:-4])
    if br>=count:
        count=br
	print br
print count


broj = 0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    cropFrame = frame[yMinPeek:yMaxPeek,xMinPeek:xMaxPeek]

    cropFlipFrame = cv2.flip(cropFrame,1)

    frame = cropFlipFrame


#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Draw a rectangle around the faces
    cv2.rectangle(frame, (xMin-2, yMin-2), (xMax-2, yMax-2), (80, 255, 80,0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('s'):
        if broj%5 ==0:
            cv2.imwrite(dir+"/c-%d.jpg" % count, frame[yMin:yMax,xMin:xMax])
            print 'Saving: '+str    (count)+'.jpg'
            count +=1
        broj +=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

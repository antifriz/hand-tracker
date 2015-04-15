#!/usr/bin/python
import cv2
import numpy as np
import fileinput
import os
import sys

cascPath = sys.argv[1]
#posVec = sys.argv[2]
rootNeg = sys.argv[2]
minN = sys.argv[3]
#widthPosVec = int(sys.argv[4])
#heightPosVec = int(sys.argv[5])

posPtr = None

def initPos(posVec,width,height):
    global posPtr
    with open(posVec,'rb') as stream:
        fbytes = bytearray(stream.read())
        fbytes = fbytes[12:]
    posPtr = fbytes
    #print len(fbytes)/width/height/4

i=1
def getNextPos(width,height):
    global posPtr,i
    #if i%100 ==0:
    #    print i
    i+=1

    area = width*height

    if len(posPtr)< area*4+2:
        return None

    buff = posPtr[:area*2]
    posPtr = posPtr[area*4+2:]

    img = np.asmatrix(buff,dtype=np.uint8)

    img = []
    row = []
    w2 = width*2
    for x in xrange(0,len(buff)):
        if x%2:
            row.append(buff[x])
        if (x+1)%(w2) == 0:
            img.append(row)
            row = []

    img = np.asmatrix(img,dtype=np.uint8)
    return img


def getPerc(img,perc):
    height, width = img.shape
    return int(width*perc),int(height*perc)

#initPos(posVec,widthPosVec,heightPosVec)

cascade = cv2.CascadeClassifier(cascPath)

PADDING_PERCENT = 0.2

#
# check positives
#

cntSum=0
cntBad=0
"""

while True:
    img = getNextPos(widthPosVec,heightPosVec)
    if img == None:
        break

    widthRel, heightRel = getPerc(img,PADDING_PERCENT)

    paddingW, paddingH = int(widthRel/2),int(heightRel/2)

    img = cv2.copyMakeBorder(img,paddingW,paddingH,paddingW,paddingH,cv2.BORDER_CONSTANT,value=[0,0,0])

    widthRel80, heightRel80 = getPerc(img,1-PADDING_PERCENT)

    hands = cascade.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=0,
        minSize=(20,30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
        #rejectLevels=blj,
        #levelWeights=lw,
        #outputRejectLevels=True
    )
    cntSum+=1
    if not len(hands):
#        for (x, y, w, h) in hands:
 #           cv2.rectangle(img, (x, y), (x+w, y+h), (128,128,128), 1)
        cntBad+=1
        #cv2.imshow('iqmg', img)


        #if cv2.waitKey(0) & 0xFF == ord('q'):
        #    break

print "HR -> " + str(cntSum-cntBad) + " / " + str(cntSum) + " : " + str(1-float(cntBad)/cntSum)

"""



cntSum=0
cntBad=0

WIDTH_DESIRED = 90
HEIGHT_DESIRED = 90


def splitImg(img):

    h,w = img.shape[:2]

    numY = h / HEIGHT_DESIRED if h>HEIGHT_DESIRED else 1
    numX = w / WIDTH_DESIRED if w>WIDTH_DESIRED else 1

    oneWidth = w/numX
    oneHeight = h/numY

    imgVect = []

    #print h,w,numX, numY

    if numX == 1 and numY == 1:
        return [img]

    for i in xrange(0,numY):
        for j in xrange(0,numX):
            xStart = j * oneWidth
            xEnd = (j+1) * oneWidth
            yStart = i*oneHeight
            yEnd = (i+1)*oneHeight
            #print xStart,xEnd,yStart,yEnd
            #print img.shape
            tmpImg = img[yStart:yEnd,xStart:xEnd]#.copy()
            imgVect.append(tmpImg)
            #cv2.imshow('img', img)

            #cv2.imshow('iqmg', tmpImg)
            #if cv2.waitKey(0) & 0xFF == ord('q'):
            #    break
    return imgVect


root = rootNeg
listadirr = os.listdir(root)
listadirr = [ x for x in listadirr if not '.' in x]
for dirr in listadirr:
    if(dirr =='rezultati-pos'):
        print 'NOOO'
        continue
    for filee in os.listdir(root + '/' + dirr):
        path = root + "/" + dirr+ "/" + filee
        imgBLJ = cv2.imread(path)


        imgVect = splitImg(imgBLJ)

        for im in imgVect:


            #cv2.imshow('iqmg', im)
            hands = cascade.detectMultiScale(
                im,
                scaleFactor=1.03,
                minNeighbors=int(minN),
                minSize=(40,60),
                #outputRejectLevels=True
            )
            cntSum+=1
            if not len(hands):
        #        for (x, y, w, h) in hands:
         #           cv2.rectangle(img, (x, y), (x+w, y+h), (128,128,128), 1)
                cntBad+=1
                continue
            
            for (x, y, w, h) in hands:
                cv2.rectangle(im, (x, y), (x+w, y+h), (128,128,128), 1)
            
            #print path
            #cv2.imshow('iqmg', im)

            #if cv2.waitKey(0) & 0xFF == ord('q'):
            #    break



print "FA -> " + str(cntSum-cntBad) + " / " + str(cntSum) + " : " + str(1-cntBad/(cntSum+0.01))

cv2.destroyAllWindows()


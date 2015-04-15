#!/usr/bin/python
import numpy as np
import cv2
import os
import sys
import xml.etree.ElementTree as ET

rects = []

#path ='../palms/cascade-backup-2/cascade.xml'
cascPath = sys.argv[1]
imgPath = sys.argv[2]

tree = ET.parse(cascPath)
root = tree.getroot()
allrect = root.findall('./cascade/features/_/rects/_')#'./cascade/features/_/rects/_')
for rect in allrect:
	 rects.append(rect.text.strip()[:-1].split())

img = cv2.imread(imgPath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.resize(img, (0,0), fx=.5, fy=.5) 
	 
imgTmp = cv2.resize(img, (0,0), fx=1, fy=1)
			 
for rect in rects:
	if int(rect[4])<0 :
		large = cv2.resize(img, (0,0), fx=20, fy=20) 
		cv2.imshow('img', large)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			exit(1)

	if int(rect[4])<0 :
		img = cv2.resize(imgTmp, (0,0), fx=1, fy=1)
	color = (255,255,255) if (int(rect[4])<0) else (0,0,0)
	
	prvi = (int(rect[0]),int(rect[1]))
	drugi = (int(rect[0])+int(rect[2]),int(rect[1])+int(rect[3]))
	cv2.rectangle(img,prvi,drugi,color,-1)








#	if len(faces) >0:
	



cv2.destroyAllWindows()
	
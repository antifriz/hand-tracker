#!/usr/bin/python

from pygame.locals import *
from sys import exit
import random, cv2, numpy as np, sys, pygame

BAR_HEIGHT = 100
MAX_MOV = 20

cascPath = sys.argv[1]

LAST_CNT = 12
INC_COLOR = 255/LAST_CNT
EXTEND_FACTOR = 1
DEV_WINDOW=75



def print_positions(arr,color,img):
  for a in arr:
    cv2.circle(img,a[:2],5,color,thickness=-1)

def getDev(positions_array,player,is_left):
  if len(positions_array) == 0:
    return (player[0]-camW,player[0]+camW) 
  i=1
  suma = 0
  div = 0
  minW = camW
  maxW = 0
  for pos in positions_array:
    for p in pos:
      suma += i*p[0]
      div += i
      if maxW < p[0]:
        maxW = p[0]
      if minW > p[0]:
        minW = p[0]

    i+=1

  if len(positions_array) == 0 or div == 0:
    return (camW/4-50,camW/4+50) if is_left else (3*camW/4-50,3*camW/4+50) 
  devRoot = suma/div
  dev = int(devRoot*EXTEND_FACTOR)


  return (minW-DEV_WINDOW,maxW+DEV_WINDOW)

  return (player[0]-dev,player[0]+dev)


def findNext(hands,player,positions_array,is_left):
  
  dev = getDev(positions_array,player,is_left)

  new_positions = []

  avgSumH=0
  avgDivH=0
  for (x, y, w, h) in hands:
    centerx = x+w/2+(0 if is_left else camW/2)
    centery = y+h/2
    if centerx>dev[0] and centerx<dev[1]:
      pos = (centerx,centery)
      new_positions.append(pos)
      avgSumH +=centery
      avgDivH +=1

  if avgDivH == 0:
    avgH = None
  else:
    avgH = avgSumH/avgDivH


  return new_positions,dev,avgH


cam = cv2.VideoCapture(0)
camW = int(cam.get(3))
camH = int(cam.get(4))

avgH1 = avgH2 = camH/2
cascade = cv2.CascadeClassifier(cascPath)
player1 = (camW/4,camH/2)
player2 = (3*camW/4,camH/2)
positions_array_1 = []
positions_array_2 = []

pygame.init()

#inicijalizacija igre

screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption("Pong Pong!")

#Creating 2 bars, a ball and background.
back = pygame.Surface((640,480))
background = back.convert()
background.fill((0,0,0))
bar = pygame.Surface((10,BAR_HEIGHT))
bar1 = bar.convert()
bar1.fill((0,0,255))
bar2 = bar.convert()
bar2.fill((255,0,0))
circ_sur = pygame.Surface((15,15))
circ = pygame.draw.circle(circ_sur,(0,255,0),(15/2,15/2),15/2)
circle = circ_sur.convert()
circle.set_colorkey((0,0,0))

# some definitions
bar1_x, bar2_x = 10. , 620.
bar1_y, bar2_y = 215. , 215.
circle_x, circle_y = 307.5, 232.5
bar1_move, bar2_move = 0. , 0.
speed_x, speed_y, speed_circ = 125., 125., 125.
bar1_score, bar2_score = 0,0
# clock and font objects
clock = pygame.time.Clock()
font = pygame.font.SysFont("calibri",40)


winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)


while True:

  img = cam.read()[1]
  img = cv2.flip(img,1)
  detectorImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  hands1 = cascade.detectMultiScale(
      detectorImg[:,:camW/2],
      scaleFactor=1.1,
      minNeighbors=3,
      minSize=(20,30),
      flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
  )
  hands2 = cascade.detectMultiScale(
      detectorImg[:,camW/2:],
      scaleFactor=1.1,
      minNeighbors=3,
      minSize=(20,30),
      flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
  )



  new_positions_1,dev1,avgH1Tmp = findNext(hands1,player1,positions_array_1,True)
  
  cv2.line(img,(dev1[0],0),(dev1[0],480),(255,0,0),thickness =2)
  cv2.line(img,(dev1[1],0),(dev1[1],480),(255,0,0),thickness =2)

  positions_array_1.append(new_positions_1)
  if(len(positions_array_1)>LAST_CNT):
    positions_array_1 = positions_array_1[1:]
  
  
  new_positions_2,dev2,avgH2Tmp = findNext(hands2,player2,positions_array_2,False)

  cv2.line(img,(dev2[0],0),(dev2[0],480),(0,0,255),thickness =2)
  cv2.line(img,(dev2[1],0),(dev2[1],480),(0,0,255),thickness =2)

  positions_array_2.append(new_positions_2)
  if(len(positions_array_2)>LAST_CNT):
    positions_array_2 = positions_array_2[1:]


  #print dev1,dev2

  i = 0
  for positions in positions_array_1 + positions_array_2:
    i +=INC_COLOR
    print_positions(positions,(0,0,i),img)
  
  print_positions([player1],(255,0,0),img)
  print_positions([player2],(255,0,0),img)
  #print_vectors(dt_01_positions,(0,0,255),img)

  cv2.imshow( winName, img )

  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break



  if avgH1Tmp:
    new = ((avgH1Tmp-camH/2)*1.4)+camH/2
    if new>avgH1 + MAX_MOV:
      avgH1 += MAX_MOV
    elif new<avgH1 - MAX_MOV:
      avgH1-=MAX_MOV
    else:
      avgH1 = new

  if avgH2Tmp:
    new = ((avgH2Tmp-camH/2)*1.4)+camH/2
    if new>avgH2 + MAX_MOV:
      avgH2 += MAX_MOV
    elif new<avgH2 - MAX_MOV:
      avgH2-=MAX_MOV
    else:
      avgH2 = new
  

  #prikazivanje rezultata i ostale funkcionalnosti igre

  score1 = font.render(str(bar1_score), True,(255,255,255))
  score2 = font.render(str(bar2_score), True,(255,255,255))

  screen.blit(background,(0,0))
  frame = pygame.draw.rect(screen,(255,255,255),Rect((5,5),(630,470)),2)
  middle_line = pygame.draw.aaline(screen,(255,255,255),(330,5),(330,475))
  screen.blit(bar1,(bar1_x,bar1_y))
  screen.blit(bar2,(bar2_x,bar2_y))
  screen.blit(circle,(circle_x,circle_y))
  screen.blit(score1,(250.,210.))
  screen.blit(score2,(380.,210.))

  bar1_y = avgH1

  # movement of circle
  time_passed = clock.tick(30)
  time_sec = time_passed / 1000.0

  circle_x += speed_x * time_sec
  circle_y += speed_y * time_sec
  ai_speed = speed_circ * time_sec
  #AI of the computer.
  bar2_y = avgH2

  if bar1_y >= 480. - BAR_HEIGHT/2: bar1_y = 480. - BAR_HEIGHT/2
  elif bar1_y <= 10. : bar1_y = 10.
  if bar2_y >= 480. - BAR_HEIGHT/2: bar2_y = 480. - BAR_HEIGHT/2
  elif bar2_y <= 10.: bar2_y = 10.
  #since i don't know anything about collision, ball hitting bars goes like this.
  if circle_x <= bar1_x + 10.:
      if circle_y >= bar1_y - 7.5 and circle_y <= bar1_y + (BAR_HEIGHT-7.5):
          circle_x = 20.
          speed_x = -speed_x
  if circle_x >= bar2_x - 15.:
      if circle_y >= bar2_y - 7.5 and circle_y <= bar2_y + (BAR_HEIGHT-7.5):
          circle_x = 605.
          speed_x = -speed_x
  if circle_x < 5.:
      bar2_score += 1
      circle_x, circle_y = 320., 232.5
      bar1_y,bar_2_y = 215., 215.
  elif circle_x > 620.:
      bar1_score += 1
      circle_x, circle_y = 307.5, 232.5
      bar1_y, bar2_y = 215., 215.
  if circle_y <= 10.:
      speed_y = -speed_y
      circle_y = 10.
  elif circle_y >= 457.5:
      speed_y = -speed_y
      circle_y = 457.5

  pygame.display.update()
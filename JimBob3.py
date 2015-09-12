#!/usr/bin/env python

""" 
  Core code for Hexapod         
  Copyright (c)  2015 Andrew Creahan.  All rights reserved.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation,
  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import sys, time, os
sys.path.append('/home/hexy/JimBob/Lidar-Lite/python')
import serial     
import RPi.GPIO as GPIO
import SerialOut
import PServo
import config
import pygame
import numpy
from espeak import espeak
from threading import Thread
from lidar_lite import Lidar_Lite
lidar = Lidar_Lite()
#from AnaSensorData import readsensor
import PServo
GPIO.setmode(GPIO.BCM)
resetpin = 13
GPIO.setup(resetpin, GPIO.OUT)
#matrix for Lidar Data
ldata = numpy.zeros((4, 9),dtype=numpy.int)
#Some random variables
a = 0
s = 0
l = 0
r = 0
start_time = time.time()
delay = 0.1  # set rest time between command sends
checksum = 0



print ("Hello")

def play(file,*args):
  pygame.mixer.init()
  pygame.mixer.music.load(file)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
      continue
      
def startup():
    Thread(target=play, args=("/home/hexy/git/JimBob2/Python/Sounds/r2d2.ogg",1)).start()
    reset()
    
    rise()
    
def rise():
    x = 0
    while x < 10:
       SerialOut.translate(0,0,90)
       time.sleep(0.1)
       x +=1
    x = 0
    SerialOut.rotate(90,0,0)
    SerialOut.wait(10)                        
    SerialOut.rotate(-90,0,0)                     
    SerialOut.wait(10) 
    while x < 10:
       SerialOut.translate(0,0,-90)
       time.sleep(0.1)
       x +=1
    

def reset():
  PServo.ResetServo()
  GPIO.output(resetpin, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(resetpin, GPIO.LOW)
  time.sleep(0.10)
  GPIO.output(resetpin, GPIO.HIGH)
  time.sleep(2)
#Travel = t then angle (0 - 360),speed (0 - 120),rotate (-100 - 100), repeat (0+)
#Rotate = r then left,right,up, repeat
#Translate = r then left,right,up, repeat


""" Startup """

startup()
connected = lidar.connect(1)
espeak.synth("Hello, Jim Bob ready to go")
c = 0
config.atrib['i_Gait'] = 0
SerialOut.wait(25)
print "here1"
#sensordata = readsensor()
priorread = time.time()+2
print "lidar"
print lidar
#print sensordata
lxpos = [2015,1915,1815,1715,1615,1515,1415,1315,1215]
lypos = [[1578,2067],[1613,2070],[1648,2090],[1683,2101],[1718,2113]]
espeak.synth("Clear the area")
lc = 0
ld = 0 
for ld in range (0,4):
   PServo.MoveServo(1,lypos[ld][1])
   PServo.MoveServo(0,lypos[ld][0])
   PServo.MoveServo(2,lxpos[lc])
   time.sleep(1)  
   for lc in range (0,9):
       try: 
           PServo.MoveServo(2,lxpos[lc])
           time.sleep(0.1)                                                                                                                    
           ldata[ld,lc] = lidar.getDistance()
       except IOError:
           print 'No lidar data'
       lc += 1
   lc = 0  
   ld += 1    
ld = 0
print ldata      

def walk(a):
    SerialOut.travel(a,100,0)
    setgait(5)
    print ('walk ', a)
    
def run(a):
    global s
    if s == 0:
      espeak.synth("I'm off for a run")
      s = 1  
    setgait(5)
    print ('run')
    SerialOut.travel(a,100,0)

def turnR():
    config.atrib['i_Gait'] = 0
    x = 0
    while x < 5:
           SerialOut.travel(0,0,90)
           print ('right')
           time.sleep(0.1)
           x +=1

def turnL():
    x = 0
    config.atrib['i_Gait'] = 0
    while x < 5:
           SerialOut.travel(0,0,-90)
           print ('left')
           time.sleep(0.1)
           x +=1  
          
                 
                  
while 1:  
  if lc < 8:
    lc += 1
  else:  
    lc =0
  print (ldata[lc],":", lc)  
  right = min(ldata[5:8])
  ahead = min(ldata[3:5])
  left = min(ldata[0:3])
      
  if ahead < 45 :
      if (left > 45) and (right > 45):
         a  = left - right
         if (a > 90):
           a = 90
         elif (a < -90):
           a = 270
         elif (a < 0):
           a = 360 + a  
  elif min(ldata) > 60:
     run(a)
  else: 
      walk (a)                
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
         
  if min(ldata)> 65:
      run(0)
      view = 0
  elif min(ldata) > 45:
      a = 0
      if (min(ldata[0:3]) < 25):
         #PServo.LookR()
         a = (min(ldata[5:8]) - min(ldata[0:3]))
         if (a > 360):
           a = 360
         elif (a < 0):
            a = 0  
      elif (min(ldata[5:8]) < 25):
         #PServo.LookR()
         lc = 8
         a = 360 - (min(ldata[0:3]) - min(ldata[5:8]))
         if (a > 360):
           a = 360
         elif (a < 0):
            a = 0  
         turnL()
  elif (min(ldata[0:3]) < 25):
       if l == 0:
         espeak.synth("Stuff to my right")
         l = 1  
       turnL()
  elif (min(ldata[5:8]) < 25):
      if r == 0:
         espeak.synth("Danger to the left")
         r = 1  
      turnR() 
  else: 
      espeak.synth("I see trouble ahead")
      turnL()                   
  

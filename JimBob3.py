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
from HMCmag import hmcmag
lidar = Lidar_Lite()
from AnaSensorData import readsensor
import PServo
GPIO.setmode(GPIO.BCM)
resetpin = 13
GPIO.setup(resetpin, GPIO.OUT)
#matrix for Lidar Data
ldata = numpy.zeros((4, 9),dtype=numpy.int)
#Some random variables
targetheading = 0
currentheading = 0 
#heading deadzone
headingzone = 20
a = 0
s = 0
l = 0
r = 0
priorturn = 'n'
start_time = time.time()
turn_time = time.time()
delay = 0.1  # set rest time between command sends
checksum = 0


def play(file,*args):
  pygame.mixer.init()
  pygame.mixer.music.load(file)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy() == True:
      continue
      
def startup():
    x = 0
    while x < 10:
       SerialOut.state(0,0,1)
       time.sleep(0.1)
       x +=1
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
  time.sleep(0.1)
  GPIO.output(resetpin, GPIO.HIGH)
  time.sleep(2)
                            
                 
""" Startup """

startup()
connected = lidar.connect(1)
espeak.synth("Hello, Jim Bob ready to go")
c = 0
SerialOut.setgait(0)
SerialOut.wait(25)
SerialOut.state(0,0,1)

sensordata = readsensor()
priorread = time.time()+2
print "lidar"
print lidar
print sensordata
lxpos = [2015,1915,1815,1715,1615,1515,1415,1315,1215]
lypos = [[1578,2067],[1613,2070],[1648,2090],[1683,2101],[1718,2113]]
espeak.synth("Clear the area")
lc = 0
ld = 0 
#for ld in range (0,4):
#   PServo.MoveServo(1,lypos[ld][1])
#   PServo.MoveServo(0,lypos[ld][0])
#   PServo.MoveServo(2,lxpos[lc])
#   time.sleep(1)  
#   for lc in range (0,9):
#       try: 
#           PServo.MoveServo(2,lxpos[lc])
#           time.sleep(0.1)                                                                                                                    
#           ldata[ld,lc] = lidar.getDistance()
#       except IOError:
#           print 'No lidar data'
#       lc += 1
#   lc = 0  
#   ld += 1    
#ld = 0
#print ldata
#left = ldata[0:,:2]
#right = ldata[0:,7:]
#centre = ldata[0:,3:6]
##print (left)
#leftm =  numpy.amin(left)
##print (centre)                        
#centrem = numpy.amin(centre)
##print (right)                        
#rightm= numpy.amin(right)



def walk(a):
    SerialOut.travel(a,100,0)
    SerialOut.setgait(5)
    print ('walk ', a)
    
def run(a):
    global s
    if s == 0:
      espeak.synth("I'm off for a run")
      s = 1  
    SerialOut.setgait(5)
    print ('run')
    SerialOut.travel(a,100,0)

def turnR():
    x = 0
    while x < 3:
           SerialOut.travel(0,0,90)
           print ('right')
           time.sleep(0.1)
           x +=1
    priorturn = 'r'
    turn_time = time.time()  

def turnL():
    x = 0
    while x < 3:
           SerialOut.travel(0,0,-90)
           print ('left')
           time.sleep(0.1)
           x +=1  
    priorturn = 'l'
    turn_time = time.time()         
           
def test():
  SerialOut.wait(1)
  while (1):
    for g in range (0,5):
        SerialOut.setgait(g)
        print("gait: ")
        print(g)
        while x < 20:
           SerialOut.travel(0,100,0)
           time.sleep(0.1)
           x +=1  
        while x < 20:
           SerialOut.travel(180,100,0)
           time.sleep(0.1)
           x +=1          

targethdg = hmcmag.heading()              
                  
while 1:  
  sensordata = readsensor() 
  a = 0
  currentheading = hmcmag.heading()
  print ("current:",currentheading)
  print sensordata  
  while  (abs(currentheading - targethdg) > headingzone):
    print ("current:",currentheading,"  target:", targethdg)
    direction = min(int(abs(currentheading - targethdg)+20),100)
    SerialOut.travel(0,0,direction)
    time.sleep(0.1)
    currentheading = hmcmag.heading()
  if sensordata['F'] < 30 :
      if ((sensordata['LF'] > 45) and ((priorturn != 'l') or ((time.time() - turn_time ) > 20))): 
         turnL()
      elif ((sensordata['RF'] > 45) and ((priorturn != 'r') or ((time.time() - turn_time ) > 20))):  
         turnR()
      else:
         SerialOut.backup(90) 
  elif ((sensordata['RF'] > 45) and (sensordata['LF'] < 35)):
           a = 90
           walk(a)
  elif ((sensordata['LF'] > 45) and (sensordata['RF'] < 35)):         
           a = 270
           walk(a)         
  elif min(sensordata['F'],sensordata['LF'],sensordata['RF']) > 60:
     run(a)
  else: 
      walk (a)                

  
  
  
  
  
  
  
  
  
  
  

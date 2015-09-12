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
#import SerialOut
import config
import PServo
from espeak import espeak
from lidar_lite import Lidar_Lite
from AnaSensorData import readsensor
lidar = Lidar_Lite()
anasensor = readsensor()


a = 0
s = 0
l = 0
r = 0
lc=2
start_time = time.time()
delay = 0.1  # set rest time between command sends
checksum = 0
GPIO.setmode(GPIO.BCM)

def startup():
    PServo.ResetServo()
 #   SerialOut.wait(1)
    PServo.LookL()
 #   SerialOut.wait(1)
    PServo.LookR()
 #   SerialOut.wait(1)
    PServo.LookA()
    time.sleep(1)
    rise()
    
    
def rise():
    x = 0
    while x < 5:
  #     SerialOut.translate(0,0,90)
        time.sleep(0.1)
        x +=1
    x = 0    
    while x < 5:
   #     SerialOut.translate(0,0,-90)
        time.sleep(0.1)
        x +=1
    

def reset():
  #rise()
  pin = 13
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.HIGH)
  print ("reset")
  time.sleep(1)
  GPIO.output(pin, GPIO.LOW)
  time.sleep(1)
  GPIO.output(pin, GPIO.HIGH)

#walktest = [('t',0,75,0,30),('t',180,75,0,30),('t',90,100,0,20),('t',270,100,0,20),('t',45,50,0,30),('t',135,50,0,30),('t',0,0,50,10),('t',0,0,-50,30)]

def walk():
    if config.atrib['i_Gait'] != 0:
    #      SerialOut.wait(10)
          config.atrib['i_Gait'] = 0
     #     SerialOut.wait(10)
    #SerialOut.travel(a,100,0)
    print ('walk ', a)
    
def sneek():
    if config.atrib['i_Gait'] != 3:
     #     SerialOut.wait(10)
          config.atrib['i_Gait'] = 3
      #    SerialOut.wait(10)
    #SerialOut.travel(a,100,0)
    print ('sneek ', a)
    
def quick():
    if config.atrib['i_Gait'] != 5:
     #     SerialOut.wait(10)
          config.atrib['i_Gait'] = 5
      #    SerialOut.wait(10)
    #SerialOut.travel(a,100,0)
    print ('quick ', a)

def turnR():
    config.atrib['i_Gait'] = 0
    x = 0
    while x < 5:
     #      SerialOut.travel(0,0,90)
           print ('right')
           time.sleep(0.1)
           x +=1

def turnL():
    x = 0
    config.atrib['i_Gait'] = 0
    while x < 5:
      #     SerialOut.travel(0,0,-90)
           print ('left')
           time.sleep(0.1)
           x +=1         
                      


available_actions = {"walk": walk,
                     "turnR": turnR,
                     "turnL": turnL,
                     "rise": rise,
                     "sneek": sneek, 
                     "quick": quick
                     }

""" Startup """
reset()
time.sleep(0.5)
startup()

#Travel angle,speed,rotate
#Rotate left,right,up
#Translate left,right,up

connected = lidar.connect(1)
espeak.synth("Hello, Jim Bob ready to go")
c = 0
config.atrib['i_Gait'] = 0
#SerialOut.wait(5)
sensordata = readsensor()
priorread = time.time()
view = 0
ldata = [0,0,0,0,0]
lpos = [1312,1282,1252,1222,1192]

while 1:
  
  #'RF','LF','FF','PX','PY','LR','DF','PR'
  
  rawdata = readsensor()
  PServo.MoveServo(5,lpos[lc])
  if lc < 4:
    lc += 1
  else:  
    lc =0
                                                                                                                             
  ldata[lc] = lidar.getDistance()
  print (ldata[lc],":", lc) 
  sensordata = { 
              "US" : int(rawdata[0]),
              "LF" : int(rawdata[1]),
              "RF" : int(rawdata[2])}
  print sensordata            
  if c > 50:
     s = 0
     l = 0
     r = 0
     c = 0
  c += 1  
  espeak.synth("Clear the area")
  
  if (ldata[3] > 65 and sensordata["LF"] > 40 and sensordata["RF"] > 40):
    a = 0
    action = 'quick'
    PServo.LookA()
    view = 0
  elif (ldata[3] > 50 and (sensordata['LF'] > 40 or sensordata ['RF'] > 40)):
    a = 0
    if (sensordata ['LF'] < 25):
       PServo.LookL()
       ldata[3]= lidar.getDistance()
       a = (sensordata['RF'] - sensordata ['LF'])
       if a > 360:
         a = 360
       elif a < 0:
          a = 0  
    elif (sensordata ['RF'] < 25):
       PServo.LookR()
       ldata[3]= lidar.getDistance()
       a = 360 - (sensordata['LF'] - sensordata ['RF'])
       if a > 360:
         a = 360
       elif a < 0:
          a = 0  
    if config.atrib['i_Gait'] != 0:
 #     SerialOut.wait(5)
      config.atrib['i_Gait'] = 0
  #    SerialOut.wait(5)
      print ("Gaitwait")
      action = 'walk'
  elif ((sensordata['RF'] > 25) and (sensordata['RF'] > 25)):
     if (sensordata['RF']  > sensordata['RF']):
         action = 'turnL'
         ldata[3]= lidar.getDistance()
     else:
         action = 'turnR'
         ldata[3]= lidar.getDistance()    
  elif (sensordata['RF'] < 25):
     if l == 0:
       espeak.synth("Stuff to my right")
       l = 1  
     action = 'turnL'
  elif (sensordata['LF'] < 25):
    if r == 0:
       espeak.synth("Danger to the left")
       r = 1  
    action = 'turnR'
  else: 
    a = 180 
    espeak.synth("I see trouble ahead")
    action = 'walk'                   
  try:
      available_actions[action]()
  except KeyError:
      print "Unrecognized command ", action
  except NameError:
      print "Unrecognized name ", action
  time.sleep(0.5)


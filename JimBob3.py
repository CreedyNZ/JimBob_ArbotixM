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
import serial_out
import p_servo
from navigate import nav
import config
import pygame
import numpy
from espeak import espeak
from threading import Thread
from lidar_lite import Lidar_Lite
lidar = Lidar_Lite()
import p_servo
GPIO.setmode(GPIO.BCM)
resetpin = 13
GPIO.setup(resetpin, GPIO.OUT)
#matrix for Lidar Data
ldata = numpy.zeros((4, 9),dtype=numpy.int)
#Some random variables
coords = config.coords

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
       serial_out.state(0,0,1)
       time.sleep(0.1)
       x +=1
    Thread(target=play, args=("/home/hexy/git/JimBob2/Python/Sounds/r2d2.ogg",1)).start()
    reset()
    rise()
    
    
def rise():
    x = 0
    while x < 10:
       serial_out.translate(0,0,90)
       time.sleep(0.1)
       x +=1
    x = 0
    serial_out.rotate(90,0,0)
    serial_out.wait(10)                        
    serial_out.rotate(-90,0,0)                     
    serial_out.wait(10) 
    while x < 10:
       serial_out.translate(0,0,-90)
       time.sleep(0.1)
       x +=1
    

def reset():
  p_servo.ResetServo()
  GPIO.output(resetpin, GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(resetpin, GPIO.LOW)
  time.sleep(0.1)
  GPIO.output(resetpin, GPIO.HIGH)
  time.sleep(2)
                            
                 
""" Startup """

startup()
connected = lidar.connect(1)
coords['i_TarPos'] = [20,20]
coords['i_CurPos'] = [1,1]
coords['offset'] = nav.offset()
susptime = time.time()
haz = 0 
temp = 0
espeak.synth("Hello, Jim Bob ready to go")
c = 0
serial_out.setgait(0)
serial_out.wait(25)
serial_out.state(0,0,1)
sensordata = readsensor()
priorread = time.time()+2
print sensordata
lxpos = [2015,1915,1815,1715,1615,1515,1415,1315,1215]
lypos = [[1578,2067],[1613,2070],[1648,2090],[1683,2101],[1718,2113]]
espeak.synth("Clear the area")
lc = 0
ld = 0





def walk(a):
    serial_out.travel(a,100,0)
    serial_out.setgait(5)
    print ('walk ', a)
    
def turn(t):
    serial_out.travel(0,100,t)
    print ('turn ', t)    
    
def run(a):
    global s
    if s == 0:
      espeak.synth("I'm off for a run")
      s = 1  
    serial_out.setgait(5)
    print ('run')
    serial_out.travel(a,100,0)

def turnR():
    x = 0
    while x < 3:
           serial_out.travel(0,0,90)
           print ('right')
           time.sleep(0.1)
           x +=1
    priorturn = 'r'
    turn_time = time.time()  

def turnL():
    x = 0
    while x < 3:
           serial_out.travel(0,0,-90)
           print ('left')
           time.sleep(0.1)
           x +=1  
    priorturn = 'l'
    turn_time = time.time()         
           
def test():
  serial_out.wait(1)
  while (1):
    for g in range (0,5):
        serial_out.setgait(g)
        print("gait: ")
        print(g)
        while x < 20:
           serial_out.travel(0,100,0)
           time.sleep(0.1)
           x +=1  
        while x < 20:
           serial_out.travel(180,100,0)
           time.sleep(0.1)
           x +=1          
             
                  
while 1:  
  nav.hdgchange
  walk(a)
  a = 0
  print sensordata  
  if sensordata['F'] < 30 :
      if ((sensordata['LF'] > 45) and ((priorturn != 'l') or ((time.time() - turn_time ) > 20))): 
         temp = -90
         nav.hdgchange(temp)
         susptime = time.time()
      elif ((sensordata['RF'] > 45) and ((priorturn != 'r') or ((time.time() - turn_time ) > 20))):  
         temp = 90
         nav.hdgchange(temp)
         susptime = time.time()
      else:
           haz +=1
           
           x=0
           while x < 3:     
               a = 180
               walk(a) 
               x +=1
           nav.hdgchange(temp)
           x=0
           while x < 4:     
               temp = 90
               nav.hdgchange(temp)
               susptime = time.time()
               x +=1
           x=0
           while x < 3:     
               a = 0
               walk(a) 
               x +=1           
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
  if haz > 3:
     haz = 0 
     if px >= 20:
        px = 1
     else: px += 5   
     if py >= 20:
        py = 1
     else: py += 10    
     coords['i_TarPos'] = [px,py]
  
  
  
  
  
  
  
  
  
  
  

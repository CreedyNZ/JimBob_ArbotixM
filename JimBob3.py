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
from navigate import move
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
targetradius = 2

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
coords['i_CurPos'] = [10,1]
nav.offset()
susptime = time.time()
haz = 0 
temp = 0
espeak.synth("Hello, Jim Bob ready to go")
c = 0
serial_out.setgait(0)
serial_out.wait(25)
serial_out.state(0,0,1)
priorread = time.time()+2
lxpos = [2015,1915,1815,1715,1615,1515,1415,1315,1215]
lypos = [[1578,2067],[1613,2070],[1648,2090],[1683,2101],[1718,2113]]
espeak.synth("Clear the area")
lc = 0
ld = 0

nav.offset()


             
nav.findtarget(10,10)            
while ((abs(coords['i_CurPos'][0]-coords['i_TarPos'][0])>targetradius) or (abs(coords['i_CurPos'][1]-coords['i_TarPos'][1])>targetradius)):  
  a = 0
  nav.findtarget(10,10)
nav.findtarget(20,10)   
while ((abs(coords['i_CurPos'][0]-coords['i_TarPos'][0])>targetradius) or (abs(coords['i_CurPos'][1]-coords['i_TarPos'][1])>targetradius)):  
  a = 0
  nav.findtarget(20,10)  
  
  
  
  
  
  
  
  
  
  
  

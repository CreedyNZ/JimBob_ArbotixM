#!/usr/bin/env python
from math import atan2,degrees
import numpy    
from HMCmag import hmcmag
import config
import serial_out
coords = config.coords

class Navigate:
    """ Class provide navigation services """
    def __init__(self,P_gain,D_gain, deadzone):
        self.D_gain = D_gain
        self.P_gain = P_gain
        self.deadzone = deadzone
        self.previous_error = 0
        self.grid = numpy.zeros((50, 50),dtype=numpy.int)
        
    def getangle(self,p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        return degrees(atan2(yDiff, xDiff))

    def odo (self,vel,ang):
        anglerad =  math.radians(ang)
        movex = math.cos (anglerad)* vel
        movey = math.sin (anglerad)* vel
        pv = [movex,movey]
        return pv
        
    def offset (self):
        currenthdg = hmcmag.heading()
        return currenthdg   
        
    
    def hdgchange(self,temp):
        currenthdg = hmcmag.heading()
        targethdg = self.getangle(coords['i_CurPos'],coords['i_TarPos'])+ coords['offset']+temp
        if targethdg > 360:
           targethdg = targethdg - 360
        print ("current:",currenthdg,"  target:", targethdg)
        error = targethdg - currenthdg
        while abs(error) > self.deadzone:
          currenthdg = hmcmag.heading()
          print ("current:",currenthdg,"  target:", targethdg)
          error = targethdg - currenthdg
          error_delta = error - self.previous_error
          if (abs(error)< self.deadzone):
              error = 0
          elif(error > 180):
              error = error -360
          elif (error < -180):
              error = error + 360
          error_delta = error - self.previous_error    
          self.previous_error = error
          if error > 0: 
             change = min(90,int(((error * self.P_gain + error_delta * self.D_gain)/100)+50))
          else:
               change = max(-90,int(((error * self.P_gain + error_delta * self.D_gain)/100)-50))
          print change
          serial_out.travel(0,0,change)
    
nav = Navigate(100,50,10)    
    

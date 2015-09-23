#!/usr/bin/env python
from math import atan2,degrees
import numpy    
from HMCmag import hmcmag

class Navigate:
    """ Class provide navigation services """
    def __init__(self,P_gain,D_gain, deadzone):
        self.D_gain = D_gain
        self.P_gain = P_gain
        self.deadzone = deadzone
        self.previous_error = 0
        self.grid = numpy.zeros((50, 50),dtype=numpy.int)
        
    def getangle(p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        return degrees(atan2(yDiff, xDiff))

    def odo (vel,ang):
        anglerad =  math.radians(ang)
        movex = math.cos (anglerad)* vel
        movey = math.sin (anglerad)* vel
        pv = [movex,movey]
        return pv
    
    def hdgchange():
        currenthdg = hmcmag.heading()
        targethdg = getangle(coords['i_CurPos'],coords['i_TarPos'])
        print ("current:",currenthdg,"  target:", targethdg)
        error = targethdg - currenthdg
        error_delta = error - previous_error
        if (abs(error)< deadzone):
            error = 0
        elif(error > 180):
            error = error -360
        elif (error < -180):
            error = error + 360
        previous_error = error
        change = ((error * P_gain + error_delta * D_gain)/100
        while change > 0
          serial_out.travel(0,0,change)
    
nav = Navigate(100,50,5)    
    

#!/usr/bin/env python
from math import atan2,degrees

class Navigate:
    """ Class provide navigation services """
    def __init__(self,P_gain,D_gain):
        self.D_gain = D_gain
        self.P_gain = P_gain
        self.previous_error = 0
        
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
    
    def hdgchange(Pc,Pt,heading):
        target = getangle(Pc,Pt)
        error = target - heading
        error_delta = error - previous_error
        if (abs(error)< deadzone):
            error = 0
        elif(error > 180):
            error = error -360
        elif (error < -180):
            error = error + 360
        previous_error = error
        change = ((error * P_gain + error_delta * D_gain)/100)
        return change
    
    

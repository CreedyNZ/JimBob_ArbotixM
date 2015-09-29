#!/usr/bin/env python
import sys, time
import math
import numpy    
import serial     
from HMCmag import hmcmag
import config
import serial_out
from HMCmag import hmcmag
from AnaSensorData import readsensor
from espeak import espeak
coords = config.coords

class Navigate:
    """ Class providing navigation services """
    def __init__(self,P_gain,D_gain, deadzone):
        self.D_gain = D_gain
        self.P_gain = P_gain
        self.deadzone = deadzone
        self.previous_error = 0
        self.grid = numpy.zeros((50, 50),dtype=numpy.int)
        self.gridhdg = 0
        self.haz = 0 
        self.temphdg = 0
        self.timer = time.time()
        # Front N,M,L - Left N,M - Right N,M
        self.frontobstacle = [False,False,False]
        self.leftobstacle = [False,False]
        self.rightobstacle = [False,False]
        
    def getangle(self,pC, pT):
        xDiff = pT[0] - pC[0]
        yDiff = pT[1] - pC[1]
        #print ("XYDiff: ", xDiff,":",yDiff)
        return math.degrees(math.atan2(xDiff, yDiff))

    def odo (self,vel, angle):
        direction = self.gridhdg + angle
        if direction > 360:
           direction -= 360
        elif direction < 0:
           direction += 360
        anglerad =  math.radians(self.gridhdg)
        movex = math.sin (anglerad)* vel/4
        movey = math.cos (anglerad)* vel/4
        #print (coords['i_CurPos'], movex,movey)
        coords['i_CurPos'][0] += movex
        coords['i_CurPos'][1] += movey
        #print (coords['i_CurPos'])
        return
        
    def offset (self):
        coords['i_Offset'] = - hmcmag.heading()
        time.sleep(0.5)
        print ('heading:  ',hmcmag.heading(), '  adj_heading:  ',hmcmag.adj_heading(), '  offset:  ',coords['i_Offset'])
        
    def hdgchange(self,temp,timer):
        currenthdg = hmcmag.adj_heading()
        if time.time()-timer > 5:
          temp = 0
        targethdg = self.getangle(coords['i_CurPos'],coords['i_TarPos']) + temp
        #print( coords['i_CurPos'],":",coords['i_TarPos'],":",temp)
        if targethdg > 360:
           targethdg -= 360
        if targethdg < 0:
           targethdg += 360   
        #print ("current:",currenthdg,"  target:", targethdg)
        error = targethdg - currenthdg
        while abs(error) > self.deadzone:
          currenthdg = hmcmag.adj_heading()
          #print ("current:",currenthdg,"  target:", targethdg)
          error = targethdg - currenthdg
          error_delta = error - self.previous_error
          if (abs(error)< self.deadzone):
              error = 0
          elif(error > 180):
              error -= 360
          elif (error < -180):
              error += 360
          error_delta = error - self.previous_error    
          self.previous_error = error
          if error > 0: 
             change = min(90,int(((error * self.P_gain + error_delta * self.D_gain)/100)+50))
          else:
               change = max(-90,int(((error * self.P_gain + error_delta * self.D_gain)/100)-50))
          #print change
          serial_out.travel(0,0,change)
        self.gridhdg = currenthdg 
          
    def obstacle(self):
        sensordata = readsensor()
        self.clear={'F1':False,'F2':False,'F3':False,'L1':False,'L2':False,'R1':False,'R2':False}
        if sensordata['F'] > 30 :
            self.clear['F1'] = True
        if sensordata['F'] > 45 :
            self.clear['F2'] = True   
        if sensordata['F'] > 60 :
            self.clear['F3'] = True    
        if sensordata['LF'] > 35 :
            self.clear['L1'] = True 
        if sensordata['LF'] > 45 :
            self.clear['L2'] = True     
        if sensordata['RF'] > 35 :
            self.clear['R1'] = True 
        if sensordata['RF'] > 45 :
            self.clear['R2'] = True                                                                                                                
        return (self.clear)
        
    def findtarget(self,xT,yT):
        coords['i_TarPos'] = [xT,yT]
        self.hdgchange(self.temphdg,self.timer)
        print self.obstacle()
        clear = self.obstacle()
        if (clear['F3'] and clear['L2'] and clear['R2']):
           move.run(0)
        elif (clear['F2']  and clear['L2'] and clear['R2']):
           move.walk(0)  
        elif (clear['F1']): 
             if (clear['L2'] or clear['L1']): 
                  move.walk(270)
             elif (clear['R2'] or clear['R1']): 
                  move.walk(90)    
             else: 
                  move.walk(165)     
        else:          
             temphdg = 0
             self.timer = time.time()
             self.hdgchange(self.temphdg,self.timer)
             move.walk(165)
             
#    def lidarscan(self):
#        
#        
#        x = (code[i])*math.cos(((i*100/length))* (3.14159 / 180))
#		    y =(code[i])*math.sin(((i*100/length))* (3.14159 / 180))
#		    print str(i+startingAngle)+"\t"+str((code[i]))+"\t"+str(x) +"\t"+str(y) # print in cartesian coordinates for plotting or graphing
#        
#        for ld in range (0,4):
#           p_servo.MoveServo(1,lypos[ld][1])
#           p_servo.MoveServo(0,lypos[ld][0])
#           p_servo.MoveServo(2,lxpos[lc])
#           time.sleep(1)  
#           for lc in range (0,9):
#               try: 
#                   p_servo.MoveServo(2,lxpos[lc])
#                   time.sleep(0.1)                                                                                                                    
#                   ldata[ld,lc] = lidar.getDistance()
#               except IOError:
#                   print 'No lidar data'
#               lc += 1
#           lc = 0  
#           ld += 1    
#        ld = 0
#        print ldata
#        left = ldata[0:,:2]
#        right = ldata[0:,7:]
#        centre = ldata[0:,3:6]
#        #print (left)
#        leftm =  numpy.amin(left)
#        #print (centre)                        
#        centrem = numpy.amin(centre)
#        #print (right)                        
#        rightm= numpy.amin(right)
#        return {'l_front':self.frontobstacle,'left':self.leftobstacle,'right':self.rightobstacle} 
           
class Move:
    """ Class providing movement services """
    def __init__(self):
        self.a = 0
        self.s_run = 0
        self.l = 0
        self.r = 0
        self.priorturn = 'n'
        self.start_time = time.time()
        self.turn_time = time.time()
        
    def commit(self):
        stdpkt.sendpkt()
        
    def walk(self,ang,gait):
        serial_out.setgait(gait)
        serial_out.state(0,0,1)
        serial_out.travel(ang,100,0)
        nav.odo(1,ang)
        print ('walk ', ang)
    
    def turn(self,t):
        serial_out.travel(0,100,t)
        self.commit()
        print ('turn ', t)    
        
    def run(self,ang,gait):
        if self.s_run == 0:
          espeak.synth("I'm off for a run")
          self.s_run = 1  
        serial_out.setgait(gait)  
        serial_out.state(0,1,1)
        nav.odo(1.5,ang)
        print ('run')
        serial_out.travel(ang,100,0)
    
    def turnR(self):
        x = 0
        while x < 3:
               serial_out.travel(0,0,90)
               self.commit()
               print ('right')
               time.sleep(0.1)
               x +=1
        priorturn = 'r'
        turn_time = time.time()  
    
    def turnL(self):
        x = 0
        while x < 3:
               serial_out.travel(0,0,-90)
               self.commit()
               print ('left')
               time.sleep(0.1)
               x +=1  
        priorturn = 'l'
        turn_time = time.time()                  
    
nav = Navigate(100,50,10)    
move = Move()    

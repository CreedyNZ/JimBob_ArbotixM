#!/usr/bin/env python
from math import atan2,degrees
import numpy    
from HMCmag import hmcmag
import config
import serial_out
from HMCmag import hmcmag
from AnaSensorData import readsensor
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
        # Front N,M,L - Left N,M - Right N,M
        self.frontobstacle = [False,False,False]
        self.leftobstacle = [False,False]
        self.rightobstacle = [False,False]
        
    def getangle(self,p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        return degrees(atan2(yDiff, xDiff))

    def odo (self,vel, angle):
        direction = self.gridhdg + a
        if direction > 360:
           direction -= 360
        elif direction < 0:
           direction += 360
        anglerad =  math.radians(self.gridhdg)
        movex = math.cos (anglerad)* vel
        movey = math.sin (anglerad)* vel
        print (coords['i_CurPos'], movex,movey)
        coords['i_CurPos'] += [movex,movey]
        print (coords['i_CurPos'])
        return
        
    def offset (self):
        currenthdg = hmcmag.heading()
        return currenthdg   
        
    
    def hdgchange(self,temp):
        currenthdg = hmcmag.heading()
        targethdg = self.getangle(coords['i_CurPos'],coords['i_TarPos'])+ coords['offset']+temp
        if targethdg > 360:
           targethdg -= 360
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
              error -= 360
          elif (error < -180):
              error += 360
          error_delta = error - self.previous_error    
          self.previous_error = error
          if error > 0: 
             change = min(90,int(((error * self.P_gain + error_delta * self.D_gain)/100)+50))
          else:
               change = max(-90,int(((error * self.P_gain + error_delta * self.D_gain)/100)-50))
          print change
          serial_out.travel(0,0,change)
        self.gridhdg = currenthdg - coords['offset']
        if self.gridhdg < 0:
           self.gridhdg = self.gridhdg + 360  
          
    def obstacle(self):
        sensordata = readsensor()
        if sensordata['F'] < 30 :
            frontobstacle[False,False,False]
        elif sensordata['F'] < 45 :
            frontobstacle[True,False,False]    
        elif sensordata['F'] < 60 :
            frontobstacle[True,True,False]    
        else:
            frontobstacle[True,True,True]
        if sensordata['LF'] < 35 :
            leftobstacle[False,False]
        elif sensordata['LF'] < 45 :
            leftobstacle[True,False]    
        else:
            leftobstacle[True,True]    
        if sensordata['RF'] < 35 :
            rightobstacle[False,False]
        elif sensordata['RF'] < 45 :
            rightobstacle[True,False]    
        else:
            rightobstacle[True,True]     
        return {'front':frontobstacle,'left':leftobstacle,'right':rightobstacle}
    
    def lidarscan(self):
        
        
                x = (code[i])*math.cos(((i*100/length)+coords['offset'])* (3.14159 / 180))
		y =(code[i])*math.sin(((i*100/length)+coords['offset'])* (3.14159 / 180))
		print str(i+startingAngle)+"\t"+str((code[i]))+"\t"+str(x) +"\t"+str(y) # print in cartesian coordinates for plotting or graphing
        
        for ld in range (0,4):
           p_servo.MoveServo(1,lypos[ld][1])
           p_servo.MoveServo(0,lypos[ld][0])
           p_servo.MoveServo(2,lxpos[lc])
           time.sleep(1)  
           for lc in range (0,9):
               try: 
                   p_servo.MoveServo(2,lxpos[lc])
                   time.sleep(0.1)                                                                                                                    
                   ldata[ld,lc] = lidar.getDistance()
               except IOError:
                   print 'No lidar data'
               lc += 1
           lc = 0  
           ld += 1    
        ld = 0
        print ldata
        left = ldata[0:,:2]
        right = ldata[0:,7:]
        centre = ldata[0:,3:6]
        #print (left)
        leftm =  numpy.amin(left)
        #print (centre)                        
        centrem = numpy.amin(centre)
        #print (right)                        
        rightm= numpy.amin(right)
        return {'l_front':self.frontobstacle,'left':self.leftobstacle,'right':self.rightobstacle} 
           
class Travel(self):
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
        
    def walk(self,a):
        serial_out.setgait(0)
        serial_out.state(0,0,1)
        serial_out.travel(a,100,0)
        self.commit()
        nav.odo(1,a)
        print ('walk ', a)
    
    def turn(self,t):
        serial_out.travel(0,100,t)
        self.commit()
        print ('turn ', t)    
        
    def run(self,a):
        if self.s_run == 0:
          espeak.synth("I'm off for a run")
          self.s_run = 1  
        serial_out.setgait(5)
        serial_out.state(0,1,1)
        print ('run')
        serial_out.travel(a,100,0)
        self.commit()
    
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
travel = Travel()    

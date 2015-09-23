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
from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import sys, time, os

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 12)
dist_ana = [0,0,0]


def readsensor():
  averagel = 0
  averager = 0
  #print ("Here3")
  raw = adc.read_voltage(7)/ 0.009766 #Read Sonar
  distance = raw * 2.54
  dist_ana[0] = int(distance)
  
  #Get a sampling of 5 readings from sensor
  for i in range (0,4):
    raw = adc.read_voltage(6)
    distancel = 27.86 * pow(raw,-1.15)
    raw = adc.read_voltage(8)
    distancer = 27.86 * pow(raw,-1.15)
    averagel = averagel + distancel
    averager = averager + distancer
    time.sleep(0.2)
    
  dist_ana[1] = min(int (averagel / 5),56)
  dist_ana[2] = min(int (averager / 5),56)
  sensordata = {
              'F' : dist_ana[0],
              'LF' : dist_ana[2],
              'RF' : dist_ana[1]}
  

  return(sensordata)
  
  

                                          
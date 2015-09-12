import sys, time, os
import serial     
import RPi.GPIO as GPIO
import PServo
import config
from espeak import espeak
from lidar_lite import Lidar_Lite
#from AnaSensorData import readsensor
GPIO.setmode(GPIO.BCM)
print ("Hello")


while 1:
      GPIO.output(13, GPIO.LOW)
      print ("Low")
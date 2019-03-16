#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
import time

def drive(bs,f):
	mr = ev3.LargeMotor("outC")
	ml = ev3.LargeMotor("outB")
	cs = ev3.ColorSensor()
	cs.mode = "RGB-RAW"
	while True:
		#print(cs.bin_data("hhh"))
		colorsum = cs.bin_data("hhh")[0] + cs.bin_data("hhh")[1] + cs.bin_data("hhh")[2]
		print(colorsum)
		a = (250 - colorsum)/250
		if mesureColor(cs) is "red":
			mr.stop()
			ml.stop()
			break
		if mesureColor(cs) is "blue":
			mr.stop()
			ml.stop()
			break
		if colorsum <= 600:
			if a<0:
				mr.speed_sp = bs+bs*a*f
				ml.speed_sp = bs
			else:
				mr.speed_sp = bs
				ml.speed_sp = bs-bs*a*f
			mr.command = "run-forever"
			ml.command = "run-forever"
			time.sleep(0.1)
		
		if colorsum > 600: #Bob left the line
			Sound.tone([(1661,75,75),(1661,75,75),(2217,75,50),(1661,75,50)]).wait()
			findLine(cs, mr, ml)
	
	while mesureColor(cs) is "blue" or mesureColor(cs) is "red": #drive over the point
		mr.speed_sp = 100
		ml.speed_sp = 100
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(0.1)
		
	time.sleep(0.4)		#get wheels at the right position
	mr.stop()
	ml.stop()
	
	print (scanPoint(cs,mr,ml))
	

def scanPoint(cs, mr, ml):
	directionList = [[],[],[],[]]
	for i in range (4):
		if findLine(cs, mr, ml):
			directionList[i] = 1
		else:
			mr.speed_sp = 100
			ml.speed_sp = -100
			mr.command = "run-forever"
			ml.command = "run-forever"
			time.sleep(0.4)
			mr.stop()
			ml.stop()
		mr.speed_sp = 150
		ml.speed_sp = -150
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(1.3)
		mr.stop()
		ml.stop()
	return directionList
		
		

def findLine(cs, mr, ml):
	mr.stop()
	ml.stop()
	timecount = 0
	while timecount < 5:
		colorsum = colorsum = cs.bin_data("hhh")[0] + cs.bin_data("hhh")[1] + cs.bin_data("hhh")[2]
		if(colorsum < 250):
			timecount = -1000
			return True
			#break
		mr.speed_sp = 100
		ml.speed_sp = -100
		mr.command = "run-forever"
		ml.command = "run-forever"
		timecount += 1
		time.sleep(0.1)
	while timecount > -5:
		colorsum = colorsum = cs.bin_data("hhh")[0] + cs.bin_data("hhh")[1] + cs.bin_data("hhh")[2]
		if(colorsum < 250):
			timecount = -1000
			return True
			#break
		mr.speed_sp = -100
		ml.speed_sp = 100
		mr.command = "run-forever"
		ml.command = "run-forever"
		timecount -= 1
		time.sleep(0.1)
	return False
		
def mesureColor(cs):
	if cs.bin_data("hhh")[0] > cs.bin_data("hhh")[2] * 3:
		return "red"
	elif cs.bin_data("hhh")[2] > cs.bin_data("hhh")[0] * 3:
		return "blue"
	else:
		return "no color"
#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters


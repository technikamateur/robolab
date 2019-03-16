#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
import time

def drive(bs,f):					#Main driving method
	mr = ev3.LargeMotor("outC")		#Initializing sensors and motors
	ml = ev3.LargeMotor("outB")
	cs = ev3.ColorSensor()
	cs.mode = "RGB-RAW"
	
	while True:						#Feedback-Loop
		colorsum = cs.bin_data("hhh")[0] + cs.bin_data("hhh")[1] + cs.bin_data("hhh")[2]	#Brightness
		#print(colorsum)
		a = (250 - colorsum)/250	#Proportional-factor
		if mesureColor(cs) is "red":	#Colormesurement to find connection points
			mr.stop()
			ml.stop()
			break
		if mesureColor(cs) is "blue":
			mr.stop()
			ml.stop()
			break
		if colorsum <= 600:			#Bob is near the white/black line
			if a<0:
				mr.speed_sp = bs+bs*a*f
				ml.speed_sp = bs
			else:
				mr.speed_sp = bs
				ml.speed_sp = bs-bs*a*f
			mr.command = "run-forever"
			ml.command = "run-forever"
			time.sleep(0.1)
			print (mr.speed, ml.speed)
		
		if colorsum > 600: 			#Bob left the line
			Sound.tone([(1661,75,75),(1661,75,75),(2217,75,50),(1661,75,50)]).wait()
			findLine(cs, mr, ml)
	
	while mesureColor(cs) is "blue" or mesureColor(cs) is "red": #drive over the point
		mr.speed_sp = 100
		ml.speed_sp = 100
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(0.1)
		
	time.sleep(0.4)					#get wheels to the right position
	mr.stop()
	ml.stop()
	
	print (scanPoint(cs,mr,ml))
	
def scanPoint(cs, mr, ml):			#returns list with point-directions
	directionList = [[],[],[],[]]
	for i in range (4):
		if findLine(cs, mr, ml):
			directionList[i] = 1
		else:
			mr.speed_sp = 100
			ml.speed_sp = -100
			mr.command = "run-forever"
			ml.command = "run-forever"
			time.sleep(0.5)
			mr.stop()
			ml.stop()
		mr.speed_sp = 100
		ml.speed_sp = -100
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(1.85)
		mr.stop()
		ml.stop()
	if not findLine(cs, mr, ml):
		mr.speed_sp = 100
		ml.speed_sp = -100
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(0.5)
		mr.stop()
		ml.stop()
	return directionList
		
def findLine(cs, mr, ml):			#returns wheather a line was found
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
		
def mesureColor(cs):				#returns "red" or "blue"
	if cs.bin_data("hhh")[0] > cs.bin_data("hhh")[2] * 2.7:
		return "red"
	elif cs.bin_data("hhh")[2] > cs.bin_data("hhh")[0] * 2.7:
		return "blue"
	else:
		return "no color"
#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters


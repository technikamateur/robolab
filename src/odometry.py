#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
import time
import math
#wheel diameter: 5,5 cm

def drive(bs,f):					#Main driving method
	mr = ev3.LargeMotor("outC")		#Initializing sensors and motors
	ml = ev3.LargeMotor("outB")
	cs = ev3.ColorSensor()
	cs.mode = "RGB-RAW"
	speedListL = []
	speedListR = []
	timeList = []
	
	
	while True:						#Feedback-Loop
		start = time.time()
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
			end = time.time()
			#print (mr.speed, ml.speed)
			speedListR.append(mr.speed)
			speedListL.append(ml.speed)
			timeList.append(end-start)
		
		if colorsum > 580: 			#Bob left the line
			Sound.tone([(1661,75,75),(1661,75,75),(2217,75,50),(1661,75,50)]).wait()
			start += findLine(cs, mr, ml)[1]
			
	
	
	while mesureColor(cs) is "blue" or mesureColor(cs) is "red": #drive over the point
		mr.speed_sp = 100
		ml.speed_sp = 100
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(0.1)
		
	time.sleep(0.4)					#get wheels to the right position
	mr.stop()
	ml.stop()
	
	#print (scanPoint(cs,mr,ml))
	
	sum = 0
	timesum = 0
	for i in range(len(speedListR)):
		sum += (speedListR[i]+speedListL[i])/2
		timesum += timeList[i]
	v = sum / len(speedListR)
	print ("v:",v,"time:",timesum,"dist:",calculateDistance(v,timesum), "Winkel:", mesureDistance(speedListR, speedListL, timeList))
	
def scanPoint(cs, mr, ml):			#returns list with point-directions
	directionList = [[],[],[],[]]
	for i in range (4):
		if findLine(cs, mr, ml)[0]:
			directionList[i] = True
		else:						#turn back to the middle if no line was found
			directionList[i] = False
			mr.speed_sp = 75
			ml.speed_sp = -75
			mr.command = "run-forever"
			ml.command = "run-forever"
			time.sleep(0.8)
			mr.stop()
			ml.stop()
		turn_by_degree(90,100)
		mr.stop()
		ml.stop()
	if not findLine(cs, mr, ml)[0]:
		mr.speed_sp = 75
		ml.speed_sp = -75
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(0.8)
		mr.stop()
		ml.stop()
	return directionList
		
def findLine(cs, mr, ml):			#returns whether a line was found
	mr.stop()
	ml.stop()
	timecount = 0
	start = time.time()
	
	print ("New Mesurement")
	while timecount < 15:
		colorsum = colorsum = cs.bin_data("hhh")[0] + cs.bin_data("hhh")[1] + cs.bin_data("hhh")[2]
		print("Turn left",colorsum)
		if(colorsum < 240):
			end = time.time()
			return True, end-start
		mr.speed_sp = 75
		ml.speed_sp = -75
		mr.command = "run-forever"
		ml.command = "run-forever"
		timecount += 1
		time.sleep(0.05)
	while timecount > -15:
		colorsum = colorsum = cs.bin_data("hhh")[0] + cs.bin_data("hhh")[1] + cs.bin_data("hhh")[2]
		print("Turn right",colorsum)
		if(colorsum < 240):
			end = time.time()
			return True, end - start
		mr.speed_sp = -75
		ml.speed_sp = 75
		mr.command = "run-forever"
		ml.command = "run-forever"
		timecount -= 1
		time.sleep(0.05)
	end = time.time()
	return False, end - start
		
def mesureColor(cs):				#returns "red" or "blue"
	if cs.bin_data("hhh")[0] > cs.bin_data("hhh")[2] * 2.7:
		return "red"
	elif cs.bin_data("hhh")[2] > cs.bin_data("hhh")[0] * 2.7:
		return "blue"
	else:
		return "no color"
		
def calculateDistance(v, t):		#returns distance in cm, uses average speed 
	return v*(11/720)*math.pi*t + 3 #+3 to counter position
	
def turn_by_degree(deg, bs):
	d = 12
	mr = ev3.LargeMotor("outC")		
	ml = ev3.LargeMotor("outB")
	rot = (deg * 12 *2)/11 
	t = rot/bs
	start = time.time()
	mr.speed_sp = bs-(bs*0.09)
	ml.speed_sp = -(bs-(bs*0.09))
	mr.command = "run-forever"
	ml.command = "run-forever"
	time.sleep(t)
	mr.stop()
	ml.stop()
	end = time.time()
	print (t, end-start)

def mesureDistance(speedListR, speedListL, timeList):
	d_wheel = 5.6
	u_wheel = d_wheel * math.pi
	v_byDeg = u_wheel / 360
	d_axis = 12
	degsum = 0
	deltaX = 0
	deltaY = 0
	
	for i in range(len(speedListR)):
		vl = speedListL[i] * v_byDeg
		vr = speedListR[i] * v_byDeg
		if vl == vr:
			beta = 0
			dx = 0
			dy = vl * timeList[i]
		else:
			alpha = timeList[i] * (vr-vl) / d_axis
			beta = alpha / 2
			s = timeList[i] * (vr + vl) / alpha * math.sin(beta)
			dx = - math.sin(degsum + beta) * s
			dy = math.cos(degsum + beta) * s
		deltaX += dx
		deltaY += dy
		degsum += alpha
	print (deltaX, deltaY)
	return degsum
		
			
		
#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters


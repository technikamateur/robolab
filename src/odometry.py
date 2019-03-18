#!/usr/bin/env python3
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
import time
import math
from planet import Direction

class Robot:
	def __init__(self):
		self.mr = ev3.LargeMotor("outC")	#Initializing sensors and motors
		self.ml = ev3.LargeMotor("outB")
		self.cs = ev3.ColorSensor()
		#self.cs.mode = "RGB-RAW"
		self.d_wheel = 5.6
		self.d_axis = 12
		self.position = [0,0]
		self.view = Direction.NORTH
		self.speedListL = []
		self.speedListR = []
		self.timeList = []
		self.directionList = []

	def drive(self, bs, f):				#main driving method	
		self.cs.mode = "RGB-RAW"
		self.speedListL = []
		self.speedListR = []
		self.timeList = []
		self.directionList = []
	
		while True:						#Feedback-Loop
			start = time.time()
			colorsum = self.cs.bin_data("hhh")[0] + self.cs.bin_data("hhh")[1] + self.cs.bin_data("hhh")[2]	#Brightness
			#print(colorsum)
			a = (250 - colorsum)/250	#Proportional-factor
			if self.mesureColor() is "red":	#Colormesurement to find connection points
				self.mr.stop()
				self.ml.stop()
				break
			if self.mesureColor() is "blue":
				self.mr.stop()
				self.ml.stop()
				break
			if colorsum <= 550:			#Bob is near the white/black line
				if a<0:
					self.mr.speed_sp = bs+bs*a*f
					self.ml.speed_sp = bs
				else:
					self.mr.speed_sp = bs
					self.ml.speed_sp = bs-bs*a*f
				self.mr.command = "run-forever"
				self.ml.command = "run-forever"
				time.sleep(0.1)
				end = time.time()
				self.speedListR.append(self.mr.speed)
				self.speedListL.append(self.ml.speed)
				self.timeList.append(end-start)
			
			else: 			#Bob left the line
				Sound.tone([(1661,75,75),(1661,75,75),(2217,75,50),(1661,75,50)]).wait()
				start += self.findLine()
				
		while self.mesureColor() is "blue" or self.mesureColor() is "red": #drive over the point
			self.mr.speed_sp = 100
			self.ml.speed_sp = 100
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			time.sleep(0.1)
			
		time.sleep(0.5)					#get wheels to the right position
		self.mr.stop()
		self.ml.stop()
		
		directionList = self.scanPoint()
		print (directionList)
		
		new_angle = self.calculateAngleAndNewPosition()[0]
		print (self.direction_to_angle(Direction.NORTH))
		self.view = self.transformAngle(new_angle)
		print (self.view)
		
	def calculateAngleAndNewPosition(self):
		u_wheel = self.d_wheel * math.pi
		v_byDeg = u_wheel / 360
		degsum = 0
		deltaX = 0
		deltaY = 0
	
		for i in range(len(self.speedListR)):
			vl = self.speedListL[i] * v_byDeg
			vr = self.speedListR[i] * v_byDeg
			if vl == vr:
				beta = 0
				alpha = 0
				dx = 0
				dy = vl * self.timeList[i]
			else:
				alpha = self.timeList[i] * (vr-vl) / self.d_axis
				beta = alpha / 2
				s = self.timeList[i] * (vr + vl) / alpha * math.sin(beta)
				dx = - math.sin(degsum + beta) * s
				dy = math.cos(degsum + beta) * s
			deltaX += dx
			deltaY += dy
			degsum += alpha
		self.transformCoordinates(deltaX, deltaY)
		return degsum, deltaX, deltaY

	def turn_by_degree(self, deg, bs):
		rot_wheel = (deg * self.d_axis *2)/11
		t = rot_wheel / bs
		self.mr.speed_sp = bs-(bs*0.09)      #factor to counter inacuracy of the motor
		self.ml.speed_sp = -(bs-(bs*0.09))
		self.mr.command = "run-forever"
		self.ml.command = "run-forever"
		time.sleep(t)
		self.mr.stop()
		self.ml.stop()           
		
	def mesureColor(self):				#returns "red" or "blue"
		if self.cs.bin_data("hhh")[0] > self.cs.bin_data("hhh")[2] * 2.7:
			return "red"
		elif self.cs.bin_data("hhh")[2] > self.cs.bin_data("hhh")[0] * 2.7:
			return "blue"
		else:
			return "no color"

	def findLine(self, b = 250, bs = 75, timestamp = 15):	#returns whether a line was found
		self.mr.stop()
		self.ml.stop()
		timecount = 0
	
		while timecount < timestamp:
			colorsum = colorsum = self.cs.bin_data("hhh")[0] + self.cs.bin_data("hhh")[1] + self.cs.bin_data("hhh")[2]
			#print("Turn left",colorsum)
			if(colorsum < b):
				return True
			self.mr.speed_sp = bs
			self.ml.speed_sp = -bs
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			timecount += 1
			time.sleep(0.05)
		while timecount > -timestamp:
			colorsum =self.cs.bin_data("hhh")[0] + self.cs.bin_data("hhh")[1] + self.cs.bin_data("hhh")[2]
			#print("Turn right",colorsum)
			if(colorsum < b):
				return True
			self.mr.speed_sp = -bs
			self.ml.speed_sp = bs
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			timecount -= 1
			time.sleep(0.05)
		return False

	def scanPoint(self):				#returns list with point-directions
		directionList = [[],[],[],[]]
		for i in range (4):
			if self.findLine():
				directionList[i] = True
			else:						#turn back to the middle if no line was found
				directionList[i] = False
				self.mr.speed_sp = 75
				self.ml.speed_sp = -75
				self.mr.command = "run-forever"
				self.ml.command = "run-forever"
				time.sleep(0.8)
				self.mr.stop()
				self.ml.stop()
			self.turn_by_degree(90,100)
			self.mr.stop()
			self.ml.stop()
		if not self.findLine(150,40, 30):
			self.mr.speed_sp = 75
			self.ml.speed_sp = -75
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			time.sleep(0.8)
			self.mr.stop()
			self.ml.stop()
		return directionList

	def transformCoordinates(self, dx, dy):
		dx /= 50
		dy /= 50
		self.position[0] += round(dx)
		self.position[1] += round(dy)
		print (self.position)
	
	def transformAngle(self, angle):
		while angle >= 2 * math.pi:
			angle -= 2 * math.pi
		while angle < 0:
			angle += 2 * math.pi
		if angle <= math.pi * 1/4 or angle > math.pi * 7/4:
			return Direction.NORTH
		elif angle <= math.pi * 3/4 and angle > math.pi * 1/4:
			return Direction.WEST
		elif angle <= math.pi * 5/4 and angle > math.pi * 3/4:
			return Direction.SOUTH
		else:
			return Direction.EAST
	
	def direction_to_angle(self, direction):
		if direction is Direction.NORTH:
			return 0
		elif direction is Direction.WEST:
			return 90
		elif direction is Direction.SOUTH:
			return 180
		else:
			return 270
	
	"""def turn_by_direction(self, direction, dire):
		if direction = "N":
			if directionList[0]"""
		
		
#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters


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
		self.ts = ev3.TouchSensor()
		#self.cs.mode = "RGB-RAW"
		self.d_wheel = 5.6
		self.d_axis = 12
		self.oldposition = (0,0)
		self.position = (0,0)
		self.oldview = Direction.NORTH
		self.view = Direction.NORTH
		self.status = "free"
		self.speedListL = []
		self.speedListR = []
		self.timeList = []
		self.directionList = []

	def drive(self, bs = 100, kp = 1, ki = 0, kd = 0, gray = 250):	#main driving method
		self.cs.mode = "RGB-RAW"
		self.speedListL = []
		self.speedListR = []
		self.timeList = []
		self.directionList = []
		self.oldview = self.view
		self.oldposition = self.position
		self.status = "free"
		integral = 0
		lastError = 0
		derivative = 0
		start_control = time.time()

		while True:						#Feedback-Loop
			start = time.time()
			colorsum = self.mesureBrightness()
			#print(colorsum)
			error = (gray - colorsum)/gray			#Proportional-factor
			integral += error
			derivative = error - lastError
			turn = kp * error + ki * integral + kd * derivative
			#print (ki * integral)
			if self.mesureColor() is "red":	#Colormesurement to find connection points
				self.mr.stop()
				self.ml.stop()
				break
			if self.mesureColor() is "blue":
				self.mr.stop()
				self.ml.stop()
				break
			if self.ts.value() == 1:			#Touchsensor is pressed
				self.mr.speed_sp = - 100
				self.ml.speed_sp = - 100
				self.mr.command = "run-forever"
				self.ml.command = "run-forever"
				time.sleep(1.1)
				self.status = "blocked"
				self.turn_by_degree(180,100)
				self.findLine(150,40, 35)
				bs = 100
				kp = 1.0
				start_control = time.time()
			if colorsum <= 650:			#Bob is near the white/black line
				if colorsum > 420 or colorsum < 120:
					bs = 100
					kp = 1.0					#!!!!!!!!!!WARNING!!!!!!!!
					start_control = time.time()
				if time.time()-start_control > 4:
					bs = 170
					kp = 0.8
				if turn<0:
					self.mr.speed_sp = bs+bs*turn
					self.ml.speed_sp = bs#-bs*turn
				else:
					self.mr.speed_sp = bs#+bs*turn
					self.ml.speed_sp = bs-bs*turn
				self.mr.command = "run-forever"
				self.ml.command = "run-forever"
				time.sleep(0.1)
				end = time.time()
				#print (end-start)
				self.speedListR.append(self.mr.speed)
				self.speedListL.append(self.ml.speed)
				self.timeList.append(end-start)

			else: 			#Bob left the line
				Sound.tone([(3135.96,100,150),(3135.96,100,150),(3729.31,75,75),(3135.96,100,75)]).wait()
				self.findLine(230,75,30)


		while self.mesureColor() is "blue" or self.mesureColor() is "red": #drive over the point
			self.mr.speed_sp = 100
			self.ml.speed_sp = 100
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			time.sleep(0.1)

		time.sleep(0.5)					#get wheels to the right position
		self.mr.stop()
		self.ml.stop()

		new_angle = self.calculateAngleAndNewPosition()[0]
		self.view = self.angle_to_direction(new_angle)

	def calculateAngleAndNewPosition(self):					#Odometry-Function
		u_wheel = self.d_wheel * math.pi
		v_byDeg = u_wheel / 360
		degsum = self.direction_to_angle(self.view) *(2 * math.pi) / 360
		deltaX = 0
		deltaY = 0
		for i in range(len(self.speedListR)):
			vl = self.speedListL[i] * v_byDeg
			vr = self.speedListR[i] * v_byDeg
			alpha = self.timeList[i] * (vr-vl) / self.d_axis
			beta = alpha / 2
			if alpha == 0:
				s = vl * self.timeList[i]
			else:
				s = self.timeList[i] * (vr + vl) / alpha * math.sin(beta)
			dx = - math.sin(degsum + beta) * s
			dy = math.cos(degsum + beta) * s
			deltaX += dx
			deltaY += dy
			degsum += alpha
		self.transformCoordinates(deltaX, deltaY)
		return degsum, deltaX, deltaY

	def turn_by_degree(self, deg, bs = 100):				#Turns by the given degree
		if deg < 0:
			vz = -1
		else:
			vz = 1
		rot_wheel = (deg * self.d_axis *2)/11
		t = vz * rot_wheel / bs
		self.mr.speed_sp = vz * bs-(bs*0.09)      #factor to counter inacuracy of the motor
		self.ml.speed_sp = -vz * (bs-(bs*0.09))
		self.mr.command = "run-forever"
		self.ml.command = "run-forever"
		time.sleep(t)
		self.mr.stop()
		self.ml.stop()
		self.checkMotorStop()

	def mesureColor(self):									#returns "red" or "blue"
		if self.cs.bin_data("hhh")[0] > self.cs.bin_data("hhh")[2] * 2.7:
			return "red"
		elif self.cs.bin_data("hhh")[2] > self.cs.bin_data("hhh")[0] * 2.5:
			return "blue"
		else:
			return "no color"

	def mesureBrightness(self):								#returns int
		self.cs.mode = "RGB-RAW"
		return self.cs.bin_data("hhh")[0] + self.cs.bin_data("hhh")[1] + self.cs.bin_data("hhh")[2]

	def findLine(self, b = 230, bs = 75, timestamp = 15):	#returns whether a line was found
		self.mr.stop()
		self.ml.stop()
		timecount = 0

		while timecount < timestamp:
			colorsum = self.mesureBrightness()
			#print("Turn left",colorsum)
			if(colorsum < b):
				self.mr.stop()
				self.ml.stop()
				self.checkMotorStop()
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
				self.mr.stop()
				self.ml.stop()
				self.checkMotorStop()
				return True
			self.mr.speed_sp = -bs
			self.ml.speed_sp = bs
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			timecount -= 1
			time.sleep(0.05)
		return False

	def scanPoint(self, ignore = 0):						#returns list with point-directions
		directionList = []
		for i in range (4):
			if ignore is self.view:
				stat = -1
			else:
				stat = -2
			if self.findLine():
				directionList.append((self.view, stat))
				self.view = self.angle_to_direction(self.direction_to_angle(self.view) + 90, "deg")
			else:						#turn back to the middle if no line was found
				directionList.append((self.view , -3))
				self.mr.speed_sp = 75
				self.ml.speed_sp = -75
				self.mr.command = "run-forever"
				self.ml.command = "run-forever"
				time.sleep(0.8)
				self.mr.stop()
				self.ml.stop()
				self.view = self.angle_to_direction(self.direction_to_angle(self.view) + 90, "deg")
			self.turn_by_degree(90,150)
			self.mr.stop()
			self.ml.stop()
			self.checkMotorStop()
		if not self.findLine():
			self.mr.speed_sp = 75
			self.ml.speed_sp = -75
			self.mr.command = "run-forever"
			self.ml.command = "run-forever"
			time.sleep(0.8)
			self.mr.stop()
			self.ml.stop()
			self.checkMotorStop()
		return {self.position: directionList}

	def transformCoordinates(self, dx, dy):					#rounds cm to coordinates !!!Sets position
		dx /= 50
		dy /= 50
		xn = self.oldposition[0] + round(dx)
		yn = self.oldposition[1] + round(dy)
		self.position = (xn,yn)
		print (self.position)

	def angle_to_direction(self, angle, deg = "rad"):
		if deg is "rad":
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
		else:
			while angle >= 360:
				angle -= 360
			while angle < 0:
				angle += 360
			if angle <= 180 * 1/4 or angle > 180 * 7/4:
				return Direction.NORTH
			elif angle <= 180 * 3/4 and angle > 180 * 1/4:
				return Direction.WEST
			elif angle <= 180 * 5/4 and angle > 180 * 3/4:
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

	def turn_by_direction(self, direction):					#changes view !!!
		turn_angle = self.direction_to_angle(direction) - self.direction_to_angle(self.view)
		if turn_angle > 180:
			turn_angle -= 180
			turn_angle *= -1
		elif turn_angle < -180:
			turn_angle += 180
			turn_angle *= -1
		self.turn_by_degree(turn_angle, 150)
		self.view = direction
		self.findLine(150,40, 35)

	def checkMotorStop(self):
		while self.ml.speed != 0 or self.mr.speed != 0:
			self.mr.stop()
			self.ml.stop()

	def createMessage(self):								#sets view, if status is "blocked"
		end_direction = self.angle_to_direction(self.direction_to_angle(self.view)+180, "deg")
		if self.status is "free":
			return [(self.oldposition, self.oldview.value),(self.position, end_direction.value), self.status]
		else:
			self.position = self.oldposition
			self.view = self.angle_to_direction(self.direction_to_angle(self.oldview)+180, "deg")
			return [(self.oldposition, self.oldview.value),(self.oldposition, self.oldview.value), self.status]

	def setPosition(self, new_pos):
		self.position = new_pos

	def setView(self, direction):
		self.view = self.angle_to_direction(self.direction_to_angle(direction)+180, "deg")

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters

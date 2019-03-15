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
		if a<0:
			mr.speed_sp = bs+bs*a*f
			ml.speed_sp = bs
		else:
			mr.speed_sp = bs
			ml.speed_sp = bs-bs*a*f
		mr.command = "run-forever"
		ml.command = "run-forever"
		time.sleep(0.1)
		if colorsum > 500:
			mr.stop()
			ml.stop()
			break

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters


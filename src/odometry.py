#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time
def drive():
    m = ev3.LargeMotor("outB")
    m.run_timed(time_sp=3000, speed_sp=500)
    time.sleep(5000)

#  Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters


#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
from planet import Direction, Planet
from communication import Communication
from odometry import Robot

client = None  # DO NOT EDIT


def run():
    # DO NOT EDIT
    # the deploy script uses this variable to stop the mqtt client after your program stops or crashes.
    # your script isn't able to close the client after crashing.
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER
    print("Hello World!")
    bob = Robot()
    while True:
        direction_str = input("Input: ")
        """kp = input("Kp: ")
        kp = float(kp)
        ki = input("Ki: ")
        ki = float(ki)
        kd = input("Kd: ")
        kd = float(kd)"""
        bob.turn_by_direction(Direction(direction_str))
        bob.drive(100,1.0) #100 und 1.1 funktioniert
    #print(bob.mesureBrightness())
    #bob.turn_by_degree(90,100)


# DO NOT EDIT
if __name__ == '__main__':
    run()
